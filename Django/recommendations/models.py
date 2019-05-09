from django.db import models

# Create your models here.
class Rule(models.Model):
    lhs = models.CharField(db_column = 'lhs', max_length = 50)
    rhs = models.CharField(db_column = 'rhs', max_length = 10)
    min_age = models.IntegerField(db_column = 'min_age')
    max_age = models.IntegerField(db_column = 'max_age')
    support = models.FloatField(db_column = 'support')
    confidence = models.FloatField(db_column = 'confidence')
    num_accepted = models.IntegerField(db_column = 'num_accepted')
    num_rejected = models.IntegerField(db_column = 'num_rejected')

    class Meta:
        #managed = False
        db_table = 'rules'
        unique_together = (("rhs", "lhs","min_age","max_age"),)