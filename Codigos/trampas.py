import time

class Trampa:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.colocada_en = time.time()
        self.id = None
    def posicion(self):
        return self.i, self.j