# Generated by Django 4.2.5 on 2023-10-03 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('income', 'Income'), ('expenses', 'Expenses'), ('investments', 'Investments'), ('transfers', 'Transfers')], max_length=20)),
                ('payment_method', models.CharField(max_length=50)),
                ('reference_number', models.CharField(max_length=50)),
               ('attachments', models.FileField(upload_to='transaction_attachments/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
