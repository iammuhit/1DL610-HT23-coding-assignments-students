import pytest, copy
from unittest import TestCase, main, mock
from io import StringIO
from checkout_and_payment import ShoppingCart, load_products_from_csv
from logout import logout


@pytest.fixture(scope='class')
def cart(request):
    request.cls.cart = ShoppingCart()


@pytest.fixture(scope='class')
def products(request):
    request.cls.products = load_products_from_csv('products.csv')


@pytest.mark.usefixtures('cart', 'products')
class LogoutTestCase(TestCase):

    def test_logout_when_cart_is_empty(self):
        self.assertTrue(logout(self.cart))
        self.assertListEqual(self.cart.items, [])

    def test_logout_with_wrong_param(self):
        with self.assertRaises(Exception):
            logout_response = logout(None)

    def test_logout_when_cart_has_items(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])

        with mock.patch('sys.stdout', new_callable=StringIO) as mock_output:
            with mock.patch('builtins.input', side_effect=['Y']):
                logout_response = logout(cart)
            mock_output.seek(0)
            captured_output = mock_output.read()

        expected = 'Your cart is not empty.You have following items\n'
        expected += f"{self.products[0].get_product()}\n"

        self.assertTrue(logout_response)
        self.assertEqual(captured_output, expected)
        self.assertEqual(len(cart.items), 0)

    def test_logout_cancel_when_cart_has_items(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])
        cart.add_item(self.products[1])

        with mock.patch('sys.stdout', new_callable=StringIO) as mock_output:
            with mock.patch('builtins.input', side_effect=['N']):
                logout_response = logout(cart)
            mock_output.seek(0)
            captured_output = mock_output.read()

        expected = 'Your cart is not empty.You have following items\n'
        expected += f"{self.products[0].get_product()}\n"
        expected += f"{self.products[1].get_product()}\n"

        self.assertFalse(logout_response)
        self.assertEqual(captured_output, expected)
        self.assertEqual(len(cart.items), 2)

    def test_cart_was_cleared_after_logout(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[1])
        cart.add_item(self.products[5])

        with mock.patch('builtins.input', side_effect=['Y']):
            logout_response = logout(cart)

        self.assertTrue(logout_response)
        self.assertEqual(len(cart.items), 0)

    def test_cart_was_not_cleared_when_logout_cancelled(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[1])
        cart.add_item(self.products[2])
        cart.add_item(self.products[3])

        with mock.patch('builtins.input', side_effect=['N']):
            logout_response = logout(cart)

        self.assertFalse(logout_response)
        self.assertEqual(len(cart.items), 3)

    def test_logout_confirmation_with_uppercase_input(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])

        with mock.patch('builtins.input', side_effect=['Y']):
            logout_response = logout(cart)

        self.assertTrue(logout_response)
        self.assertEqual(len(cart.items), 0)

    def test_logout_confirmation_with_lowercase_input(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])

        with mock.patch('builtins.input', side_effect=['y']):
            logout_response = logout(cart)

        self.assertTrue(logout_response)
        self.assertEqual(len(cart.items), 0)

    def test_logout_confirmation_with_wrong_input(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])

        with mock.patch('builtins.input', side_effect=['Yes']):
            logout_response = logout(cart)

        self.assertFalse(logout_response)
        self.assertEqual(len(cart.items), 1)

    def test_logout_confirmation_with_numeric_input(self):
        cart = copy.deepcopy(self.cart)
        cart.add_item(self.products[0])

        with mock.patch('builtins.input', side_effect=['1']):
            logout_response = logout(cart)

        self.assertFalse(logout_response)
        self.assertEqual(len(cart.items), 1)


if __name__ == '__main__':
    main()
