import textwrap

def depositar(valor, saldo, extrato, /):
    """
    Processa um depósito. Apenas manipula os dados e retorna o novo estado.
    Não imprime nada além de mensagens de erro.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n" 
        sucesso = True
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        sucesso = False
    
    return saldo, extrato, sucesso

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Função para sacar dinheiro.
    Recebe todos os parâmetros por nome (*).
    Verifica as regras de negócio e retorna o novo estado.
    """

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print(f"\n@@@ Operação falhou! O valor do saque (R$ {valor:.2f}) excede o limite de R$ {limite:.2f}. @@@")
    elif numero_saques >= limite_saques:
        print(f"\n@@@ Operação falhou! Número máximo de {limite_saques} saques diários foi excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    """
    Função dedicada a EXIBIR o extrato de forma formatada.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato.strip())
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
        }

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in contas:
        usuario = conta["usuario"]
        print(f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{usuario['nome']}
        """)

def menu():
    frase_prompt = "\nPor favor, digite a opção desejada => "
    return input(textwrap.dedent(f"""
        ============= MENU =============

        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nu]\tNovo usuário
        [nc]\tNova conta
        [lc]\tListar contas
        [q]\tSair

        ================================
    {frase_prompt}"""))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu().lower().strip()

        match opcao:
            case 'd':
                try:
                    valor = float(input("Informe o valor do depósito: "))
                    saldo, extrato, sucesso = depositar(valor, saldo, extrato)
                    
                    if sucesso:
                        print("\n=== Depósito realizado com sucesso! ===")
                
                except ValueError:
                    print("\n@@@ Operação falhou! Por favor, informe um número válido. @@@")

            case 's':
                try:
                    valor = float(input("Informe o valor do saque: "))
                    saldo, extrato, numero_saques = sacar(
                        saldo=saldo,
                        valor=valor,
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES
                    )
                except ValueError:
                    print("\n@@@ Operação falhou! Por favor, informe um número válido. @@@")

            case 'e':
                mostrar_extrato(saldo, extrato=extrato)
            case 'nu':
                criar_usuario(usuarios)
            case 'nc':
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
            case 'lc':
                listar_contas(contas)
            case 'q':
                print("\nObrigado por usar nosso sistema! Saindo...")
                break

            case _:
                print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()