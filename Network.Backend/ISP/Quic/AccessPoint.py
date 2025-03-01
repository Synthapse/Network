import asyncio
import json
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol


class AccessPoint:
    def __init__(self, id, mb_available, bandwidth, latency, network_type, location, kafka_broker, isp_topic,
                 network_point_ip, network_point_port):
        self.id = id
        self.mb_available = mb_available
        self.bandwidth = bandwidth
        self.latency = latency
        self.network_type = network_type
        self.location = location
        self.kafka_broker = kafka_broker
        self.isp_topic = isp_topic
        self.network_point_ip = network_point_ip
        self.network_point_port = network_point_port

    async def request_bandwidth_update(self):
        config = QuicConfiguration(is_client=True)

        try:
            async with connect(self.network_point_ip, self.network_point_port, configuration=config) as connection:
                stream_id = connection.get_next_available_stream_id()
                request = {"request": "get_bandwidth", "access_point_id": self.id}

                # Send request
                await connection.send_stream_data(stream_id, json.dumps(request).encode())

                # Receive response
                response_data = await self.receive_response(connection, stream_id)

                if response_data:
                    print(f"Access Point {self.id} - Received bandwidth update: {response_data}")
                else:
                    print(f"Access Point {self.id} - No response received.")

        except Exception as e:
            print(f"Access Point {self.id} - Error in bandwidth request: {e}")

    async def receive_response(self, connection: QuicConnectionProtocol, stream_id: int):
        """ Wait for response on the given stream """
        try:
            while True:
                event = await connection.wait_for_event()
                if event.stream_id == stream_id and event.data:
                    return json.loads(event.data.decode())
        except Exception as e:
            print(f"Access Point {self.id} - Error receiving response: {e}")
            return None


async def main():
    access_point = AccessPoint(
        id=1,
        mb_available=500,
        bandwidth=50,
        latency=20,
        network_type="5G",
        location="City Center",
        kafka_broker="localhost:9092",
        isp_topic="isp_updates",
        network_point_ip="127.0.0.1",
        network_point_port=4433
    )

    await access_point.request_bandwidth_update()


# Run the event loop
asyncio.run(main())
