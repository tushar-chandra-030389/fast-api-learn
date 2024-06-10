def addition(a, b):
    return a + b

class LowBalanceException(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0.0):
        self.balance = round(starting_balance, 2)

    def deposit(self, amount):
        self.balance = round(self.balance + amount, 2)

    def withdraw(self, amount):
        if amount > self.balance:
            raise LowBalanceException('Insufficient balance')
        self.balance = round(self.balance  - amount, 2)

    def collect_interest(self):
        self.balance = round(self.balance * 1.02, 2)
