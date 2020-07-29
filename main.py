#!/usr/local/bin/python3
import src.runner

if __name__ == "__main__":

    try:
        src.runner.main()
    except KeyboardInterrupt:
        print('Exiting...')
