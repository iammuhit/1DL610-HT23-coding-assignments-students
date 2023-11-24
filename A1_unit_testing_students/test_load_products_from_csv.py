import os
import shutil

from checkout_and_payment import *
import pytest

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

def test_float_input():
    with pytest.raises(Exception):
        load_products_from_csv(0.5)

def test_string_input():
    with pytest.raises(Exception):
        load_products_from_csv("string")

def test_no_input():
    with pytest.raises(Exception):
        load_products_from_csv()
def test_invalid_file(copy_csv_file):
    with pytest.raises(Exception):
        load_products_from_csv('products.sql')

def test_loaded_products_valid(copy_csv_file):
    products = load_products_from_csv('copy_products.csv')

    assert len(products) == 71

def test_loaded_products_valid2(copy_csv_file):
    products = load_products_from_csv('copy_products.csv')

    assert products[0].name == "Apple"
    assert products[0].price == 2
    assert products[0].units == 10

def test_loaded_products_valid3(copy_csv_file):
    products = load_products_from_csv('copy_products.csv')

    assert products[70].name == "Backpack"
    assert products[70].price == 15
    assert products[70].units == 1
def test_loaded_products_not_empty_file(copy_csv_file):
    products = load_products_from_csv('copy_products.csv')

    assert len(products) != 0