import aiohttp
import asyncio
import os
import time
import json
import websockets

import commands
from utils import API_BASE, TOKEN, HEADERS, SESSION, SESSION_DATA, parse_data

async def start(resume):
    '''Connection to the API'''
    async with websockets.connect('wss://gateway.discord.gg?encoding=json&v=6', loop=asyncio.get_event_loop()) as websocket:
        start_time = time.time()
        if not resume:
            hello = parse_data(await websocket.recv())
            payload = {
                "op":2,
                "d":{
                    "token":TOKEN, 
                        'properties': {
                            '$properties':os.name, 
                            '$browser':'dapi-bot', 
                            '$device':'dapi-bot'
                        },
                    'compress':True, 
                    'large_threshold': 250,
                    "presence": {
                        "game": {
                            "name": " with Discord API",
                            "type": 0
                        },
                        "status": "dnd",
                        "since": int(time.time()),
                        "afk": False
                    }
                }
            }
            await websocket.send(json.dumps(payload))
            ready = parse_data(await websocket.recv())
            SESSION_DATA[0] = ready['d']['session_id']
            for i in ready['d']['guilds']:
                x = parse_data(await websocket.recv())
            print('Bot connected')
        else:
            payload = {
                "op":6,
                "d":{
                    "token":TOKEN,
                    "session_id":SESSION_DATA[0],
                    "seq":SESSION_DATA[1]
                }
            }
            await websocket.send(json.dumps(payload))
            hello = parse_data(await websocket.recv())
            await websocket.recv()
        while True:
            if int(time.time() - start_time)+1 % hello['d']['heartbeat_interval'] == 0:
                payload = {
                    "op": 1,
                    "d": SESSION_DATA[1]
                }
                await websocket.send(json.dumps(payload))
                await websocket.recv()
            try:
                event = parse_data(await websocket.recv())
                SESSION_DATA[1] = event['s']
                print(event['t']) #Logs every event the WS sendss
                await commands.parse_event(event)
            except websockets.exceptions.ConnectionClosed:
                break

asyncio.get_event_loop().run_until_complete(start(False))
# This is to ensure the bot doesn't stop
while True:
    asyncio.get_event_loop().stop()
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(start(True))
SESSION.close()
asyncio.get_event_loop().close()
