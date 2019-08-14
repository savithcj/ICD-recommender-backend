# Generated by Django 2.2.1 on 2019-08-14 17:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('code', models.CharField(db_column='code', max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField(db_column='description')),
                ('parent', models.CharField(db_column='parent', max_length=20)),
                ('children', models.CharField(db_column='children', max_length=1000)),
                ('times_coded', models.IntegerField(db_column='times_coded', default=0)),
                ('times_coded_dad', models.IntegerField(db_column='times_coded_dad', default=0)),
                ('keyword_terms', models.TextField(db_column='keyword_terms')),
            ],
        ),
        migrations.CreateModel(
            name='CodeBlockUsage',
            fields=[
                ('block', models.CharField(db_column='block', max_length=20, primary_key=True, serialize=False)),
                ('times_coded', models.IntegerField(db_column='times_coded', default=0)),
                ('destination_counts', models.CharField(db_column='destination_counts', max_length=1000, null=True, validators=[django.core.validators.int_list_validator])),
            ],
            options={
                'db_table': 'code_usage',
            },
        ),
        migrations.CreateModel(
            name='DaggerAsterisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dagger', models.CharField(db_column='dagger', max_length=20)),
                ('asterisk', models.CharField(db_column='asterisk', max_length=20)),
            ],
            options={
                'db_table': 'dagger_asterisk',
            },
        ),
        migrations.CreateModel(
            name='TreeCode',
            fields=[
                ('code', models.CharField(db_column='code', max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='description', max_length=1000)),
                ('parent', models.CharField(db_column='parent', max_length=20)),
                ('children', models.TextField(db_column='children', max_length=1000)),
            ],
            options={
                'db_table': 'tree_codes',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lhs', models.CharField(db_column='lhs', max_length=50)),
                ('rhs', models.CharField(db_column='rhs', max_length=10)),
                ('gender', models.CharField(db_column='gender', max_length=1, null=True)),
                ('min_age', models.IntegerField(db_column='min_age', default=0)),
                ('max_age', models.IntegerField(db_column='max_age', default=150)),
                ('support', models.FloatField(db_column='support', default=0)),
                ('confidence', models.FloatField(db_column='confidence', default=0)),
                ('num_accepted', models.IntegerField(db_column='num_accepted', default=0)),
                ('num_rejected', models.IntegerField(db_column='num_rejected', default=0)),
                ('num_suggested', models.IntegerField(db_column='num_suggested', default=0)),
                ('num_flags', models.IntegerField(db_column='num_flags', default=0)),
                ('review_status', models.IntegerField(db_column='review_status', default=0)),
                ('active', models.BooleanField(db_column='active', default=True)),
                ('manual', models.IntegerField(db_column='manual', default=0)),
                ('oracle', models.BooleanField(db_column='oracle', default=False)),
            ],
            options={
                'db_table': 'rules',
                'unique_together': {('rhs', 'lhs', 'min_age', 'max_age', 'gender')},
            },
        ),
    ]
