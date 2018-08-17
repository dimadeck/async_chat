import sys

import aiohttp_web as aio_chat
import bind_aio_as as all_tcp
import chat_asyncio as as_chat
import chat_tornado as tor_chat
import chat_twisted as tw_chat

LAUNCH = {'tw_chat': tw_chat.main, 'as_chat': as_chat.main, 'tor_chat': tor_chat.main, 'aio_chat': aio_chat.main,
          'all_tcp': all_tcp.main}
LAUNCH_KEYS = list(LAUNCH.keys())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog in LAUNCH:
            LAUNCH[prog]()
        else:
            print('Unknown program!')
    else:
        print(f'Type program name: {LAUNCH_KEYS}')
