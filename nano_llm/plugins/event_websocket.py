import asyncio
import websockets
import socket
import threading
import logging

from nano_llm.plugin import Plugin

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class EventWebSocket(Plugin):
    """
    Plugin that runs a WebSocket server and sends event messages (e.g. 'swim', 'angry')
    to all connected clients when triggered.
    """
    connected_clients = set()
    server_thread_started = False

    def __init__(self, **kwargs):
        super().__init__(inputs=['text'], outputs=[], threaded=False, **kwargs)

        # Start the server only once globally
        if not EventWebSocket.server_thread_started:
            EventWebSocket.server_thread_started = True
            threading.Thread(target=self.run_server, daemon=True).start()

    def process(self, input, **kwargs):
        """
        Sends the event word directly (e.g. 'swim', 'angry') over WebSocket.
        """
        logger.info(f"EventWebSocket process() received: {input}")

        if isinstance(input, str):
            message = input.strip().lower()
            asyncio.run_coroutine_threadsafe(self.send_command(message), EventWebSocket.loop)
            logger.info(f"Sent WebSocket message: '{message}'")
        else:
            logger.warning("EventWebSocket received non-string input")

    async def send_command(self, command):
        for client in EventWebSocket.connected_clients.copy():
            try:
                await client.send(str(command))  # Ensure it's a raw string
                logger.info(f"Sent command '{command}' to client")
            except Exception as e:
                logger.warning(f"Failed to send command to client: {e}")
                EventWebSocket.connected_clients.discard(client)

    def run_server(self):
        EventWebSocket.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(EventWebSocket.loop)
        EventWebSocket.loop.run_until_complete(self.main())

    async def main(self):
        threading.Thread(target=self.udp_discovery, daemon=True).start()
        logger.info("UDP discovery thread started")

        try:
            server = await websockets.serve(self.handle_websocket, "0.0.0.0", 8765)
            logger.info("WebSocket server started on port 8765")
            await server.wait_closed()
        except OSError as e:
            logger.error(f"Failed to start WebSocket server: {e}")

    async def handle_websocket(self, websocket):
        logger.info("Client connected")
        EventWebSocket.connected_clients.add(websocket)
        try:
            async for message in websocket:
                logger.info(f"Received: {message}")
        except websockets.ConnectionClosed as e:
            logger.info(f"Connection closed: {e}")
        finally:
            EventWebSocket.connected_clients.discard(websocket)

    def udp_discovery(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            udp_sock.bind(('', 8765))
            logger.info("UDP discovery started on port 8765")
        except OSError as e:
            logger.error(f"Failed to bind UDP socket: {e}")
            return

        while True:
            try:
                data, addr = udp_sock.recvfrom(1024)
                message = data.decode('utf-8')
                if message == "DISCOVER_WEBSOCKET_SERVER":
                    logger.info(f"Received discovery request from {addr}")
                    response = "WEBSOCKET_SERVER_RESPONSE"
                    udp_sock.sendto(response.encode('utf-8'), addr)
                    logger.info(f"Sent response to {addr}")
            except Exception as e:
                logger.error(f"Error in UDP discovery: {e}")

