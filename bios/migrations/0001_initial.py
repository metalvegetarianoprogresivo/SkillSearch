# Generated by Django 2.0.7 on 2018-10-01 22:25

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('account_name', models.TextField(blank=True, null=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('p1_end', models.DateField(blank=True, null=True)),
                ('p2_end', models.DateField(blank=True, null=True)),
                ('p3_end', models.DateField(blank=True, null=True)),
                ('utilisation', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('title', models.CharField(default='', max_length=100)),
                ('url', models.TextField(blank=True, null=True)),
                ('location', models.CharField(default='', max_length=50)),
                ('email', models.TextField(blank=True, null=True)),
                ('profile', models.TextField(blank=True, null=True)),
                ('technical_skills', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('experience', models.TextField(blank=True, null=True)),
                ('assignments', djongo.models.fields.ArrayReferenceField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bios.Assignments')),
            ],
        ),
        migrations.CreateModel(
            name='EmailAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
            ],
        ),
    ]
