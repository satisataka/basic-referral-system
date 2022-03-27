# Generated by Django 3.2.12 on 2022-03-24 11:23

import account.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='phone number')),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_verifited', models.BooleanField(default=False, verbose_name='verifited')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('invite_key', models.EmailField(max_length=6, verbose_name='invite key')),
                ('user_invite_key', models.EmailField(max_length=6, verbose_name='my invite key')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'unique_together': {('phone_number', 'email')},
            },
            managers=[
                ('objects', account.models.AccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(editable=False, max_length=128, region=None)),
                ('otp', models.CharField(editable=False, max_length=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.IntegerField(default=0)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'OTP Token',
                'verbose_name_plural': 'OTP Tokens',
            },
        ),
        migrations.CreateModel(
            name='InviteKey',
            fields=[
                ('master', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='master', serialize=False, to='account.account')),
                ('key', models.CharField(editable=False, max_length=40)),
                ('slave', models.ManyToManyField(related_name='slave', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invite Key',
                'verbose_name_plural': 'Invite Key',
            },
        ),
    ]
