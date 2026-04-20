import asyncio
import prog_root

async def echo(reader, writer):
    while data := await reader.readline():
        try:
            res = prog_root.sqroots(data.strip().decode())
        except Exception as E:
            res = str(E)
        writer.write(f"{res}\n".encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())