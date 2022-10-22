import carreralib
import contextlib
import logging
import argparse

from carreralib import ControlUnit


parser = argparse.ArgumentParser(prog='python3 carl_test.py')
parser.add_argument('-s', '--speed', type=int)
args = parser.parse_args()


def main():
    print("Hello world!")
    with contextlib.closing(ControlUnit('/dev/ttyUSB0', timeout=300)) as cu:
        for i in range(7):
            cu.setspeed(i,args.speed)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    filename='carreralib.log',
                    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S')
    main()
