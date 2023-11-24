import json

# Login as a user
def login():
    username = input('Enter your username: ')

    # Look for user in database
    with open('users.json', 'r') as file:
        data = json.load(file)
        user = None
        for entry in data:
            if entry.get('username') == username:
                user = entry
                password = input('Enter your password: ')
                if entry.get('password') == password:
                    print('Successfully logged in.')
                    return {
                        'username': entry.get('username'),
                        'wallet': entry.get('wallet'),
                    }
                else:
                    print('The password was incorrect.')
                    return None

        # register new user
        if user is None:
            return register({'username': username})

        return None


def register(user):
    register_confirmation = input('User not found! Would you like to register? (Y/N): ')
    if register_confirmation.upper() == 'Y':
        while True:
            password = input('Enter your password: ')
            validation_errors = validate_password(password)
            if not validation_errors:
                user.update({'password': password})
                user.update({'wallet': 0})
                save_user(user)

                print('Your account was created successfully.')
                print('Successfully logged in.')

                return {
                    'username': user.get('username'),
                    'wallet': user.get('wallet'),
                }
            else:
                for validation_error in validation_errors.values():
                    print(validation_error)
    return None


def save_user(user):
    """
    Save the new user into database.

    :param user: the user dictionary
    :return: void
    """
    with open('users.json', 'r+') as file:
        users = json.load(file)
        users.append(user)

        # Update the users.json file
        file.seek(0)
        json.dump(users, file, indent=4)
        file.close()


def check_username(username, data):
    """
    Check if the user already exists.

    :param username: the username of the new user
    :param data: the list of existing users
    :return: boolean
    """
    return any(user.get('username') == username for user in data)


def validate_password(password):
    """
    Validates the password criteria.

    :param password: the password
    :return: dictionary: the list of errors
    """
    min_length = 8
    errors = {}

    if len(password) < min_length:
        errors.update({'length': 'The password must be at least eight characters.'})

    if not any(char.isupper() for char in password):
        errors.update({'capital': 'The password must contain at least one capital letter.'})

    if not any(not char.isalnum() for char in password):
        errors.update({'symbol': 'The password must contain at least one special symbol.'})

    return errors
