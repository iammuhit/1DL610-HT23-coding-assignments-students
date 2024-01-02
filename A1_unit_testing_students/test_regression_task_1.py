import pytest
import os
import shutil
import csv
from unittest.mock import mock_open, ANY, patch
from login import login
from logout import logout
from checkout_and_payment import *
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

# Helper function to create a CSV file
def create_csv_helper(tmp_path, filename, rows):
    file_path = tmp_path / filename
    file_path.write_text('\n'.join(rows))
    return file_path


# TEST CHECK_CART
@pytest.fixture
def mock_input1(mocker):
    return mocker.patch("builtins.input", side_effect=["y"])

@pytest.fixture
def mock_input2(mocker):
    return mocker.patch("builtins.input", side_effect=["invalid"])

def test_check_cart_checkout(mock_input1):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_continue_shopping(mock_input1):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_checkout_no_items(mock_input1):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()

    result = check_cart(user, cart)
    assert result is None

def test_check_cart_continue_shopping_no_items(mock_input1):
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

#TEST CHECKOUT
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

def test_checkout_success(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    cart.add_item(Product(name='Cookies', price=3, units=8))
    checkout(user, cart)

    mock_print.assert_called_with(f"Thank you for your purchase, Daniel Galean! Your remaining balance is 77.0")

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

def test_checkout_product_units_update(mock_print):
    user = User(name="Daniel Galean", wallet=80)
    cart = ShoppingCart()
    product = Product(name='Cookies', price=3, units=8)
    cart.add_item(product)
    checkout(user, cart)

    assert product.units == 7

#TEST LOAD_PRODUCT_FROM_CSV
@pytest.fixture
def mock_open(mocker):
    return mocker.patch("builtins.open")

@pytest.fixture()
def copy_csv_file():
    shutil.copyfile('products.csv', 'copy_products.csv')
    yield 'copy_products.csv'
    os.remove('copy_products.csv')

def test_header(copy_csv_file):
    with open('copy_products.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        assert header == ['Product', 'Price', 'Units']

def test_int_input(mock_open):
    mock_open.side_effect = TypeError("Int incorrect type")

    with pytest.raises(TypeError, match="Int incorrect type"):
        load_products_from_csv(1)

def test_no_input():
    with pytest.raises(Exception):
        load_products_from_csv()

def test_invalid_file(copy_csv_file):
    with pytest.raises(Exception):
        load_products_from_csv('products.sql')

def test_loaded_products_not_empty_file(copy_csv_file):
    products = load_products_from_csv('copy_products.csv')

    assert len(products) != 0

#TEST LOGIN
mock_data_log = """
    [
        {
        "username": "valid_username", 
        "password": "Password!", 
        "wallet": 100
        }
    ]
"""


@pytest.fixture
def mock_file_open_log(mocker):
    return mocker.patch("builtins.open", new_callable=mock_open, read_data=mock_data_log)


@pytest.fixture
def mock_input_log(mocker):
    return mocker.patch("builtins.input")


@pytest.fixture
def mock_print_log(mocker):
    return mocker.patch("builtins.print")


@pytest.fixture
def mock_json_log(mocker):
    return mocker.patch("json.load", return_value=[{
        "username": "valid_username",
        "password": "Password!",
        "wallet": 100
    }])


@pytest.fixture
def mock_json_dump_log(mocker):
    return mocker.patch("json.dump", return_value=None)


@pytest.fixture
def mock_is_valid_password_log(mocker):
    return mocker.patch("login.is_valid_password", return_value=True)


def test_login_exising_username_correct_password(mock_print_log, mock_file_open_log, mock_json_log, mock_input_log):
    """
    Test that login returns an existing account when the user exists and the password is correct
    """
    mock_input.side_effect_log = ["valid_username", "Password!"]

    result = login()

    assert result["username"] == "valid_username"
    assert result["wallet"] == 100


def test_login_exising_username_incorrect_password(mock_print_log, mock_file_open_log, mock_json_log, mock_input_log):
    """
    Test that login returns None when the user exists and the password is incorrect
    """
    mock_input.side_effect_log = ["valid_username", "WrongPassword!"]

    result = login()

    assert result is None


def test_login_nonexistent_username_no_register(mock_input_log, mock_json_log, mock_file_open_log):
    """
    Test that login returns None when the user does not exist and does not want to register
    """

    mock_input.side_effect_log = ["invalid_username", "n"]

    result = login()
    assert result is None


def test_login_nonexistent_username_register(mock_file_open_log, mock_jso_log_log, mock_json_dump_log, mock_input_log,
                                             mock_is_valid_password_log, mock_print_log):
    """
    Test that login returns a new account when the user does not exist and wants to register
    """
    mock_input.side_effect_log = ["invalid_username", "y", "Password!"]

    result = login()

    assert result["username"] == "invalid_username"
    assert result["wallet"] == 0

    mock_json_dump_log.assert_called_once_with([
        {
            "username": "valid_username",
            "password": "Password!",
            "wallet": 100
        },
        {
            "username": "invalid_username",
            "password": "Password!",
            "wallet": 0
        },
    ], ANY, indent=ANY)


def test_login_nonexistent_username_register_invalid_password(mock_print_log, mock_file_open_log, mock_json_dump_log,
                                                              mock_json_log, mock_input_log, mock_is_valid_password_log):
    """
    Test that login returns a new account when the user does not exist and wants to register,
    but the password is invalid the first time
    """
    mock_input.side_effect_log = ["invalid_username", "y", "invalid", "Password!"]
    mock_is_valid_password_log.side_effect = [False, True]

    result = login()

    assert result["username"] == "invalid_username"
    assert result["wallet"] == 0

    mock_json_dump_log.assert_called_once_with([
        {
            "username": "valid_username",
            "password": "Password!",
            "wallet": 100
        },
        {
            "username": "invalid_username",
            "password": "Password!",
            "wallet": 0
        },
    ], ANY, indent=ANY)

       
#TEST LOGOUT
@pytest.fixture
def mock_input_logo(mocker):
    return mocker.patch("builtins.input")

@pytest.fixture
def mock_print_logo(mocker):
    return mocker.patch("builtins.print")

def test_logout_empty_cart():
    """
    Test that logout returns True when the cart is empty
    """

    cart = ShoppingCart()
    assert logout(cart) is True


def test_logout_not_empty_cart_yes(mock_input_logo, mock_print_logo):
    """
    Test that logout returns True when the cart is not empty and the user confirms
    """
    mock_input.side_effect = ["y"]

    cart = ShoppingCart()
    product = Product("item", 10, 1)
    cart.add_item(product)

    assert len(cart.items) == 1
    assert logout(cart) is True
    assert len(cart.items) == 0


def test_logout_not_empty_cart_no(mock_input_logo, mock_print_logo):
    """
    Test that logout returns False when the cart is not empty and the user does not confirm
    """
    mock_input.side_effect = ["n"]

    cart = ShoppingCart()
    product = Product("item", 10, 1)
    cart.add_item(product)

    assert logout(cart) is False
    assert len(cart.items) == 1


#TEST DISPLAY_CSV_AS_TABLE

def test_display_csv_as_table_valid_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="price,units,product"))
    display_csv_as_table("valid.csv")
    captured = capsys.readouterr()
    expected_output =("Valid csv")
    assert captured.out == expected_output

