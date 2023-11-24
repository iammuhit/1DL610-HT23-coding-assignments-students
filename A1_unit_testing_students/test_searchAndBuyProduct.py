from unittest.mock import Mock,patch
from products import *
import pytest
import pytest_mock
from login import login
from _pytest import monkeypatch

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
def test_searchAndBuyProduct_successful_shopping_and_checkout(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', mock_input(['valid_user', 'password', 'all', 'y']))
    searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Search for products in inventory" in captured.out
    assert "Checkout" in captured.out
def test_searchAndBuyProduct_empty_inventory(capsys,mocker):
    mocker,patch('builtins.input', side_effect=['valid_user', 'password', 'all', 'y'])
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Search for products in inventory" in captured.out
    assert "No products available." in captured.out
def test_searchAndBuyProduct_invalid_login_max_retries(capsys,mocker):
    mocker.patch('builtins.input', side_effect=['invalid_user'] * 5)
    searchAndBuyProduct()
    captured = capsys.readouterr()

    assert "Either username or password were incorrect" in captured.out
    assert "Maximum login attempts reached. Exiting." in captured.out
def test_searchAndBuyProduct_search_cancel_shopping(capsys,mocker):
    mocker.patch('builtins.input', side_effect=['valid_user', 'password', 'all', 'n'])
    searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Shopping canceled." in captured.out
def test_searchAndBuyProduct_invalid_search_input(capsys,mocker):
    mocker.patch('builtins.input', side_effect=['valid_user', 'password', 'invalid_search', 'all', 'y'])
    searchAndBuyProduct()
    captured = capsys.readouterr()
    assert "Search for products in inventory" in captured.out
    assert "Invalid search input. Please try again." in captured.out