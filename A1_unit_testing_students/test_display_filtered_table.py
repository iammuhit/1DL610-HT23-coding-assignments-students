from unittest.mock import patch

from products import display_filtered_table
import pytest
import pytest_mock


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
def test_display_filtered_table_special_characters(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,6\nBanana,0,75\nOrange,1,25\n"))
    display_filtered_table('test.csv', '@pple')
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price','unit']\n['Apple', '1','6']\n"
    assert captured.out == expected_output
def test_display_filtered_table_spaces_in_search_term(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,6\nBanana,0,75\nOrange,1,25\n"))
    display_filtered_table('test.csv', "Ban ana")
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price','unit']\n['Banana', '0','75']\n"
    assert captured.out == expected_output
def test_display_filtered_table_empty_string_search_term(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,6\nBanana,0,75\nOrange,1,25\n"))
    display_filtered_table('test.csv', "")
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price', 'unit']\n"
    assert captured.out == expected_output
def test_display_filtered_table_search_term_not_in_header(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,6\nBanana,0,75\nOrange,1,25\n"))
    display_filtered_table('test.csv',  "Quantity")
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price', 'unit']\n"
    assert captured.out == expected_output
def test_display_filtered_table_numeric_search_term(capsys,mocker):
    mocker.patch('builtins.open',  mocker.mock_open(read_data="Product,Price,unit\nApple,1,6\nBanana,0,75\nOrange,1,25\n"))
    display_filtered_table('test.csv',  "75")
    captured = capsys.readouterr()
    expected_output = "['Product', 'Price', 'unit']\n['Banana','0','75']"
    assert captured.out == expected_output





