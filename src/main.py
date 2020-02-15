import sys
from LeapListener import LeapListener
sys.path.insert(0, "./lib/x86")
import Leap


def main():
    listener = LeapListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
