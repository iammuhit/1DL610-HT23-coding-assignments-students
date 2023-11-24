import pytest, shutil, json, copy
from unittest import TestCase, main, mock
from io import StringIO
from login import login, validate_password, check_username


@pytest.fixture(scope='class')
def users(request):
    shutil.copy('users.json', 'test_users.json')
    with open('test_users.json', 'r') as file:
        request.cls.users = json.load(file)


@pytest.mark.usefixtures('users')
class LoginTestCase(TestCase):

    def test_login_with_correct_username_and_password(self):
        username = 'Ramanathan'
        password = 'Notaproblem23*'

        with mock.patch('sys.stdout', new_callable=StringIO) as mock_output:
            with mock.patch('builtins.input', side_effect=[username, password]):
                login_response = login()
            mock_output.seek(0)
            captured_output = mock_output.read()

        expected_output = 'Successfully logged in.\n'
        expected_response = {
            'username': username,
            'wallet': 100,
        }

        self.assertEqual(captured_output, expected_output)
        self.assertDictEqual(login_response, expected_response)

    def test_login_with_correct_username_and_wrong_password(self):
        username = 'Ramanathan'
        password = 'Maya@123'

        with mock.patch('sys.stdout', new_callable=StringIO) as mock_output:
            with mock.patch('builtins.input', side_effect=[username, password]):
                login_response = login()
            mock_output.seek(0)
            captured_output = mock_output.read()

        expected_output = 'The password was incorrect.\n'

        self.assertIsNone(login_response)
        self.assertEqual(captured_output, expected_output)

    def test_login_with_wrong_username_and_without_registration(self):
        username = 'Muhit'
        registration = 'N'

        with mock.patch('builtins.input', side_effect=[username, registration]):
            login_response = login()

        self.assertIsNone(login_response)

    def test_password_validation_C1(self):
        password = 'mayarun'
        validation_errors = validate_password(password)
        expected_errors = {
            'length': 'The password must be at least eight characters.',
            'capital': 'The password must contain at least one capital letter.',
            'symbol': 'The password must contain at least one special symbol.',
        }
        self.assertDictEqual(validation_errors, expected_errors)

    def test_password_validation_C2(self):
        password = 'nurulamin'
        validation_errors = validate_password(password)
        expected_errors = {
            'capital': 'The password must contain at least one capital letter.',
            'symbol': 'The password must contain at least one special symbol.',
        }
        self.assertDictEqual(validation_errors, expected_errors)

    def test_password_validation_C3(self):
        password = 'MayarunN'
        validation_errors = validate_password(password)
        expected_errors = {
            'symbol': 'The password must contain at least one special symbol.',
        }
        self.assertDictEqual(validation_errors, expected_errors)

    def test_password_validation_C4(self):
        password = 'Mayarun$'
        validation_errors = validate_password(password)
        expected_errors = {}
        self.assertDictEqual(validation_errors, expected_errors)

    def test_password_validation_C5(self):
        password = 'Mayarun'
        validation_errors = validate_password(password)
        expected_errors = {
            'length': 'The password must be at least eight characters.',
            'symbol': 'The password must contain at least one special symbol.',
        }
        self.assertDictEqual(validation_errors, expected_errors)

    def test_check_user_exists_in_database(self):
        username = 'Tiger'
        users = copy.deepcopy(self.users)
        has_user = check_username(username, users)
        self.assertTrue(has_user)

    def test_check_user_not_exists_in_database(self):
        username = 'Maya'
        users = copy.deepcopy(self.users)
        has_user = check_username(username, users)
        self.assertFalse(has_user)


if __name__ == '__main__':
    main()
