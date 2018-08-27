import sys

from chats import chat_asyncio as as_chat, chat_twisted as tw_chat, chat_tornado as tor_chat, \
    chat_ws_asyncio as as_ws_chat, chat_ws_twisted as tw_ws_chat, chat_ws_tornado as tor_ws_chat
from binder import main as bind

LAUNCH = {'tw_chat': tw_chat.main, 'as_chat': as_chat.main, 'tor_chat': tor_chat.main,
          'as_ws_chat': as_ws_chat.main, 'tor_ws_chat': tor_ws_chat.main, 'tw_ws_chat': tw_ws_chat.main,
          'bind': bind}
BIND = ['as', 'tor', 'tw', 'tcp_all', 'ws_all']
LAUNCH_KEYS = list(LAUNCH.keys())

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog == 'bind':
            try:
                bind_prog = sys.argv[2]
                if bind_prog in BIND:
                    LAUNCH[prog](bind_prog)
                else:
                    print(f'Unknown program! Available: {BIND}')
            except IndexError:
                print(f'Type program name for bind: {BIND}')
        elif prog in LAUNCH:
            LAUNCH[prog]()
        else:
            print('Unknown program!')
    else:
        print(f'Type program name: {LAUNCH_KEYS}')
