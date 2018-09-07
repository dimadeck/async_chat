import sys

from servers import asyncIO as as_chat, asyncIO_ws as as_ws_chat, asyncIO_pair as as_chats
from servers import tornado as tor_chat, tornado_ws as tor_ws_chat, tornado_pair as tor_chats
from servers import twisted as tw_chat, twisted_ws as tw_ws_chat, twisted_pair as tw_chats
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
