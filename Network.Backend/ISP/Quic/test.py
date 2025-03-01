import json
import asyncio
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived


async def main():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False  # Ignore self-signed certificate errors

    async with connect("127.0.0.1", 4433, configuration=config) as protocol:
        quic = protocol._quic  # Access the underlying QUIC connection

        stream_id = quic.get_next_available_stream_id()  # ✅ Get a new stream ID
        request = {"request": "get_bandwidth"}

        quic.send_stream_data(stream_id, json.dumps(request).encode())



# Run the async function
asyncio.run(main())
