from django.db import models
from django.core.validators import int_list_validator
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


class Rule(models.Model):
    lhs = models.CharField(db_column='lhs', max_length=50)
    rhs = models.CharField(db_column='rhs', max_length=10)
    gender = models.CharField(db_column='gender', max_length=1, null=True)
    min_age = models.IntegerField(db_column='min_age', default=0)
    max_age = models.IntegerField(db_column='max_age', default=150)
    support = models.FloatField(db_column='support', default=0)
    confidence = models.FloatField(db_column='confidence', default=0)
    num_accepted = models.IntegerField(db_column='num_accepted', default=0)
    num_rejected = models.IntegerField(db_column='num_rejected', default=0)
    num_suggested = models.IntegerField(db_column='num_suggested', default=0)
    num_flags = models.IntegerField(db_column='num_flags', default=0)
    # review_status: 1- user flagged, 2- admin approved for rule supression 3- admin disapprove rule for supression(always show)
    review_status = models.IntegerField(db_column='review_status', default=0)
    active = models.BooleanField(db_column='active', default=True)
    # manual: 0 for a rule that has been mined, 1 for a rule that has been entered by an admin
    manual = models.IntegerField(db_column='manual', default=0)
    # oracle: rules that were mined by Mingkai and agreed upon by a panel of professionals
    oracle = models.BooleanField(db_column='oracle', default=False)

    class Meta:
        db_table = 'rules'
        unique_together = (("rhs", "lhs", "min_age", "max_age", "gender"),)


class Code(models.Model):
    code = models.CharField(db_column='code', max_length=20, primary_key=True)
    description = models.TextField(db_column='description')
    parent = models.CharField(db_column='parent', max_length=20)
    children = models.CharField(db_column='children', max_length=1000)
    times_coded = models.IntegerField(db_column='times_coded', default=0)
    times_coded_dad = models.IntegerField(db_column='times_coded_dad', default=0)
    keyword_terms = models.TextField(db_column='keyword_terms')
    selectable = models.BooleanField(db_column='selectable', default=True)


# Used for creating the tree, using chapters as parents to blocks of codes,
# blocks of codes as parents of high level codes, etc.
# Example: Chapter 01 is parent of A00-A09, A15-A19, etc.
# A00-A09 is parent of A00, A01, ... , A09
class TreeCode(models.Model):
    code = models.CharField(db_column='code', max_length=20, primary_key=True)
    description = models.CharField(db_column='description', max_length=1000)
    parent = models.CharField(db_column='parent', max_length=20)
    children = models.TextField(db_column='children', max_length=1000)

    class Meta:
        db_table = 'tree_codes'


# Used to store how many times each block of code has been used,
# and the number of rules between different blocks
class CodeBlockUsage(models.Model):
    block = models.CharField(
        db_column='block', max_length=20, primary_key=True)
    times_coded = models.IntegerField(db_column='times_coded', default=0)
    destination_counts = models.CharField(db_column='destination_counts', max_length=1000,
                                          validators=[int_list_validator], null=True)

    class Meta:
        db_table = 'code_usage'


# All dagger asterisk pairs
class DaggerAsterisk(models.Model):
    dagger = models.CharField(db_column='dagger', max_length=20)
    asterisk = models.CharField(db_column='asterisk', max_length=20)

    class Meta:
        db_table = 'dagger_asterisk'
