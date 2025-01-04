# Generated by Django 5.1.4 on 2024-12-30 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={},
        ),
        migrations.AlterModelManagers(
            name='users',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='users',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='projectmembers',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='projectmembers',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Member', 'Member')], max_length=10),
        ),
        migrations.AlterField(
            model_name='projects',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], default='To Do', max_length=15),
        ),
        migrations.AlterField(
            model_name='users',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]