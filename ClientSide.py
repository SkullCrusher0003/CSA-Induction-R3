import socketio, time, string, random, webbrowser
from socketio.exceptions import TimeoutError
import os
import socketio.exceptions

sio = socketio.SimpleClient()
try:
    sio.connect("<your host address here>", transports=['websocket'])
except socketio.exceptions.ConnectionError:
    pass

# Random Token Generator
def token_generator():
    chars = string.ascii_letters + string.digits
    token_list = []
    for i in range(6):
        token_list.append(random.choice(chars))
    token = ''.join(token_list)
    print(f"Your token to be entered for registration is: {token} \nPlease use the /register command to initiate registration.")
    return token
roomID = token_generator()

sio.emit('regr', {'roomID': f'{roomID}'})

# Execution of Commands
def open_website(curr_event):
    link = curr_event[1]
    if link.startswith("www."):
        pass
    else:
        link = f"www.{link}"
    webbrowser.open(link)

def wait_for(curr_event):
    secs = curr_event[1]
    time.sleep(secs)

def shell_cmd(curr_event):
    cmd = curr_event[1]
    os.system(cmd)

# List of Commands
cmd_list = [open_website, wait_for, shell_cmd]

# Parsing the Received Event
def process_event(event):
    for i in range(len(event[1])):
        current_step = event[1][i]
        cmd_list[current_step[0]-1](current_step)
        

# Continuously Listening for Events
while True:
    try:
        event = sio.receive(timeout = 300)
    except TimeoutError:
        pass
    else:
        process_event(event)
