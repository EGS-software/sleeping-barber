import time
import random
from barbearia import Barbearia
from barbeiro import Barbeiro
from cliente import Cliente

SIMULAR_CAOS = False 

def main():
    cenario = "CAOS (Filas lotadas)" if SIMULAR_CAOS else "TRANQUILO (Fluxo ideal)"
    print(f"--- Iniciando Simulação | Cenário: {cenario} ---\n")
    
    barbearia = Barbearia(num_cadeiras=3)
    
    barbeiro = Barbeiro(barbearia=barbearia, tempo_corte=(0.5, 1.5))
    barbeiro.start()
    
    intervalo_chegada = (0.1, 0.3) if SIMULAR_CAOS else (1.0, 3.0)
    
    clientes = []
    for i in range(1, 11):
        cliente = Cliente(id_cliente=i, barbearia=barbearia)
        clientes.append(cliente)
        cliente.start()
        
        time.sleep(random.uniform(*intervalo_chegada))
        
    for c in clientes:
        c.join()
        
    time.sleep(2)
    print("\n--- Expediente encerrado! ---")

if __name__ == "__main__":
    main()