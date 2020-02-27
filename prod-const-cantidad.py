import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def productor(monitor):
    print("Voy a producir")
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)
              # agrega un ítem
            print(len(items))
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2)


class Consumidor(threading.Thread):
    def __init__(self, monitor,cuantos):
        super().__init__()
        self.monitor = monitor
        self.cuantos = cuantos

    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while not len(items) == self.cuantos:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                i = 0
                while i < self.cuantos:
                    x = items.pop(0)     # saca (consume) el primer ítem
                    logging.info(f'Consumi {x}')
                    i=i +1
            time.sleep(2)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# un thread que consume
cons1 = Consumidor(items_monit,2)
cons2 = Consumidor(items_monit,2)
cons1.start()
cons2.start()

# El productor
productor(items_monit)
