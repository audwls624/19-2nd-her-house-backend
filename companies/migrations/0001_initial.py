# Generated by Django 3.2 on 2021-04-28 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=100)),
                ('star_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('contract_number', models.IntegerField()),
                ('upper_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lower_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=20, max_digits=25)),
                ('longtitude', models.DecimalField(decimal_places=20, max_digits=25)),
                ('thumbnail_image', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='CompanyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
            ],
            options={
                'db_table': 'company_images',
            },
        ),
    ]
