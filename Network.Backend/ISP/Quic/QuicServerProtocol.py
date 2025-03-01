import asyncio
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration

class QuicServerProtocol(QuicConnectionProtocol):
    async def quic_data_received(self, stream_id, data):
        print(f"Received QUIC data: {data.decode()}")
        self._quic.send_stream_data(stream_id, b"Data received")

async def run_quic_server(host, port):
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("cert.pem", "key.pem")  # TLS encryption
    await serve(host, port, configuration=config, create_protocol=QuicServerProtocol)

asyncio.run(run_quic_server("0.0.0.0", 4433))

