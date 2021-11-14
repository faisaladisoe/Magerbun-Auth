from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from account.models import Account
from account.serializers import AccountSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def accountTest(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many = True)
    data = serializer.data
    return Response(data, status = status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def accountRegister(request):
    response = {}
    serializer = AccountSerializer(data = request.data)
    if serializer.is_valid():
        account = serializer.save()
        token = Token.objects.get(user = account).key
        response['email'] = account.email
        response['username'] = account.username
        response['token'] = token
        response['status'] = 'Account Successfully Created!'
        return Response(response, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAdminUser|IsAuthenticated])
def accountProfile(request, role, email):
    try:
        account = Account.objects.get(email = email)
        print(account)
    except Account.DoesNotExist:
        message = {'error': 'Sorry, seems there\'s a problem with your email'}
        return Response(message, status = status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_staff and account != request.user:
        message = {'error': 'Sorry, you\'re prohibited in this area'}
        return Response(message, status = status.HTTP_403_FORBIDDEN)

    if account.role != role:
        message = {'error': 'Sorry, seems there\'s a problem with the slug that relate to the email or role'}
        return Response(message, status = status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        serializer = None
        data = None

        if account.role == 'buyer':
            serializer = AccountSerializer(account, many = False, fields = (
                'username', 'email', 'role', 'namaLengkap', 'nomorInduk', 'angkatan', 'jurusan'
            ))
            data = serializer.data
            data['password'] = '*******'
        elif account.role == 'seller':
            serializer = AccountSerializer(account, many = False, fields = (
                'username', 'email', 'role', 'namaLengkap', 'namaPanggilan', 'nomorHP', 'namaToko', 'tipeDagangan'
            ))
            data = serializer.data
            data['password'] = '*******'

        return Response(data, status = status.HTTP_200_OK)
    elif request.method == 'PATCH':
        
        serializer = None
        if account.role == 'buyer':
            serializer = AccountSerializer(account, data = request.data, partial = True, fields = (
                'username', 'email', 'role', 'namaLengkap', 'nomorInduk', 'angkatan', 'jurusan', 'password', 'passwordConfirmation'
            ))
        elif account.role == 'seller':
            serializer = AccountSerializer(account, data = request.data, partial = True, fields = (
                'username', 'email', 'role', 'namaLengkap', 'namaPanggilan', 'nomorHP', 'namaToko', 'tipeDagangan'
            ))

        if serializer.is_valid():
            serializer.update(account.email)
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)