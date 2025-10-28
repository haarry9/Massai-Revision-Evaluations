def withdraw_money(balance, amount):
    try:
        if amount > balance:
            raise ValueError("Amount exceeds balance")
    except ValueError as e:
        raise Exception("InsufficientFundsError")


try:
    withdraw_money(5000, 10000)
except Exception as e:
    print("Transaction failed:", e)
    