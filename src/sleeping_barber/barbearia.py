import threading

class Barbearia:
    def __init__(self, num_cadeiras: int):
        self.num_cadeiras = num_cadeiras
        self.clientes_esperando = 0
        
        self.mutex = threading.Lock()
        self.sem_clientes = threading.Semaphore(0)
        self.sem_barbeiro = threading.Semaphore(0)

    def barbeiro_chama_proximo(self):
        """Chamado pelo Barbeiro: dorme se não há clientes, ou chama o próximo."""
        print("[Barbeiro] Sem clientes. Tirando um cochilo...")

        self.sem_clientes.acquire()
        
        self.mutex.acquire()
        self.clientes_esperando -= 1
        self.sem_barbeiro.release()
        self.mutex.release()

    def cliente_tenta_entrar(self, id_cliente: int) -> bool:
        """Chamado pelo Cliente: tenta sentar na recepção (Região Crítica)."""
        self.mutex.acquire()
        
        if self.clientes_esperando < self.num_cadeiras:
            self.clientes_esperando += 1
            print(f"[Cliente {id_cliente}] Entrou. (Espera: {self.clientes_esperando}/{self.num_cadeiras})")

            self.sem_clientes.release()
            self.mutex.release()
            return True
        else:
            self.mutex.release()
            print(f"[Cliente {id_cliente}] Barbearia LOTADA! Foi embora.")
            return False

    def cliente_senta_na_cadeira(self, id_cliente: int):
        """Chamado pelo Cliente: aguarda o barbeiro autorizar o corte."""
        self.sem_barbeiro.acquire()
        print(f"[Cliente {id_cliente}] Sentou na cadeira de corte.")