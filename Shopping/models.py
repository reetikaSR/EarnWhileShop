from django.db import models
from django.core.exceptions import ValidationError
import AmazonASINMatcher


# Create your models here.
def url_validator(value):
    if not AmazonASINMatcher.is_valid_link(value):
        raise ValidationError(message="the url is not valid", code='invalid')


class Purchase(models.Model):
    link = models.URLField(default='', validators=[url_validator])
    quantity = models.IntegerField()
    paytm_number = models.BigIntegerField(max_length=10)

