MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

WITHDRAW_LIMIT = 50000  # R$ 500,00 in cents. Working with cents to avoid floating point issues
DAILY_WITHDRAW_LIMIT = 3


def format_amount(amount_in_cents: int) -> str: #Format amount in cents to reais with two decimal places
    return f"R$ {amount_in_cents / 100:.2f}"


def read_amount_in_cents(message: str) -> int: #Read a value in reais from user input and convert to cents."""
    entry = input(message).replace(",", ".")  # converts comma to dot
    try:
        amount_reais = float(entry)
        return int(round(amount_reais * 100))
    except ValueError:
        print("Entrada inválida! Digite um número válido.")
        return 0


def deposit(balance, transactions):
    amount = read_amount_in_cents("Informe o valor do depósito (em reais): ")
    if amount > 0:
        balance += amount
        transactions.append(("Depósito", amount))
        print(f"✅ Depósito de {format_amount(amount)} realizado com sucesso!")
    else:
        print("❌ Operação falhou! O valor informado é inválido.")
    return balance


def withdraw(balance, transactions, withdraw_count):
    print("\n------ INFORMAÇÕES DE SAQUE ------")
    print(f"💰 Saldo disponível: {format_amount(balance)}")
    print(f"🔒 Limite por saque: {format_amount(WITHDRAW_LIMIT)}")
    print(f"🧾 Saques restantes hoje: {DAILY_WITHDRAW_LIMIT - withdraw_count}")
    print("---------------------------------")

    amount = read_amount_in_cents("Informe o valor do saque (em reais): ")

    if amount <= 0:
        print("❌ Operação falhou! O valor informado é inválido.")
    elif amount > balance:
        print("❌ Operação falhou! Você não tem saldo suficiente.")
    elif amount > WITHDRAW_LIMIT:
        print("❌ Operação falhou! O valor do saque excede o limite por operação.")
    elif withdraw_count >= DAILY_WITHDRAW_LIMIT:
        print("❌ Operação falhou! Número máximo de saques diários excedido.")
    else:
        balance -= amount
        transactions.append(("Saque", amount))
        withdraw_count += 1
        print(f"✅ Saque de {format_amount(amount)} realizado com sucesso!")

    return balance, withdraw_count


def show_statement(balance, transactions):
    print("\n================ EXTRATO ================")
    if not transactions:
        print("Não foram realizadas movimentações.")
    else:
        for t_type, amount in transactions:
            print(f"{t_type}: {format_amount(amount)}")
    print(f"\nSaldo atual: {format_amount(balance)}")
    print("==========================================")


def main():
    balance = 0
    withdraw_count = 0
    transactions = []

    while True:
        option = input(MENU).lower()

        if option == "d":
            balance = deposit(balance, transactions)
        elif option == "s":
            balance, withdraw_count = withdraw(balance, transactions, withdraw_count)
        elif option == "e":
            show_statement(balance, transactions)
        elif option == "q":
            print("👋 Obrigado por usar nosso sistema bancário. Até logo!")
            break
        else:
            print("⚠️ Operação inválida, por favor selecione novamente.")


if __name__ == "__main__":
    main()