import time
from signal import SIGINT,signal

def signal_handler(sig_rcv, frame):

    fecha = time.strftime('%d/%m/%Y--%H:%M:%S')
    print('\nDetenida la integracion por interrupcion de teclado: ', fecha,'\n')
    exit(0)
def detencion_programa():
    signal(SIGINT, signal_handler)

