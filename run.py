import twisted_simple_chat as tw_chat
import asyncio_simple_chat.server as as_chat
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prog = sys.argv[1]
        if prog == 'tw_chat' or prog == '1':
            tw_chat.main()
        elif prog == 'as_chat' or prog == '2':
            as_chat.main()
        else:
            print('Unknown program!')
    else:
        print("Type program name: 'tw_chat' or 'as_chat'")