def test_display_csv_as_table_with_spaces(capsys,mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Bell Pepper, 1.2 , 8"))
    display_csv_as_table("csv_with_spaces.csv")
    captured = capsys.readouterr()
    expected_output =("['Bell Pepper', ' 1.2 ', ' 8']\n")
    assert captured.out == expected_output

def test_display_csv_as_table_with_newline_characters(capsys,mocker):
     mocker.patch("builtins.open", mocker.mock_open(read_data="price,units,product\n7,4,Chicken \nBreast"))
     display_csv_as_table("csv_with_newline_characters.csv")
     captured = capsys.readouterr()
     expected_output = ("""['price,units,product'
                               '7,4,Chicken'
                                'Breast']""")
     assert captured.out == expected_output

def test_display_csv_as_table_with_empty_values(capsys, mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Cucumber,Ice cream,30,"))
    display_csv_as_table("csv_with_empty_values.csv")
    captured = capsys.readouterr()
    expected_output = ("[Cucumber,1, Ice cream,,]")
    assert captured.out == expected_output

def test_display_csv_as_table_with_unicode_characters(capsys,mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Water 💦 ,1,20,Broom🧹,5,4"))
    display_csv_as_table("csv_with_unicode_characters.csv")
    captured = capsys.readouterr()
    expected_output = ("['Water 💦 ', '1', '20', 'Broom🧹', '5', '4']\n")
    assert captured.out == expected_output

# TEST DISPLAY_FILTERED_TABLE

def test_display_filtered_table_simple(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,5"))
    display_filtered_table('test.csv', 'Apple')
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price', 'unit']\n['Apple', '1', '5']\n"
    assert captured.out == expected_output

def test_display_filtered_table_empty(capsys,mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="Product,Price,unit\nApple,1,5"))
    display_filtered_table('test.csv', 'Banana')
    captured = capsys.readouterr()
    expected_output = "[table empty]"
    assert captured.out == expected_output

def test_display_filtered_table_product_not_found(capsys,mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="Product,Price,unit\nApple,1,5"))
    display_filtered_table('test.csv', 'Banana')
    captured = capsys.readouterr()
    expected_output = "Product not found"
    assert captured.out == expected_output
def test_display_filtered_table_case_insensitive(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nBanana,1,5\nApple,1,0"))
    display_filtered_table('test.csv', 'BaNaNa')
    captured = capsys.readouterr()
    expected_output = "Product,Price,unit\nBanana,1,5"
    assert captured.out == expected_output
def test_display_filtered_table_multiple_matches(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,0\nBanana,1,5\nOrange,1,25\nBanana,1,5\n"))
    display_filtered_table('test.csv', 'Banana')
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price', 'unit']\n['Banana', '1', '5']\n['Banana', '1', '5']\n"
    assert captured.out == expected_output

# TEST SEARCHANDBUYPRODUCT

@pytest.fixture
def mocker_login(mocker):
    return mocker.patch('products.login')
@pytest.fixture
def mocker_display_csv(mocker):
    return mocker.patch('products.display_csv_as_table')

@pytest.fixture
def mocker_display_filtered(mocker):
    return mocker.patch('products.display_filtered_table')

def mock_input(mock_values):
    def input(prompt):
        return mock_values.pop(0)
    return input

def test_searchAndBuyProduct_successful_login_and_search(monkeypatch, capsys,mocker,mocker_login,mocker_display_csv,mocker_display_filtered):
    monkeypatch.setattr('builtins.input', mock_input(['valid_user', 'password', 'all', 'y']))
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Successfully logged in" in captured.out
    assert "Search for products in inventory" in captured.out

def test_searchAndBuyProduct_login_and_retry(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', mock_input(['invalid_user', 'wrong_password', 'valid_user', 'password', 'all', 'y']))
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Either username or password were incorrect" in captured.out
    assert "Successfully logged in" in captured.out

def test_searchAndBuyProduct_search_all_products(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', mock_input(['valid_user', 'password', 'all', 'y']))
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Search for products in inventory" in captured.out
    assert "Products" in captured.out
def test_searchAndBuyProduct_search_specific_product(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', mock_input(['valid_user', 'password', 'specific_product', 'y']))
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Search for products in inventory" in captured.out
    assert "Product 1" in captured.out

def test_searchAndBuyProduct_invalid_ready_to_shop_input(monkeypatch, capsys):
        monkeypatch.setattr('builtins.input', mock_input(['valid_user', 'password', 'all', 'invalid_input', 'y']))
        searchAndBuyProduct()
        captured = capsys.readouterr()

        assert "Ready to shop?" in captured.out
        assert "Invalid input" in captured.out


#NEW IMPLEMENTATION: STRENGTHENING THE PRODUCT SYSTEM

def test_query_item_empty_cart():
    shopCart = ShoppingCart()
    assert query_item_in_cart(shopCart, "product0") == None

def test_query_item_multiple_items_match_and_no_match():
    cart = ShoppingCart()
    product0 = Product("product0", 10, 5)
    product1 = Product("product1", 10, 5)
    product2 = Product("product2", 10, 5)
    cart.add_item(product0)
    cart.add_item(product1)
    cart.add_item(product2)
    assert query_item_in_cart(cart, "product0") == product0
    assert query_item_in_cart(cart, "product1") == product1
    assert query_item_in_cart(cart, "product2") == product2
    assert query_item_in_cart(cart, "product3") == None
    assert query_item_in_cart(cart, "product7") == None
    assert query_item_in_cart(cart, "product47") == None

def test_remove_item_multiple_items_match_and_no_match(mocker):
    cart = ShoppingCart()
    product0 = Product("product0", 10, 5)
    product1 = Product("product1", 10, 5)
    product2 = Product("product2", 10, 5)

    cart.add_item(product0)
    cart.add_item(product1)
    cart.add_item(product2)

    mocker.patch('checkout_and_payment.query_item_in_cart', side_effect=[product0, product1, product2, None, None, None])

    assert remove_item_from_cart(cart, "product0") == True
    assert remove_item_from_cart(cart, "product1") == True
    assert remove_item_from_cart(cart, "product2") == True
    assert remove_item_from_cart(cart, "product3") == False
    assert remove_item_from_cart(cart, "product7") == False
    assert remove_item_from_cart(cart, "product47") == False

# SMOKE TESTING
def test_login_exising_username_correct_password(mock_print_log, mock_file_open_log, mock_json_log, mock_input_log):
    """
    Test that login returns an existing account when the user exists and the password is correct
    """
    mock_input.side_effect_log = ["valid_username", "Password!"]

    result = login()

    assert result["username"] == "valid_username"
    assert result["wallet"] == 100

def test_logout_empty_cart():
    """
    Test that logout returns True when the cart is empty
    """

    cart = ShoppingCart()
    assert logout(cart) is True

def test_login_nonexistent_username_register(mock_file_open_log, mock_jso_log_log, mock_json_dump_log, mock_input_log,
                                             mock_is_valid_password_log, mock_print_log):
    """
    Test that login returns a new account when the user does not exist and wants to register
    """
    mock_input.side_effect_log = ["invalid_username", "y", "Password!"]

    result = login()

    assert result["username"] == "invalid_username"
    assert result["wallet"] == 0

    mock_json_dump_log.assert_called_once_with([
        {
            "username": "valid_username",
            "password": "Password!",
            "wallet": 100
        },
        {
            "username": "invalid_username",
            "password": "Password!",
            "wallet": 0
        },
    ], ANY, indent=ANY)

def test_login_exising_username_correct_password(mock_print_log, mock_file_open_log, mock_json_log, mock_input_log):
    """
    Test that login returns an existing account when the user exists and the password is correct
    """
    mock_input.side_effect_log = ["valid_username", "Password!"]

    result = login()

    assert result["username"] == "valid_username"
    assert result["wallet"] == 100

def test_remove_item_one_item_no_match(mocker):
    cart = ShoppingCart()
    cart.add_item(Product("product0", 10, 5))
    mocker.patch('checkout_and_payment.query_item_in_cart', return_value=None)
    assert remove_item_from_cart(cart, "product8") == False


def test_remove_item_empty_cart(mocker):
    cart = ShoppingCart()
    mocker.patch('checkout_and_payment.query_item_in_cart', return_value=None)
    assert remove_item_from_cart(cart, "product0") == False

def test_remove_item_multiple_items_match_and_no_match(mocker):
    cart = ShoppingCart()
    product0 = Product("product0", 10, 5)
    product1 = Product("product1", 10, 5)
    product2 = Product("product2", 10, 5)

    cart.add_item(product0)
    cart.add_item(product1)
    cart.add_item(product2)

    mocker.patch('checkout_and_payment.query_item_in_cart', side_effect=[product0, product1, product2, None, None, None])

    assert remove_item_from_cart(cart, "product0") == True
    assert remove_item_from_cart(cart, "product1") == True
    assert remove_item_from_cart(cart, "product2") == True
    assert remove_item_from_cart(cart, "product3") == False
    assert remove_item_from_cart(cart, "product11") == False
    assert remove_item_from_cart(cart, "product22") == False

def test_remove_item_one_item_no_match(mocker):
    cart = ShoppingCart()
    cart.add_item(Product("product0", 10, 5))
    mocker.patch('checkout_and_payment.query_item_in_cart', return_value=None)
    assert remove_item_from_cart(cart, "product1") == False

def test_remove_item_twice(mocker):
    cart = ShoppingCart()
    product = Product("product0", 10, 5)
    cart.add_item(product)
    mocker.patch('checkout_and_payment.query_item_in_cart', side_effect=[product, None])
    assert remove_item_from_cart(cart, "product0") == True
    assert remove_item_from_cart(cart, "product0") == False

def test_logout_not_empty_cart_no(mock_input_logo, mock_print_logo):
    """
    Test that logout returns False when the cart is not empty and the user does not confirm
    """
    mock_input.side_effect = ["n"]

    cart = ShoppingCart()
    product = Product("item", 10, 1)
    cart.add_item(product)

    assert logout(cart) is False
    assert len(cart.items) == 1
