def menu():  
    return input("""

    [c] Cadastrar usuário
    [a] Criar conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [lu] Lista de usuários
    [lc] Lista de contas
    [q] Sair

    => """)


def cadastrar_usuario(usuarios):

    usuario = {}
    usuario["nome"] = input("Digite o nome do usuário: ")
    usuario["data_nascimento"] = input("Digite a data de nascimento do usuário: ")
    
    # valida CPF
    cpf = input("Digite o CPF do usuário (apenas números): ")
    while not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido! Digite novamente (11 números).")
        cpf = input("Digite o CPF do usuário (apenas números): ")

    # valida duplicidade
    cpf_existe = False
    for u in usuarios:
        if u["cpf"] == cpf:
            cpf_existe = True
    
    while cpf_existe:
        print("CPF já existe!")
        cpf = input("Digite o CPF novamente (apenas números): ")

        while not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido! Digite novamente (11 números).")
            cpf = input("Digite o CPF do usuário (apenas números): ")

        cpf_existe = False
        for u in usuarios:
            if u["cpf"] == cpf:
                cpf_existe = True

    usuario["cpf"] = cpf

    print("Digite o endereço do usuário")
    endereco = ( input("Logradouro: ") + ' - ' + 
                input("Número: ") + ' - ' +
                input("Bairro: ") + ' - ' +
                input("Cidade: ") + '/' +
                input("Estado (SIGLA): ")
    )
    usuario["endereco"] = endereco
    usuarios.append(usuario)

    return usuarios


def criar_conta(usuarios, contas):

    cpf = input("Digite o CPF do usuário (apenas números): ")

    for u in usuarios:
        if cpf == u["cpf"]:
            conta = {
                "agencia": "0001",
                "conta": 1 if len(contas) == 0 else contas[-1]["conta"] + 1,
                "cpf": cpf
            }
            contas.append(conta)
            return contas, True

    return contas, False


def sacar(*, saldo, limite, numero_saques, LIMITE_SAQUES, extrato):

    valor = float(input("Informe o valor do saque: "))

    if valor > saldo:
        print("Operação falhou! Saldo insuficiente.")

    elif valor > limite:
        print("Operação falhou! Valor excede o limite.")

    elif numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Limite de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Valor inválido!")

    return saldo, extrato, numero_saques


def depositar(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Valor inválido!")

    return saldo, extrato


def mostra_extrato(saldo, /, *, extrato, numero_saques):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}\nNúmero de saques: {numero_saques}")
    print("==========================================")


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "c":
            usuarios = cadastrar_usuario(usuarios)

        elif opcao == "a":
            contas, ok = criar_conta(usuarios, contas)
            print("Conta cadastrada!" if ok else "CPF não existe!")

        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                limite=limite,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES,
                extrato=extrato
            )

        elif opcao == "e":
            mostra_extrato(saldo, extrato=extrato, numero_saques=numero_saques)

        elif opcao == "lu":
            print(usuarios if usuarios else "Não há usuários cadastrados!")

        elif opcao == "lc":
            print(contas if contas else "Não há contas abertas!")

        elif opcao == "q":
            break

        else:
            print("Opção inválida.")


main()
