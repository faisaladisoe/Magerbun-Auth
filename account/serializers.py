from account.models import Account
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class AccountSerializer(DynamicFieldsModelSerializer):
    
    password = serializers.CharField(write_only = True, validators = [validate_password])
    passwordConfirmation = serializers.CharField(write_only = True)

    class Meta:
        model = Account
        exclude = ['date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin', 'is_superuser']

    def save(self):
        if ' ' in self.validated_data['username']:
            raise serializers.ValidationError({'username': 'username can\'t contain any whitespace(s)'})
        
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            role = self.validated_data['role'].lower()
        )

        password = self.validated_data['password']
        passwordConfirmation = self.validated_data['passwordConfirmation']

        if password != passwordConfirmation:
            raise serializers.ValidationError({'passwordConfirmation': 'password confirmation field didn\'t match with the password field'})
        
        account.set_password(password)
        account.passwordConfirmation = passwordConfirmation

        account.save()
        return account
    
    def update(self, email):
        account = Account.objects.get(email = email)

        if self.validated_data.get('username') and (' ' in self.validated_data['username']):
            raise serializers.ValidationError({'username': 'username can\'t contain any whitespace(s)'})
        elif self.validated_data.get('username'):
            oldUsername = account.username
            newUsername = self.validated_data['username']
            if oldUsername != newUsername:
                account.username = newUsername
                account.save()
            else:
                raise serializers.ValidationError({'username': 'The new username still same with the previous one'})
        
        if self.validated_data.get('password') and self.validated_data.get('passwordConfirmation'):
            oldPassword = account.password
            newPassword = self.validated_data['password']
            passwordConfirmation = self.validated_data['passwordConfirmation']
            if not check_password(newPassword, oldPassword):
                if newPassword != passwordConfirmation:
                    raise serializers.ValidationError({'passwordConfirmation': 'password confirmation field didn\'t match with the password field'})
                account.set_password(newPassword)
                account.passwordConfirmation = passwordConfirmation
                account.save()
            else:
                raise serializers.ValidationError({'password': 'The new password still same with the previous one'})

        content = self.validated_data

        if 'namaLengkap' in content and content['namaLengkap']:
            oldOne = account.namaLengkap
            newOne = content['namaLengkap']
            if oldOne != newOne:
                account.namaLengkap = newOne
                account.save()
            else:
                raise serializers.ValidationError({'nama lengkap': 'The new full name still same with the previous one'})
        
        if 'nomorInduk' in content and content['nomorInduk']:
            oldOne = account.nomorInduk
            newOne = content['nomorInduk']
            if oldOne != newOne:
                account.nomorInduk = newOne
                account.save()
            else:
                raise serializers.ValidationError({'nomor induk': 'The new number ID still same with the previous one'})
        
        if 'angkatan' in content and content['angkatan']:
            oldOne = account.angkatan
            newOne = content['angkatan']
            if oldOne != newOne:
                account.angkatan = newOne
                account.save()
            else:
                raise serializers.ValidationError({'angkatan': 'The new university class still same with the previous one'})
            
        if 'jurusan' in content and content['jurusan']:
            oldOne = account.jurusan
            newOne = content['jurusan']
            if oldOne != newOne:
                account.jurusan = newOne
                account.save()
            else:
                raise serializers.ValidationError({'jurusan': 'The new major still same with the previous one'})
        
        if 'namaPanggilan' in content and content['namaPanggilan']:
            oldOne = account.namaPanggilan
            newOne = content['namaPanggilan']
            if oldOne != newOne:
                account.namaPanggilan = newOne
                account.save()
            else:
                raise serializers.ValidationError({'nama panggilan': 'The new nickname still same with the previous one'})
        
        if 'nomorHP' in content and content['nomorHP']:
            oldOne = account.nomorHP
            newOne = content['nomorHP']
            if oldOne != newOne:
                account.nomorHP = newOne
                account.save()
            else:
                raise serializers.ValidationError({'nomor hp': 'The new phone number still same with the previous one'})
        
        if 'namaToko' in content and content['namaToko']:
            oldOne = account.namaToko
            newOne = content['namaToko']
            if oldOne != newOne:
                account.namaToko = newOne
                account.save()
            else:
                raise serializers.ValidationError({'nama toko': 'The new stall name still same with the previous one'})
        
        if 'tipeDagangan' in content and content['tipeDagangan']:
            oldOne = account.tipeDagangan
            newOne = content['tipeDagangan']
            if oldOne != newOne:
                account.tipeDagangan = newOne.lower()
                account.save()
            else:
                raise serializers.ValidationError({'tipe dagangan': 'The new item type still same with the previous one'})

        return account