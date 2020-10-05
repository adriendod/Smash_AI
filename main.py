#!/usr/bin/python3
import argparse
import signal
import sys
import melee
import action_space



port = 2
opponent = 1
debug = False
framerecord = False
address = "127.0.0.1"
dolphin_executable_path = "../Ishiiruka/build/Binaries"
connect_code = ""

log = None
if debug:
    log = melee.Logger()

framedata = melee.FrameData(framerecord)

console = melee.Console(path=dolphin_executable_path,
                        slippi_address=address,
                        slippi_port=51441,
                        blocking_input=False,
                        logger=log)

console.render = True

controller = melee.Controller(console=console,
                              port=port,
                              type=melee.ControllerType.STANDARD)

controller_opponent = melee.Controller(console=console,
                                       port=opponent,
                                       type=melee.ControllerType.GCN_ADAPTER)

# This isn't necessary, but makes it so that Dolphin will get killed when you ^C
def signal_handler(sig, frame):
    console.stop()
    if debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    if framerecord:
        framedata.save_recording()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Run the console
console.run()

# Connect to the console
print("Connecting to console...")
if not console.connect():
    print("ERROR: Failed to connect to the console.")
    print("\tIf you're trying to autodiscover, local firewall settings can " +
          "get in the way. Try specifying the address manually.")
    sys.exit(-1)
print("Console connected")

# Plug our controller in
#   Due to how named pipes work, this has to come AFTER running dolphin
#   NOTE: If you're loading a movie file, don't connect the controller,
#   dolphin will hang waiting for input and never receive it
print("Connecting controller to console...")
if not controller.connect():
    print("ERROR: Failed to connect the controller.")
    sys.exit(-1)
print("Controller connected")

# Main loop
while True:
    step = 0
    gamestate = console.step()
    distance = gamestate.distance
    print(distance)
    if gamestate is None:
        continue
    try:
        print(gamestate.player[1].x)
    except:
        print("no player gamestate")

    # If in game:
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:

        if framerecord:
            framedata._record_frame(gamestate)

        action_space.press_random_button(controller)

    # If in a menu:
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            port,
                                            melee.Character.FOX,
                                            melee.Stage.POKEMON_STADIUM,
                                            connect_code,
                                            autostart=True,
                                            swag=True)


    if log:
        log.logframe(gamestate)
        log.writeframe()
