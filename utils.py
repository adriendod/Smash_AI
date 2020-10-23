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