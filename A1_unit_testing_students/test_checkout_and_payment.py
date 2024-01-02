from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from logout import logout
import pytest
import shutil
import os
import json
from unittest import mock


# Dummy user file
@pytest.fixture(scope='module')
def user_dummmy_file():
    shutil.copy('users.json', 'dummy_users.json')
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


# Login confirmed
def logout_confirmed(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "You have been logged out for the system."
    assert output in out[:28]



# Test add item to cart
def test_add_item(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack added to your cart."
    assert output in out[30:]



# Test out of stock
def test_out_of_stock(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack is out of stock."
    assert output in out[30:]


# Test a product
def test_one_product(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    products = [Product("Ice cream", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Ice cream - $15.0 - Units: 1"
    assert expected_o in out[:31]


# Test several products
def test_several_products(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Banana - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]


# Test other letter
def test_other_letter(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", fake_input(["a", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Invalid input. Please try again."
    assert output in out



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