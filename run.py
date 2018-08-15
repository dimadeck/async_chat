import sys

import chat_asyncio as as_chat
import chat_tornado as tor_chat
import chat_twisted as tw_chat
import aiohttp_web as aio_chat

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog == 'tw_chat' or prog == '1':
            tw_chat.main()
        elif prog == 'as_chat' or prog == '2':
            as_chat.main()
        elif prog == 'tor_chat' or prog == '3':
            tor_chat.main()
        elif prog == 'aio_chat' or prog == '4':
            aio_chat.main()
        else:
            print('Unknown program!')
    else:
        print("Type program name: 'tw_chat' or 'as_chat' or 'tor_chat' or 'aio_chat")
