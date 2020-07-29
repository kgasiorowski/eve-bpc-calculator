#!/usr/local/bin/python3
import src.driver

if __name__ == "__main__":
    try:
        src.driver.main()
    except KeyboardInterrupt:
        print('Exiting...')
