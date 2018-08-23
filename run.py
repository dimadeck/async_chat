import sys

import chat_asyncio as as_chat
import chat_tornado as tor_chat
import chat_twisted as tw_chat
import chat_ws_asyncio as aio_ws_chat
import chat_ws_tornado as tor_ws_chat
from binder import main as bind

LAUNCH = {'tw_chat': tw_chat.main, 'as_chat': as_chat.main, 'tor_chat': tor_chat.main,
          'aio_ws_chat': aio_ws_chat.main, 'tor_ws_chat': tor_ws_chat.main,
          'bind': bind}
BIND = ['as', 'tor', 'tcp_all', 'ws_all']
LAUNCH_KEYS = list(LAUNCH.keys())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog == 'bind':
            bind_prog = sys.argv[2]
            if bind_prog in BIND:
                LAUNCH[prog](bind_prog)
            else:
                print(f'Unknown program! Available: {BIND}')
        elif prog in LAUNCH:
            LAUNCH[prog]()
        else:
            print('Unknown program!')
    else:
        print(f'Type program name: {LAUNCH_KEYS}')
