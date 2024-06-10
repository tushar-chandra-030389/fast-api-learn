import pytest
from app.calculation import addition, BankAccount, LowBalanceException
from termcolor import colored

# fixture
@pytest.fixture
def zero_bank_account():
    print(colored('\n) bank account', 'yellow'))
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50.55)

@pytest.mark.parametrize('x, y, result', [
    [1, 2, 3],
    [10, 3, 13]
])
def test_addition(x, y, result):
    assert addition(x, y) == result


def test_zero_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account(bank_account):
    assert bank_account.balance == 50.55

def test_bank_account_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 51.56

@pytest.mark.parametrize('dep, wit, bal', [
    [100, 10, 140.55],
    [100.5, 10.2, 140.85]
])
def test_bank_transaction(bank_account, dep, wit, bal):
    assert bank_account.balance == 50.55
    bank_account.deposit(dep)
    bank_account.withdraw(wit)
    assert bank_account.balance == bal

def test_exception_for_low_balance(bank_account):
    with pytest.raises(LowBalanceException):
        bank_account.withdraw(100)
