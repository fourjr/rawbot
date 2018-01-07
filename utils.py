import asyncio
import json
import zlib
import aiohttp

import errors

API_BASE = 'https://discordapp.com/api/v6'
CONFIG_FILE = json.load(open('data/config.json'))
TOKEN = CONFIG_FILE['token']
HEADERS = {'Authorization': 'Bot ' + TOKEN,
           'User-Agent': 'DiscordBot (https://www.github.com/fourjr/dapi-bot,\
           aiohttp and websockets)'}
SESSION = aiohttp.ClientSession(loop=asyncio.get_event_loop())
SESSION_DATA = [None, None]
PREFIX = './'

def parse_data(data):
    '''Parses the websocket data into a dictionary'''
    if isinstance(data, bytes):
        return json.loads(zlib.decompress(data, 15, 10490000).decode('utf-8'))
    else:
        return json.loads(data)

def find(obj:list, **kwargs):
    '''Finds a element of the given object that satisfies all kwargs'''
    for i in obj:
        if all(i[k] == kwargs[k] for k in kwargs):
            return i
    return None

async def request(http, endpoint, obj=None):
    '''Used to request to the Discord API'''
    if http == 'POST':
        resp = await SESSION.post(API_BASE + endpoint, json=obj, headers=HEADERS)
    elif http == 'DELETE':
        resp = await SESSION.delete(API_BASE + endpoint, json=obj, headers=HEADERS)
    if resp.status == 204:
        return
    obj = await resp.json()
    print(resp)
    if 300 > resp.status >= 200:
        return #ok
    elif resp.status == 403:
        raise errors.Forbidden(resp, obj)
    elif resp.status == 404:
        raise errors.NotFound(resp, obj)
    elif resp.status == 429:
        raise errors.RateLimit(resp, obj)

async def get_channel(channel_id):
    '''Gets a channel by the ID'''
    return await request('GET', f'/channels/{channel_id}')

async def send_message(channel_id, content):
    '''Sends a plain text message to the provided channel ID'''
    return await request('POST', f'/channels/{channel_id}/messages', {'content':content})