# Set data.config before importing packetdecoder so that it is available to all packetdecoders
import data
import tomllib
with open("config.toml", "rb") as f:
    data.config = tomllib.load(f)
print(data.config)

import asyncio
import traceback

#set up events and listeners
import events
import listeners

import packetdecoders as pd

from data import Connection, connections
from enums import State


HOST = "0.0.0.0"
PORT = 25565

async def handle_connection(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"New connection from {addr!r}")

    connection = Connection(addr[0], addr[1], reader, writer, State.HANDSHAKE)
    connections[addr] = connection
    
    while True:
        data = await reader.read(1024)
        if not data:
            break
        
        try:
            return_data = pd.decode_packet(data, connection)
        except Exception as e:
            traceback.print_exc()
            return_data = {"error": str(e)}

        if return_data is None:
            # never going to happen but there just in case
            # can be triggered by packetdecoder not getting return data
            print(f"Return data is None for data: {data}")
        if return_data == {}:
            continue
        if "error" in return_data:
            print(return_data["error"])
        if "close" in return_data:
            writer.close()
            await writer.wait_closed()
            break
        
async def main():
    server = await asyncio.start_server(handle_connection, HOST, PORT)

    print(f"Server started on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
    #import packetdecoders.config.main as config_main
    #config_main.main()