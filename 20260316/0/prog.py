import asyncio

async def echo(reader, writer):
    host, port = writer.get_extra_info('peername')
    while data := await reader.readline():
        match data.decode().split():
            case ['print', *args]:
                try:
                    writer.write((' '.join(args) + '\n').encode())
                except Exception as E:
                    print(E, 'exception')
            case ['info', 'host']:
                writer.write((str(host) + '\n').encode())
            case ['info', 'port']:
                writer.write((str(port) + '\n').encode())
            case _:
                writer.write('Unknown command\n'.encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
