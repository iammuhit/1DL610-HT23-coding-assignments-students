import os
import shutil

from checkout_and_payment import *
import pytest

@pytest.fixture
def mock_print(mocker):
    return mocker.patch("builtins.print")
@pytest.fixture()
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

def test_empty_basket(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    checkout(user, cart)

    mock_print.assert_called_with("\nYour basket is empty. Please add items before checking out.")

def test_failed_checkout(mock_print):
    user = User(name="Daniel Galean", wallet=20)
    cart = ShoppingCart()
    cart.add_item(Product(name='TV', price=500, units=1))
    checkout(user, cart)

    mock_print.assert_called_with("Please try again!")

def test_failed_checkout2(mock_print):
    user = User(name="Daniel Galean", wallet=20)
    cart = ShoppingCart()
    cart.add_item(Product(name='Laptop', price=800, units=1))
    checkout(user, cart)

    mock_print.assert_called_with("Please try again!")

def test_checkout_success(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    cart.add_item(Product(name='Cookies', price=3, units=8))
    checkout(user, cart)

    mock_print.assert_called_with(f"Thank you for your purchase, Daniel Galean! Your remaining balance is 77.0")

def test_checkout_success2(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    cart.add_item(Product(name='Cookies', price=3, units=8))
    cart.add_item(Product(name='Broom', price=5, units=4))
    checkout(user, cart)

    mock_print.assert_called_with(f"Thank you for your purchase, Daniel Galean! Your remaining balance is 72.0")

def test_checkout_success_add_and_remove(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    product2 = Product(name='Broom', price=5, units=4)
    cart.add_item(product)
    cart.add_item(product2)
    cart.remove_item(product)
    checkout(user, cart)

    mock_print.assert_called_with(f"Thank you for your purchase, Daniel Galean! Your remaining balance is 75.0")

def test_checkout_success_add_and_remove2(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    product2 = Product(name='Broom', price=5, units=4)
    product3 = Product(name='Blender', price=30, units=1)
    cart.add_item(product)
    cart.add_item(product2)
    cart.add_item(product3)
    cart.remove_item(product3)
    checkout(user, cart)

    mock_print.assert_called_with(f"Thank you for your purchase, Daniel Galean! Your remaining balance is 72.0")


def test_checkout_product_units_update(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)
    checkout(user, cart)

    assert product.units == 7

def test_checkout_product_units_update2(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    product2 = Product(name='Broom', price=5, units=4)
    cart.add_item(product)
    cart.add_item(product2)
    checkout(user, cart)

    assert product.units == 7
    assert product2.units == 3

def test_checkout_user_wallet_updated(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)
    checkout(user, cart)

    assert user.wallet == 77