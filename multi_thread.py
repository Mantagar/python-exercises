from threading import Thread
import time
from multiprocessing import Process

def print_text_every_sec(text, repeat):
  for i in range(repeat):
    time.sleep(1.0)
    print("{}: {}".format(text, i))

t1 = Thread(target=print_text_every_sec, args=("T_1", 30))
t2 = Thread(target=print_text_every_sec, args=("T_2", 30))

p1 = Process(target=print_text_every_sec, args=("P_1", 30))
p2 = Process(target=print_text_every_sec, args=("P_2", 30))

t1.start()
t2.start()

p1.start()
p2.start()

t1.join()
t2.join()

p1.join()
p2.join()
