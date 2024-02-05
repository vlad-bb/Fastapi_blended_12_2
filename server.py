import asyncio
import json
import logging
import re
import aiohttp
import websockets
import names
from aiopath import AsyncPath
from aiofile import async_open
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from datetime import datetime, timedelta
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)
ua = UserAgent()


async def request(url: str, querystring: dict, headers: dict) -> dict | str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=querystring, headers=headers) as response:
            response.raise_for_status()
            response_json = await response.json()
            data = response_json["exchangeRate"]
            pattern = '|{:^10}|{:^10}|{:^10}|\n'
            result = '|{:^32}|\n'.format(response_json["date"])
            result += pattern.format('Currency', 'Sale', 'Purchase')
            for el in data:
                currency = el["currency"]
                if currency in ['USD', 'EUR']:
                    result += pattern.format(el["currency"], el["saleRate"], el["purchaseRate"])
            return result


async def get_exchange(days):
    url = "https://api.privatbank.ua/p24api/exchange_rates"
    headers = {"User-Agent": f"{ua.random}"}
    tasks = []
    for day in range(int(days)):
        date_string = f'{datetime.now().date() - timedelta(days=day):%d.%m.%Y}'
        querystring = {"json": "", "date": f"{date_string}"}
        tasks.append(request(url, querystring, headers))

    result = await asyncio.gather(*tasks)
    return ''.join(result)


async def save_logs(msg: str, remote_address: str):
    apath = AsyncPath('logs.txt')
    if await apath.exists():
        async with async_open('logs.txt', 'a', encoding='utf-8') as afp:
            await afp.write(f'{datetime.now()} - {remote_address} - [{msg}]\n')
    else:
        async with async_open('logs.txt', 'w', encoding='utf-8') as afp:
            await afp.write(f'{datetime.now()} - {remote_address} - [{msg}]\n')


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            r = re.search(r'(exchange)\s*(\d*)', message)
            if r:
                await save_logs(message, ws.remote_address)
                if r.group(2):
                    exchange = await get_exchange(r.group(2))
                    await self.send_to_clients(exchange)
                else:
                    exchange = await get_exchange(1)
                    await self.send_to_clients(exchange)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
