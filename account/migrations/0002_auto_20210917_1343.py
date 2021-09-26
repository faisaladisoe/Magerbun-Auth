# Generated by Django 3.2.7 on 2021-09-17 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='angkatan',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='jurusan',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='namaLengkap',
            field=models.CharField(max_length=150, null=True, verbose_name='nama lengkap'),
        ),
        migrations.AddField(
            model_name='account',
            name='namaPanggilan',
            field=models.CharField(max_length=20, null=True, verbose_name='nama panggilan'),
        ),
        migrations.AddField(
            model_name='account',
            name='namaToko',
            field=models.CharField(max_length=50, null=True, verbose_name='nama toko'),
        ),
        migrations.AddField(
            model_name='account',
            name='nomorHP',
            field=models.CharField(max_length=15, null=True, verbose_name='nomor hp'),
        ),
        migrations.AddField(
            model_name='account',
            name='nomorInduk',
            field=models.CharField(max_length=30, null=True, verbose_name='nomor induk mahasiswa/pegawai'),
        ),
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], default='visitor', max_length=7),
        ),
        migrations.AddField(
            model_name='account',
            name='tipeDagangan',
            field=models.CharField(max_length=10, null=True, verbose_name='tipe dagangan'),
        ),
    ]
