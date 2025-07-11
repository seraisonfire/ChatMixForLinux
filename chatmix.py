import re  # for getting chatmix value
import subprocess  # for running the whole thing
import time  # for polling rate

# all applications that should be considered comms by chatmix e.g. Discord 
comm_applications = [
    "Discord"
]

# all other applications are considered "game audio", the following applications will be exceptions in case they are ever needed, and will not be regulated
game_exceptions = (
    []
)  
# TO ADD NEW APPLICATION:
# 1. Open the application you want to add, go into a call or something
# 2. Run 'wpctl status'
# 3. Search for the ID of the application under Audio > Streams. The name doesn't have to match, it can be also be "Chromium" for example
# 4. Run 'wpctl inspect ID', with the ID being the one you just found. If your app doesn't show up, just try all and guess a bit
# 5. Under "application.process.binary", if the name matches the application, you're golden, add that here. Capitalization is important though


volume = None
comms_streams_exist = None

# Option in case you don't want the chatmix to work when you aren't chatting
ONLY_RUN_WHEN_COMMS = True


def get_chatmix_value():
    try:
        chatmix_value = subprocess.run(
        ["headsetcontrol", "-m"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        chatmix_value = chatmix_value[-4:]
        chatmix_value = int(re.sub(r"\D", "", chatmix_value))

        global volume
        if chatmix_value == volume:
            return
        volume = chatmix_value
    except:
        time.sleep(10)

def find_all_comms():
    global comms_streams_exist
    comms_streams = []
    for c in comm_applications:
        for i in find_stream_ID(c):
            comms_streams.append(i)
    comms_streams_exist = True
    if len(comms_streams) == 0:
        comms_streams_exist = False

    return comms_streams

def find_all_else():
    # shell command to find all pipewire streams
    command = f'pw-dump | jq \'.[] | select(.type=="PipeWire:Interface:Node") | select(.info.props."media.class" == "Stream/Output/Audio") |.id\''
    
    streams = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    streams = streams.split("\n")[:-1]
    for i in range(0, len(streams)):
        streams[i] = int(streams[i])
    comms_and_exceptions = find_all_comms()
    # remove comms and applications in the game_exceptions array
    global game_exceptions
    for e in game_exceptions: 
        IDs = find_stream_ID(e)
        for i in IDs:
            # The loop is needed because find_stream_ID returns an array, in case there are multiple streams matching the name
            comms_and_exceptions.append(i)
    for c in comms_and_exceptions:
        if c in streams:
            streams.remove(c)
    return streams



def find_stream_ID(application_name):
    IDs = []
    # shell command to find pipewire streams from specific application
    command = f'pw-dump | jq \'.[] | select(.type=="PipeWire:Interface:Node") | select(.info.props."application.process.binary" == "{application_name}") | select(.info.props."media.class" == "Stream/Output/Audio") |.id\''

    streams = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    streams = streams.split("\n")[:-1]
    for s in streams:
        IDs.append(int(s))
    return IDs

def calculate_volumes(chatmix_value):
    # Clamp value to [0, 128] just in case
    chatmix_value = max(0, min(128, chatmix_value))

    if chatmix_value <= 64:
        game_volume = (chatmix_value / 64) * 100
        comms_volume = 100
    else:
        game_volume = 100
        comms_volume = ((128 - chatmix_value) / 64) * 100

    return [round(game_volume), round(comms_volume)]


def set_volume(stream, new_volume):
    subprocess.run(["wpctl", "set-volume", f"{stream}", f"{str(new_volume)}%"])

def apply_volumes():
    global volume, comms_streams_exist, ONLY_RUN_WHEN_COMMS

    comms = find_all_comms()
    if not comms_streams_exist and ONLY_RUN_WHEN_COMMS:
        return
    other_audio = find_all_else()
    game_volume, comms_volume = calculate_volumes(volume)[0], calculate_volumes(volume)[1]
    for c in comms:
        set_volume(c, comms_volume)
    for o in other_audio:
        set_volume(o, game_volume)


def mix():
    old_volume = volume
    get_chatmix_value()
    if not old_volume == volume:
        apply_volumes()

while True:
    mix()
    time.sleep(0.05)
