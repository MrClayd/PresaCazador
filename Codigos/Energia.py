import time

class Energia:
    def __init__(self, max_energia=10):
        self.max_energia = max_energia
        self.actual = max_energia
        self.ultimo_uso = time.time()

    def consumir(self, cantidad=1):
        if self.actual >= cantidad:
            self.actual -= cantidad
            self.ultimo_uso = time.time()
            return True
        return False

    def regenerar(self):
        # Regenera 1 punto cada 2 segundos si no está en máximo
        if self.actual < self.max_energia:
            if time.time() - self.ultimo_uso >= 2:
                self.actual += 1
                self.ultimo_uso = time.time()
                