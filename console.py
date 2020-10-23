import melee
import config
import signal
import sys

if config.debug:
    log = melee.Logger()

framedata = melee.FrameData(config.framerecord)

console = melee.Console(path=config.dolphin_executable_path,
                        slippi_address=config.address,
                        slippi_port=51441,
                        blocking_input=False,
                        logger=config.log)
console.render = True
controller = melee.Controller(console=console,
                              port=config.port,
                              type=melee.ControllerType.STANDARD)
controller_opponent = melee.Controller(console=console,
                                       port=config.opponent_port,
                                       type=melee.ControllerType.GCN_ADAPTER)


# This isn't necessary, but makes it so that Dolphin will get killed when you ^C
def signal_handler(sig, frame):
    console.stop()
    if config.debug:
        log.writelog()
        print("")  # because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    if config.framerecord:
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
print("Connecting controller to console...")
if not controller.connect():
    print("ERROR: Failed to connect the controller.")
    sys.exit(-1)
print("Controller connected")
