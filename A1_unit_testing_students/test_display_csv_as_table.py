from unittest.mock import patch

from products import display_csv_as_table
import pytest
import pytest_mock


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


def test_display_csv_as_table_with_missing_header(capsys, mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Light Bulbs,1,15\nVacuumCleaner,100,1"))
    with pytest.raises(ValueError, match="CSV file must have a header."):
     display_csv_as_table("missing_header.csv")
     captured = capsys.readouterr()
     expected_output = ("missing header")
     assert captured.out == expected_output

def test_display_csv_mixed_data_types(capsys,mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Ice cream,55,34,mango,4,6,Vacuum Cleaner,100,1"))
    display_csv_as_table("csv_with_unicode_characters.csv")
    captured = capsys.readouterr()
    expected_output = ("[Ice cream,55,34,mango,4,six]")
    assert captured.out == expected_output

def test_display_csv_as_table_empty_csv(capsys,mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    display_csv_as_table("empty.csv")
    captured = capsys.readouterr()
    expected_output = ("Empty csv")
    assert captured.out == expected_output

def test_display_csv_as_table_with_duplicate_rows(capsys, mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Pens,0.5,10\nDumbbells,20,2\nPens,0.5,10"))
    display_csv_as_table("csv_with_duplicates.csv")
    captured = capsys.readouterr()
    expected_output = ("[Pens,0.5,10,Pens,0.5,10]")
    assert captured.out == expected_output

def test_display_csv_as_table_with_numeric_values_as_strings(capsys, mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Trash Bags,2,10\nMicrowave,80,1"))
    display_csv_as_table("csv_numeric_as_strings.csv")
    captured = capsys.readouterr()
    expected_output = ("['Trash Bags', '2', '10']\n['Microwave', '80', '1']\n")
    assert captured.out == expected_output
    assert captured.err == ""


