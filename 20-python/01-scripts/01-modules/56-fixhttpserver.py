# http.server print and log lag and ctrl+c lag
import sys

# 1. ctrl+c exit immediately
import signal
signal.signal(signal.SIGINT, lambda s, f: (print('KeyboardInterrupt by Ctrl+C!'), sys.exit(0)))

# 2. print immediately
_print = print


def print(*args, **kwargs):
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    _print(*args, **kwargs)


# 3. change dir
'''
parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
'''
