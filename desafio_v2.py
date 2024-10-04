from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

# Classe base de Cliente
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

# Herança de Cliente, específica para Pessoa Física 
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nasc):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = data_nasc

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nasc(self):
        return self._data_nasc
    
    # Retorna uma representação string do cliente
    def __str__(self):
        return f"""\
        Nome:\t\t{self.nome}
        CPF:\t\t{self.cpf}
        Nascimento:\t{self.data_nasc}
        Endereço:\t{self.endereco}
        """
    
# Classe base de Contas
class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("\n ** Operação falhou! Você não possui saldo suficiente. **")

        elif valor > 0:
            self._saldo -= valor
            print("\n == Saque realizado com sucesso! ==")
            return True
        
        else: 
            print("\n ** Operação falhou! Digite um valor válido. **")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n == Depósito realizado com sucesso! ==")
            return True
        else: 
            print("\n ** Operação falhou! Digite um valor válido. **")
            return False

# Herança de Conta, específica para Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        nro_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        limite = self._limite
        limite_saques = self._limite_saques

        if valor > limite:
            print("\n ** Operação falhou! O valor do saque excedeu o limite. **")
        
        elif nro_saques > limite_saques:
            print("\n ** Operação falhou! Você excedeu o número máximo de saques. **")

        else:
            return super().sacar(valor)
        
        return False
    
    # Retorna uma representação string da conta
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """

# Classe que aramzena o histórico de transações de uma conta
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })

# Classe abstrata para transações (depósito e saque)
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
 
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe que representa um Depósito, 'filha' da classe abstrata
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.depositar(self.valor)

        if transacao: 
            conta.historico.adicionar_transacao(self)

# Classe que representa um Saque, 'filha' da classe abstrata
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.sacar(self.valor)

        if transacao: 
            conta.historico.adicionar_transacao(self)

# Menu de opções do usuário
def menu():
    menu = """\n
======= Bem-Vindo ao nosso Sistema Bancário =======

* Informe o tipo de operação que deseja realizar *
[1] - Depósito
[2] - Saque
[3] - Extrato
[4] - Novo Cliente
[5] - Nova Conta
[6] - Listar Clientes
[7] - Listar Contas
[0] - Sair
===================================================
=> """

    return input(menu)

# Função: encontra um cliente apartir do CPF
def encontrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função: encontra a primeira conta de um cliente
def encontrar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n ** O cliente não possui conta! **")
        return
    
    # FIXME: não permite o cliente escolher a conta 
    return cliente.contas[0]

# Função: realiza um depósito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função: realiza um saque
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função: exibe o extrato de uma conta, apartir do CPF do cliente
def exibe_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return
    
    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============= EXTRATO =============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\nNão houve movimentações na conta."

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("====================================")

# Função: cria um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente:
        print("\n ** Já existe um cliente com esse CPF! **")
        return
    
    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nasc=data_nasc)

    clientes.append(cliente)

    print("\n == Cliente criado com sucesso! ==")

# Função: cria uma nova conta para um cliente específico, apartir do CPF
def criar_conta(nro_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=nro_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n == Conta criada com sucesso! ==")

# Função: lista todos os clientes
def listar_clientes(clientes): 
    for cliente in clientes:
        print("=" * 40)
        print(str(cliente))

# Função: lista todas as contas 
def listar_contas(contas): 
    for conta in contas:
        print("=" * 40)
        print(str(conta))

# Inicia o sistema bancário
def main():
    clientes = []
    contas = []

    while True:

        option = menu()

        if option == '1':
            depositar(clientes)

        elif option == '2':
            sacar(clientes)

        elif option == '3':
            exibe_extrato(clientes)

        elif option == '4':
            criar_cliente(clientes)

        elif option == '5':
            nro_conta = len(contas) + 1
            criar_conta(nro_conta, clientes, contas)

        elif option == '6':
            listar_clientes(clientes)
        
        elif option == '7':
            listar_contas(contas)
           
        elif option == '0':
            break

        else:
            print('Operação falhou! Selecione uma opção válida.')


main()