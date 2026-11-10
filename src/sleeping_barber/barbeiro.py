import threading
import time
import random
from barbearia import Barbearia

class Barbeiro(threading.Thread):
    def __init__(self, barbearia: Barbearia, tempo_corte: tuple):
        super().__init__()
        self.barbearia = barbearia
        self.tempo_corte = tempo_corte
        # daemon=True faz a thread encerrar quando o programa principal acabar
        self.daemon = True 

    def run(self):
        while True:
            # Interage com o monitor (Barbearia)
            self.barbearia.barbeiro_chama_proximo()
            self.cortar_cabelo()

    def cortar_cabelo(self):
        """Ação local do barbeiro, fora da zona crítica."""
        print("[Barbeiro] Cortando o cabelo...")
        time.sleep(random.uniform(*self.tempo_corte))
        print("[Barbeiro] Corte finalizado!\n")