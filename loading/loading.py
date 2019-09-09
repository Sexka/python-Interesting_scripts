import  itertools
import sys
import time
flush=sys.stdout.flush
for i in  itertools.cycle("|/-\\"):
    print('\b'*len(i)+i,end='')
    flush()
    time.sleep(.1)