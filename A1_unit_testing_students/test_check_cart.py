from checkout_and_payment import *
import pytest

@pytest.fixture
def mock_input(mocker):
    return mocker.patch("builtins.input", side_effect=["y"])

@pytest.fixture
def mock_input2(mocker):
    return mocker.patch("builtins.input", side_effect=["invalid"])

def test_check_cart_checkout(mock_input):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_continue_shopping(mock_input):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_checkout_no_items(mock_input):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_continue_shopping_no_items(mock_input):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_checkout_invalid_input(mock_input2):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is False

def test_check_cart_continue_shopping_invalid_input(mock_input2):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is False

def test_chech_cart_checkout_lower_case(mock_input, mocker):
    mocker.patch("builtins.input", side_effect=["y"])
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is None

def test_chech_cart_continue_shopping_lower_case(mock_input, mocker):
    mocker.patch("builtins.input", side_effect=["n"])
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is False

def test_chech_cart_checkout_upper_case(mock_input, mocker):
    mocker.patch("builtins.input", side_effect=["Y"])
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is None

def test_chech_cart_continue_shopping_upper_case(mock_input, mocker):
    mocker.patch("builtins.input", side_effect=["N"])
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is False