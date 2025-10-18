import textwrap

# --- FUNÇÕES DE OPERAÇÃO (Apenas manipulam dados) ---

def depositar(valor, saldo, extrato, /):
    """
    Processa um depósito. Apenas manipula os dados e retorna o novo estado.
    Não imprime nada além de mensagens de erro.
    """
    if valor > 0:
        saldo += valor
        # O extrato agora só registra a MOVIMENTAÇÃO
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

# --- FUNÇÕES DE EXIBIÇÃO (Apenas mostram coisas na tela) ---
def mostrar_extrato(saldo, /, *, extrato):
    """
    Função dedicada a EXIBIR o extrato de forma formatada.
    """
    print("\n================ EXTRATO ================")
    # Se a string 'extrato' estiver vazia, mostra a mensagem.
    # Senão, imprime o histórico de transações.
    print("Não foram realizadas movimentações." if not extrato else extrato.strip())
    
    # Exibe o saldo final, bem alinhado
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def menu():
    frase_prompt = "\nPor favor, digite a opção desejada => "
    return input(textwrap.dedent(f"""
        ============= MENU =============

        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [q]\tSair

        ================================
    {frase_prompt}"""))

# --- FUNÇÃO PRINCIPAL (A Orquestradora) ---

def main():
    # Constantes e variáveis de estado
    LIMITE_SAQUES = 3
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    while True:
        # Padroniza a entrada do usuário
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
                # A única responsabilidade do 'e' é chamar a função de exibição
                mostrar_extrato(saldo, extrato=extrato)

            case 'q':
                print("\nObrigado por usar nosso sistema! Saindo...")
                break

            case _:
                print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()