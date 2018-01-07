# DAPI Bot
This bot is created in pure Discord API, without any wrappers. More technical specifications below.

# Contributing
I'll only accept PRs with bug fixes and I might not accept all of them. The aim of this project is for me to learn stuff, and not to get a bot working.    
I ask questions regularly about this on the CodeGrok discord though. That's also where the testing goes on. 

# What's on the TODO list?
Look at the issues, I created a to do list there, more like a challenge. You can suggest more things in the comments.

# Technical Specifications
Python 3.6 (I use fstrings here) 
asyncio
websockets 
aiohttp

# How to run this?
- Fill up `config.json` similar to `config.json example `
  - Basically, include your token and prefix
- `pip install -r requirements.txt ` (got to do this) 
- A samples folder will be created upon launch which will contain JSON files of all the WS events discord gives us (might get removed)
- Lastly, do `python websocket.py` and it'll start it up.

# My own fork
## How to add commands? 
This might get changed in the future.   
- Go to `commands.py`
- Add your command similar to the format of the already created ones in `parse_command`
- It uses startswith ;)

## How to remove roles.....? or do whatever that isn't already done? 
- Read the DDevs documentation and use the request function.

### I won't be providing support for this. 