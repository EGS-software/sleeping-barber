# Problema do Barbeiro Dorminhoco

Simulação em Python do problema clássico de sincronização conhecido como **Barbeiro Dorminhoco**. O projeto usa threads, um mutex e semáforos para coordenar a chegada de clientes, a sala de espera e o atendimento do barbeiro.

## O problema

Uma barbearia tem um barbeiro, uma cadeira de corte e um número limitado de cadeiras na sala de espera. Quando não há clientes, o barbeiro dorme. Ao chegar:

- Se o barbeiro estiver dormindo ou houver lugar na sala de espera, o cliente aguarda e será atendido.
- Se todas as cadeiras de espera estiverem ocupadas, o cliente vai embora.
- Depois de terminar um corte, o barbeiro chama outro cliente; se não houver ninguém, volta a dormir.

O desafio de concorrência é coordenar barbeiro e clientes sem que duas threads alterem simultaneamente o estado da sala de espera ou que o barbeiro fique esperando indefinidamente por um cliente que já chegou.

## Como a sincronização funciona

| Recurso | Função |
| --- | --- |
| `threading.Lock` (`mutex`) | Protege a contagem de clientes esperando e a decisão de aceitar ou recusar uma chegada. |
| `threading.Semaphore` (`sem_clientes`) | Notifica o barbeiro de que há um cliente para atender. Com valor inicial zero, faz o barbeiro esperar quando a barbearia está vazia. |
| `threading.Semaphore` (`sem_barbeiro`) | Faz o cliente aguardar até o barbeiro liberar o atendimento. |

O mutex é liberado antes de o barbeiro realizar o corte; assim, a operação demorada não bloqueia a entrada de outros clientes. Os semáforos coordenam a espera sem manter o mutex preso. Quando um cliente é aceito, ele incrementa a contagem de espera e sinaliza `sem_clientes`; depois do corte atual, o barbeiro consome esse sinal e libera `sem_barbeiro` para chamar um cliente. Assim, cliente e barbeiro não ficam presos esperando um pelo outro sem que exista um sinal para prosseguir. O programa demonstra essa solução sincronizada; ele **não** contém um modo que provoque deadlock intencionalmente.

## Estrutura do projeto

```text
src/
└── sleeping_barber/
    ├── main.py        # Configura e inicia a simulação
    ├── barbearia.py   # Estado compartilhado, mutex e semáforos
    ├── barbeiro.py    # Thread do barbeiro e duração do corte
    ├── cliente.py     # Thread de cada cliente
    └── __init__.py
```

## Requisitos

- Python 3
- Nenhuma dependência externa: a implementação usa apenas a biblioteca padrão do Python.

## Como executar

Na raiz do projeto, execute:

```powershell
python src\sleeping_barber\main.py
```

O programa inicia um barbeiro e cria dez clientes, com três cadeiras de espera. A saída informa quando clientes entram ou encontram a barbearia lotada e quando o barbeiro inicia e termina um corte.

### Cenários

Em `src/sleeping_barber/main.py`, a constante `SIMULAR_CAOS` seleciona o ritmo de chegada:

- `False` (padrão): chegadas mais espaçadas, representando um fluxo tranquilo.
- `True`: chegadas rápidas, aumentando a chance de lotação e de clientes irem embora.

Para experimentar o cenário de lotação, altere a constante para `True` e execute novamente. Esse cenário evidencia o limite de capacidade: quando todas as cadeiras de espera estão ocupadas, o próximo cliente é recusado e vai embora. Isso **não é deadlock**, pois esse cliente não fica bloqueado esperando por um recurso; ele encerra sua participação. Os clientes já aceitos continuam sendo atendidos, e o barbeiro pode esperar por novos clientes quando não há ninguém na fila.

**Deadlock** é uma situação em que uma ou mais threads ficam bloqueadas permanentemente porque cada uma espera por algo que outra precisa liberar — por exemplo, uma espera circular por locks. Na simulação, esperar pelo semáforo faz parte do funcionamento normal: o barbeiro espera quando não há clientes, e um cliente aceito espera até ser chamado. Essas esperas têm uma forma prevista de prosseguir: a chegada sinaliza `sem_clientes`, e o barbeiro sinaliza `sem_barbeiro` ao chamar o próximo cliente. Portanto, ver uma thread aguardando não significa, por si só, que há deadlock; é preciso verificar se existe uma dependência circular sem possibilidade de progresso.
