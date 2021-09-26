from django.test import TestCase
from account.models import Account, AccountManager

class AccountModelTest(TestCase):
    def setUp(self):
        self.testEmail = 'email.test@yandex.com'
        self.testUsername = 'usernametest'
        self.testPassword = 'passwordtest'
        self.testPasswordConfirmation = 'passwordtest'
        self.testRole = 'buyer'

        Account.objects.create(
            email = 'account.test@yandex.com',
            username = 'usernameaccountest',
            password = 'passwordaccountest',
            passwordConfirmation = 'passwordaccountest',
            role = 'buyer'
        )
    
    def test_create_user_with_valid_input(self):
        response = Account.objects.create_user(
            email = self.testEmail,
            username = self.testUsername,
            password = self.testPassword,
            role = self.testRole
        )
        account = Account.objects.get(email = self.testEmail)
        self.assertEqual(response, account)
    
    def test_create_user_with_invalid_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(
                email = None, 
                username = self.testUsername, 
                password = self.testPassword, 
                role = self.testRole
            )
    
    def test_create_user_with_invalid_username(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(
                email = self.testEmail,
                username = None,
                password = self.testPassword,
                role = self.testRole
            )
    
    def test_create_user_with_invalid_role(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(
                email = self.testEmail,
                username = self.testUsername,
                password = self.testPassword,
                role = None
            )
    
    def test_create_super_user_with_valid_input(self):
        response = Account.objects.create_superuser(
            email = self.testEmail,
            username = self.testUsername,
            password = self.testPassword,
            role = self.testRole
        )
        account = Account.objects.get(email = self.testEmail)
        self.assertEqual(response, account)
    
    def test_account_name_formatting(self):
        account = Account.objects.get(email = 'account.test@yandex.com')
        expected_object_name = f'{account.email}'
        self.assertEqual(str(account), expected_object_name)