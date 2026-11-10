import threading
from barbearia import Barbearia

class Cliente(threading.Thread):
    def __init__(self, id_cliente: int, barbearia: Barbearia):
        super().__init__()
        self.id_cliente = id_cliente
        self.barbearia = barbearia

    def run(self):
        conseguiu_entrar = self.barbearia.cliente_tenta_entrar(self.id_cliente)
        
        if conseguiu_entrar:
            self.barbearia.cliente_senta_na_cadeira(self.id_cliente)