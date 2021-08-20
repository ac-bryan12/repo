# Generated by Django 3.2.6 on 2021-08-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('precio', models.FloatField()),
                ('description', models.TextField(max_length=150)),
                ('documentos', models.TextField(max_length=150)),
                ('reportes', models.IntegerField()),
                ('soporte', models.TextField(max_length=50)),
                ('firma', models.TextField(max_length=50)),
                ('usuarios', models.TextField(max_length=50)),
                ('clientes', models.TextField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Planes',
        ),
    ]
