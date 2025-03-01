import asyncio
import json
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived


class NetworkPoint(QuicConnectionProtocol):
    def __init__(self, quic, bandwidth_capacity=1000, latency=10, **kwargs):
        super().__init__(quic, **kwargs)
        self.bandwidth_capacity = bandwidth_capacity  # Total bandwidth available
        self.latency = latency  # Simulated latency

# Get Kafka Data
    async def handle_bandwidth_request(self, stream_id: int, data: bytes):
        """Process a bandwidth request and send a response"""
        print(f"📩 Raw received data: {data}")  # ✅ Debugging

        try:
            request = json.loads(data.decode())
            print(f"📥 Received request from stream {stream_id}: {request}")  # ✅ Log received JSON

            if request.get("request") == "get_bandwidth":
                response = {
                    "response": "bandwidth_update",
                    "available_bandwidth": self.bandwidth_capacity,
                    "latency": self.latency
                }

                # Send response
                response_data = json.dumps(response).encode()
                self._quic.send_stream_data(stream_id, response_data)
                await self.send_pending()  # ✅ Ensure the response is sent

                print(f"✅ Sent response to stream {stream_id}: {response}")  # ✅ Log sent response

        except json.JSONDecodeError:
            print(f"❌ Received invalid JSON from stream {stream_id}")

# Get Quic Data
    def quic_event_received(self, event):
        """Handle ALL incoming QUIC events"""
        print(f"🟢 QUIC Event: {type(event).__name__} - {event}")

        if isinstance(event, StreamDataReceived):
            print(f"🔔 Data Received on Stream {event.stream_id}, Length: {len(event.data)}")
            asyncio.create_task(self.handle_bandwidth_request(event.stream_id, event.data))


async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("cert.pem", "key.pem")  # Ensure you have TLS certs for QUIC

    # 🚨 Security Warning: Only use `verify_mode = False` in testing!
    config.verify_mode = False

    server = await serve(
        host="0.0.0.0",
        port=4433,
        configuration=config,
        create_protocol=NetworkPoint
    )

    print("🚀 NetworkPoint listening on port 4433...")
    await asyncio.Future()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
