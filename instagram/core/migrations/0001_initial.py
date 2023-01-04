# Generated by Django 4.1.4 on 2023-01-04 23:36

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import instagram.core.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=40, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=40, null=True, verbose_name='last name')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username can be only contains letters, numbers, . or _', regex='^([\\w\\d\\._]+[^\\s\\-@\\*\\[\\{(\\)\\}\\]\\/\\+:,;\\\\%&$]){3,30}$')], verbose_name='username')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^([a-zA-Z0-9\\._-]{3,}[^\\s])@\\w{2,25}\\.\\w{2,15}(\\.\\w{2,15})?$')], verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', instagram.core.models.user.UserManager()),
            ],
        ),
    ]
