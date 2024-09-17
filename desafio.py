menu = """ 

----- Bem-Vindo ao nosso Sistema Bancário -----

* Informe o tipo de operação que deseja realizar
    
[1] - Depósito
[2] - Saque
[3] - Extrato
[0] - Sair

-----------------------------------------------

-> """

saldo = 0
limite = 500
extrato = "\n"
n_saques = 0
LIMITE_SAQUES = 3


while True:

    option = input(menu)

    if option == '1':
        deposit = float(input("Informe o valor do depósito: "))

        if deposit > 0:
            saldo += deposit
            extrato += f"Depósito: R$ {deposit:.2f}\n"
            print("Depósito realizado com sucesso!")
        
        else: 
            print("Operação falhou! Digite um valor válido.")

    elif option == '2':
        saque = float(input("Informe o valor do saque: "))

        if saque > saldo:
            print("Operação falhou! Você não possui saldo suficiente.")

        elif saque > limite:
            print("Operação falhou! O valor do saque excedeu o limite.")

        elif n_saques >= LIMITE_SAQUES:
            print("Operação falhou! Você excedeu o número máximo de saques.")

        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            n_saques += 1
            print("Saque realizado com sucesso!")
        
        else:
            print("Operação falhou! Digite um valor válido.")

    elif option == '3':
        print("\n---------- EXTRATO ----------")
        print("\nNão houve movimentações na conta." if extrato == '\n' else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("-----------------------------")

    elif option == '0':
        break

    else:
        print('Operação falhou! Selecione uma opção válida.')
