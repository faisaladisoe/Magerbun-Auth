from django.urls import reverse
from django.test import TestCase
from account.models import Account

from rest_framework import status
from rest_framework.utils import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class AccountTests(APITestCase, TestCase):
    def setUp(self):
        self.valid_input = {
            'email': 'testemail@account.com',
            'username': 'testusername',
            'password': 'testpassword',
            'passwordConfirmation': 'testpassword',
            'role': 'buyer'
        }

        self.invalid_input = {
            'email': 'accountemail@test.com',
            'username': 'invalidusername',
            'password': 'invalidpassword',
            'passwordConfirmation': 'invalidpassword',
            'role': 'buyer'
        }

        self.url = reverse('account:Account Register')
        self.data = {
            'email': 'accountemail@test.com',
            'username': 'accountusername',
            'password': 'accountpassword',
            'passwordConfirmation': 'accountpassword',
            'role': 'buyer'
        }
        self.response = self.client.post(self.url, self.data, format = 'json')
        self.user = Account.objects.get(email = self.data['email'])
        self.token = Token.objects.get(user = self.user).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {self.token}')
    
    def test_retrieve_all_accounts(self):
        url = reverse('account:Account Test')
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_register_account_with_valid_input(self):
        url = reverse('account:Account Register')
        data = self.valid_input
        response = self.client.post(url, data, format = 'json')
        
        account = Account.objects.get(email = data['email'])
        token = Token.objects.get(user = account).key
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data, {
            'email': 'testemail@account.com', 
            'username': 'testusername', 
            'token': token, 
            'status': 'Account Successfully Created!'
        })
    
    def test_register_account_with_invalid_input(self):
        url = reverse('account:Account Register')
        data = self.invalid_input
        response = self.client.post(url, data, format = 'json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_account_with_whitespace_in_username_input(self):
        url = reverse('account:Account Register')
        data = {
            'email': 'account.email@test.com',
            'username': 'invalid username',
            'password': 'invalidpassword',
            'passwordConfirmation': 'invalidpassword',
            'role': 'buyer'
        }
        response = self.client.post(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_account_with_inconsistent_of_password_and_its_confirmation(self):
        url = reverse('account:Account Register')
        data = {
            'email': 'account.email@test.com',
            'username': 'invalidusername',
            'password': 'invalidpassword',
            'passwordConfirmation': 'invalidpassword12',
            'role': 'buyer'
        }
        response = self.client.post(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_account_details_with_valid_input(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data, {
            'email': 'accountemail@test.com', 
            'username': 'accountusername', 
            'role': 'buyer', 
            'namaLengkap': None, 
            'nomorInduk': None, 
            'angkatan': None, 
            'jurusan': None, 
            'password': '*******'
        })
    
    def test_retrieve_non_exist_account_details(self):
        url = reverse('account:Account Profile', kwargs = {'role': 'buyer', 'email': 'haha@test.com'})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_unauthorized_account_details(self):
        urlPost = reverse('account:Account Register')
        dataPost = {
            'email': 'dummyemail@test.com',
            'username': 'dummyusername',
            'password': 'dummypassword',
            'passwordConfirmation': 'dummypassword',
            'role': 'seller'
        }
        responsePost = self.client.post(urlPost, dataPost, format = 'json')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummyemail@test.com'})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'error': "Sorry, you're prohibited in this area"
        })
    
    def test_retrieve_wrong_role_slug(self):
        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': self.data['email']})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_valid_seller_account(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data, {
            'email': 'dummytest@seller.com', 
            'username': 'dummyseller', 
            'role': 'seller', 
            'namaLengkap': None, 
            'namaPanggilan': None, 
            'nomorHP': None, 
            'namaToko': None, 
            'tipeDagangan': None, 
            'password': '*******'
        })
    
    def test_patch_valid_buyer_account(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'username': 'updatedusernamebuyer',
            'password': 'thisisnewpassword',
            'passwordConfirmation': 'thisisnewpassword'
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data, {
            'email': 'accountemail@test.com', 
            'username': 'accountusername', 
            'role': 'buyer', 
            'namaLengkap': None, 
            'nomorInduk': None, 
            'angkatan': None, 
            'jurusan': None
        })
    
    def test_patch_valid_seller_account(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        data = {
            'username': 'updatedsellerusername'
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data, {
            'email': 'dummytest@seller.com', 
            'username': 'dummyseller', 
            'role': 'seller', 
            'namaLengkap': None, 
            'namaPanggilan': None, 
            'nomorHP': None, 
            'namaToko': None, 
            'tipeDagangan': None
        })
    
    def test_patch_valid_buyer_account_with_invalid_input(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'username': ''
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_account_with_invalid_username(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'username': 'hai hai'
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_another_invalid_username(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'username': self.data['username']
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_inconsistent_of_password_and_its_confirmation(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'password': 'huehuehue',
            'passwordConfirmation': 'testpassword123'
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_password_remain_unchanged(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'password': self.data['password'],
            'passwordConfirmation': self.data['passwordConfirmation']
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_valid_and_invalid_full_name(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'namaLengkap': 'John Doe'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_valid_and_invalid_registration_number(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'nomorInduk': '12313124'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_valid_and_invalid_school_generation(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'angkatan': '1999'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_buyer_account_with_valid_and_invalid_major_degree(self):
        url = reverse('account:Account Profile', kwargs = {'role': self.data['role'], 'email': self.data['email']})
        data = {
            'jurusan': 'Ilmu Kodok'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_seller_account_with_valid_and_invalid_nickname(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        data = {
            'namaPanggilan': 'Eddy'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_seller_account_with_valid_and_invalid_phone_number(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        data = {
            'nomorHP': '088888888'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_seller_account_with_valid_and_invalid_stall_name(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        data = {
            'namaToko': 'Toko Jaya Makmur'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_valid_seller_account_with_valid_and_invalid_item_type(self):
        account = Account.objects.create_superuser(
            email = 'dummytest@seller.com',
            username = 'dummyseller',
            password = 'dummypassword',
            role = 'seller'
        )
        account.save()

        accountSeller = Account.objects.get(email = 'dummytest@seller.com')
        tokenSeller = Token.objects.get(user = accountSeller).key
        self.client.credentials(HTTP_AUTHORIZATION = f'Token {tokenSeller}')

        url = reverse('account:Account Profile', kwargs = {'role': 'seller', 'email': 'dummytest@seller.com'})
        data = {
            'tipeDagangan': 'campuran'
        }
        response = self.client.patch(url, data, format = 'json')
        responseNew = self.client.patch(url, data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(responseNew.status_code, status.HTTP_400_BAD_REQUEST)