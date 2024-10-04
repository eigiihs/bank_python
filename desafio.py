def menu():
    menu = """\n
======= Bem-Vindo ao nosso Sistema Bancário =======

* Informe o tipo de operação que deseja realizar *
[1] - Depósito
[2] - Saque
[3] - Extrato
[4] - Novo Usuário
[5] - Nova Conta
[6] - Listar Usuários
[7] - Listar Contas
[0] - Sair
===================================================
=> """

    return input(menu)

def depositar(saldo, deposito, extrato, /):
    if deposito > 0:
        saldo += deposito
        extrato += f"Depósito:\tR$ {deposito:.2f}\n"
        print("\n == Depósito realizado com sucesso! ==")
    else: 
        print("\n ** Operação falhou! Digite um valor válido. **")

    return saldo, extrato

def sacar(*, saldo, saque, extrato, limite, n_saques, limite_saques):
    if saque > saldo:
        print("\n ** Operação falhou! Você não possui saldo suficiente. **")

    elif saque > limite:
        print("\n ** Operação falhou! O valor do saque excedeu o limite. **")

    elif n_saques >= limite_saques:
        print("\n ** Operação falhou! Você excedeu o número máximo de saques. **")

    elif saque > 0:
        saldo -= saque
        extrato += f"Saque:\t\tR$ {saque:.2f}\n"
        n_saques += 1
        print("\n == Saque realizado com sucesso! ==")
        
    else:
        print("\n ** Operação falhou! Digite um valor válido. **")

    return saldo, extrato

def exibe_extrato(saldo, /, *, extrato):
    print("\n---------- EXTRATO ----------")
    print("\nNão houve movimentações na conta." if extrato == '\n' else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("-----------------------------")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    usuario = encontrar_usuario(cpf, usuarios)

    if usuario:
        print("\n ** Já existe um usuário com esse CPF! **")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nasc, "endereco": endereco})

    print("\n == Usuário criado com sucesso! ==")

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    else:
        return None

def criar_conta(agencia, nro_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = encontrar_usuario(cpf, usuarios)

    if usuario:
        print("\n == Conta criada com sucesso! ==")
        return {"agencia": agencia, "numero_conta": nro_conta, "usuario": usuario}
    
    print("\n ** Usuário não encontrado! Não foi possível concluir a criação da conta. **")

def listar_usuarios(usuarios):
    for usuario in usuarios:
        linha = f""" 
        -------- USUÁRIOS ENCONTRADOS --------
        {usuario["nome"]}: \t{usuario["cpf"]}
        --------------------------------------
        """
        print(linha)
    
    print("\n ** Não foi encontrado nenhum usuário no sistema! **")

def listar_contas(contas): 
    for conta in contas:
        linha = f"""\n
        ---------- CONTA ENCONTRADA -----------
        Agência:\t{conta["agencia"]}
        C/C:\t\t{conta["numero_conta"]}
        Titular:\t{conta["usuario"]["nome"]}
        ---------------------------------------
        """
        print(linha)

    print("\n ** Não foi encontrada nenhuma conta no sistema! **")

def main():
    saldo = 0
    limite = 500
    extrato = "\n"
    n_saques = 0
    usuarios = []
    contas = []

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while True:

        option = menu()

        if option == '1':
            deposito = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, deposito, extrato)

        elif option == '2':
            saque = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                saque=saque, 
                extrato=extrato,
                limite=limite,
                n_saques=n_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif option == '3':
            exibe_extrato(saldo, extrato=extrato)

        elif option == '4':
            criar_usuario(usuarios)

        elif option == '5':
            nro_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, nro_conta, usuarios)

            if conta:
                contas.append(conta)

        elif option == '6':
            listar_usuarios(usuarios)
        
        elif option == '7':
            listar_contas(contas)
           
        elif option == '0':
            break

        else:
            print('Operação falhou! Selecione uma opção válida.')


main()