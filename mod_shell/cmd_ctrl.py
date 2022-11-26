import time
from signal import SIGINT,signal

def signal_handler(sig_rcv, frame):

    date = time.strftime('%d/%m/%Y--%H:%M:%S')
    print('\nJOSHUA killed by keyboard interrupt: ', date,'\n')
    exit(0)
def detencion_programa():
    signal(SIGINT, signal_handler)

