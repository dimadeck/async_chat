import sys

from chats import chat_asyncio as as_chat, chat_ws_asyncio as as_ws_chat, AsyncIO as as_chats
from chats import chat_tornado as tor_chat, chat_ws_tornado as tor_ws_chat, Tornado as tor_chats
from chats import chat_twisted as tw_chat, chat_ws_twisted as tw_ws_chat, Twisted as tw_chats
from testing import test_all

LAUNCH = {'tor_chat': tor_chat.main, 'tor_ws_chat': tor_ws_chat.main, 'tor_chats': tor_chats.main,
          'as_chat': as_chat.main, 'as_ws_chat': as_ws_chat.main, 'tw_chats': tw_chats.main,
          'tw_chat': tw_chat.main, 'tw_ws_chat': tw_ws_chat.main, 'as_chats': as_chats.main,
          'test': test_all}

LAUNCH_KEYS = list(LAUNCH.keys())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog in LAUNCH:
            LAUNCH[prog]()
        else:
            print(f'Unknown program! Available: {LAUNCH_KEYS}')
    else:
        print(f'Type program name: {LAUNCH_KEYS}')
