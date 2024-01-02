from unittest.mock import patch

from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from products import *
from logout import logout
from login import login
import pytest
import shutil
import os
import json
from unittest import mock

# Dummy user file
@pytest.fixture(scope='module')
def user_dummmy_file():
    shutil.copy('../../../pythonProject11/1DL610-HT23-coding-assignments-students/A1_unit_testing_students/users.json', 'dummy_users.json')
    print("Dummy file created")
    yield

    os.remove('dummy_users.json')
    print("Dummy file removed")


# Check user registration
@pytest.fixture
def check_user_registered():
    return {"username": "Simba", "password": "LionKing@^456", "wallet": 100}


# Open file stub
@pytest.fixture
def open_file_stub(monkeypatch, user_registered):
    read_data = json.dumps([user_registered])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))


# Magic mock JSON
@pytest.fixture
def json_dump_mocked(monkeypatch):
    mock_test = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_test)
    return mock_test


# Logout stub
@pytest.fixture
def stub_logout(mocker):
    return mocker.patch('logout.logout', return_value=True)


# Fake input
def fake_input(input_list):
    i = 0

    def _fake_input(foo_bar):
        nonlocal i
        mimicked_input = input_list[i]
        i += 1
        return mimicked_input

    return _fake_input


def test_login(capsys, monkeypatch):
    with mock.patch('builtins.input', side_effect=["Zara", "Rai#nbow2022"]):
        user = login()
    assert user["username"] == "Zara" and user["wallet"] == 110

def test_additem(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba","expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card]}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Backpack added to your cart." in captured.out

def test_removeitem(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba","expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card]}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1","l", "y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Backpack removed from your cart." in captured.out
def test_productoutofstock(stub_logout, capsys, monkeypatch):
     card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba", "expiry_date": "1/26"}
     login_details = {"username": "Simba", "wallet": 100, "cards": [card]}
     products = [Product("Banana", 15, 0)]
     monkeypatch.setattr("checkout_and_payment.products", products)
     monkeypatch.setattr("builtins.input", fake_input(["1", "c", "w", "l"]))
     checkoutAndPayment(login_details)
     captured = capsys.readouterr()
     assert "Sorry, Banana is out of stock." in captured.out

def test_paywithzerobalance(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba", "expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 0, "cards": [card]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l","y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "You don't have enough money to complete the purchase." in captured.out

def test_PaybyWallet(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba", "expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card]}
    products = [Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Payment using wallet successful." in captured.out
    assert "Thank you for your purchase, Simba! Your remaining balance is 99.5" in captured.out

def test_PaybyCard(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba","expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100,"cards":[card]}
    products = [Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","y","card","1","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Payment using card 1 successful." in captured.out


def test_MultipleCardpayment(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba","expiry_date": "1/26"}
    card_2 = {"card_number": "1234 5678 0000 0000", "holder_name": "Simba","expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100,"cards":[card,card_2]}
    products = [Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","y","card","1","6","c","y","card","2","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Payment using card 1 successful." in captured.out
    assert "Payment using card 2 successful." in captured.out

def test_mixedPayments(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba","expiry_date": "1/26"}
    card_2 = {"card_number": "1234 5678 0000 0000", "holder_name": "Simba","expiry_date": "1/26"}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    login_details = {"username": "Simba", "wallet": 200, "cards": [card, card_2]}
    monkeypatch.setattr("builtins.input", fake_input(["6","c","y","wallet","6","c","y","card","1","6","c","y","card","2","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "Payment using wallet successful." in captured.out
    assert "Payment using card 1 successful." in captured.out
    assert "Payment using card 2 successful." in captured.out

def test_log_out(capsys, monkeypatch):
    card = {"card_number": "1234 5678 1234 5678", "holder_name": "Simba", "expiry_date": "1/26"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card]}
    products = [Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "card","1", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    assert "You have been logged out" in captured.out



