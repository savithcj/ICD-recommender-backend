from django.db import models


class Rule(models.Model):
    lhs = models.CharField(db_column='lhs', max_length=50)
    rhs = models.CharField(db_column='rhs', max_length=10)
    min_age = models.IntegerField(db_column='min_age')
    max_age = models.IntegerField(db_column='max_age')
    support = models.FloatField(db_column='support')
    confidence = models.FloatField(db_column='confidence')
    num_accepted = models.IntegerField(db_column='num_accepted', default=0)
    num_rejected = models.IntegerField(db_column='num_rejected', default=0)
    num_suggested = models.IntegerField(db_column='num_suggested', default=0)

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
