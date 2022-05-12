from sys import path

path.append('packages')

from packages.adapters.zohoSDK.auth import sdk_initializer
from packages.presentation.console.console_main import execute


def initialize_sdk():
    sdk_initializer.initialize()


def console():
    execute()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initialize_sdk()
    console()
    print('done')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
