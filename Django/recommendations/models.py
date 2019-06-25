from django.db import models
from django.core.validators import int_list_validator


class Rule(models.Model):
    lhs = models.CharField(db_column='lhs', max_length=50)
    rhs = models.CharField(db_column='rhs', max_length=10)
    min_age = models.IntegerField(db_column='min_age', default=0)
    max_age = models.IntegerField(db_column='max_age', default=150)
    support = models.FloatField(db_column='support', default=0)
    confidence = models.FloatField(db_column='confidence', default=0)
    num_accepted = models.IntegerField(db_column='num_accepted', default=0)
    num_rejected = models.IntegerField(db_column='num_rejected', default=0)
    num_suggested = models.IntegerField(db_column='num_suggested', default=0)
    # review_status: 1- user flagged for rule supression, 2- admin approved for rule supression 3- admin disapprove rule for supression(always show)
    review_status = models.IntegerField(db_column='review_status', default=0)
    active = models.BooleanField(db_column='active', default=True)

    class Meta:
        #managed = False
        db_table = 'rules'
        unique_together = (("rhs", "lhs", "min_age", "max_age"),)


class Code(models.Model):
    code = models.CharField(db_column='code', max_length=20, primary_key=True)
    description = models.CharField(db_column='description', max_length=100)
    parent = models.CharField(db_column='parent', max_length=20)
    children = models.TextField(db_column='children', max_length=1000)
    times_coded = models.IntegerField(db_column='times_coded', default=0)

    class Meta:
        db_table = 'codes'


class TreeCode(models.Model):
    code = models.CharField(db_column='code', max_length=20, primary_key=True)
    description = models.CharField(db_column='description', max_length=100)
    parent = models.CharField(db_column='parent', max_length=20)
    children = models.TextField(db_column='children', max_length=1000)

    class Meta:
        db_table = 'tree_codes'


class CodeBlockUsage(models.Model):
    block = models.CharField(
        db_column='block', max_length=20, primary_key=True)
    times_coded = models.IntegerField(db_column='times_coded', default=0)
    destination_counts = models.CharField(db_column='destination_counts', max_length=1000,
                                          validators=[int_list_validator], null=True)

    class Meta:
        db_table = 'code_usage'


class DaggerAsterisk(models.Model):
    dagger = models.CharField(db_column='dagger', max_length=20)
    asterisk = models.CharField(db_column='asterisk', max_length=20)
    description = models.CharField(db_column='description', max_length=1000)

    class Meta:
        db_table = 'dagger_asterisk'
