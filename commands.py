import json
from utils import PREFIX, request
import utils, errors

async def parse_event(event):
    '''Parses all events the discord websocket connection sends'''
    with open('samples/' + event['t'] + '.json', 'w+') as f:
        json.dump(event['d'], f, indent=4) #just so i have a copy of the events
    assign = {'MESSAGE_CREATE': 'parse_command', 'PRESENCE_UPDATE':'parse_presence_change'}

    if event['t'].strip() not in assign:
        return print("NotImplementedError(f'Event {event[\"t\"]} has not been added to assign.')") 
        #to be changed to a raise

    to_run = assign[event['t']]
    if to_run not in globals():
        raise NotImplementedError(f'Function {to_run} not added, part of {event["t"]}')
    return await globals()[to_run](event['d'])

async def parse_command(message):
    '''Parses all MESSAGE_CREATE events'''
    if message['content'].startswith(PREFIX + 'hi'):
        print('activated')
        return await utils.send_message(message['channel_id'], 'Hello!')

    if message['content'].startswith(PREFIX + 'kick'):
        try:
            days = int(message['content'].replace(PREFIX + 'kick', ''))
        except ValueError:
            await utils.send_message(message['channel_id'], 'Invalid day (provide a number)')
        else:
            await request('DELETE', '/guilds/345787308282478592/members/319778485239545868', {'delete-message-days':days})
            await utils.send_message(message['channel_id'], 'Kicked!')

async def parse_presence_change(user):
    '''Parses all PRESENCE_UPDATE events'''
    pass