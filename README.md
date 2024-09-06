# CSA Round 3 Task
## Information
### Description of Project
This project consists of a discord bot that is capable of running commands on your computer. The user is required to select from pre-existing routines (i.e. sequence of actions) which are to be executed.

### About Repository
This repository contains both the code for the client side (on user's personal machine) and the server side (which runs the bot). 

### Potential Improvements
The following improvements would be made in the near future:
- Ability for a user to register their own custom routine
- A database integration which stores each user's routines linked to their discord userID
- Greater control over the system (i.e. more possible actions)

## Usage
### Steps
1. Download the files
2. Replace `<your bot token here>` with your discord bot's token in the [Server File](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/ServerSide.py)
3. Replace `<your host address here>` with your (server's) host IP address in the [Server File](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/ServerSide.py) and [Client File](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/ClientSide.py)
You can find your IP address by running `ipconfig` in command prompt.
4. Modify the routines as you wish in the [Routines file](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/routines.py)
5. Replace `[3, '']` in the [Routines file](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/routines.py) under `r2` with the complete file path of [Sample File](https://github.com/SkullCrusher0003/CSA-Induction-R3/blob/main/sample.py) on your computer.
6. Run the server first, then the client.

### Libraries 
The libraries maybe installed by running `pip install <library name>` in your terminal.
- discord.py
- py-cord
- asyncio
- python-socketio
- aiohttp

