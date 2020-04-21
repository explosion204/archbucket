from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import date

class ItemType(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    description = models.TextField(verbose_name='Description', default='desc')
    url = models.SlugField(max_length=150, unique=True, default=None)

class Item(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    description = models.TextField(verbose_name='Description', max_length=50)
    source_code = models.TextField(verbose_name='Source code')
    documentation = models.TextField(verbose_name='Documentation')
    item_type = models.ForeignKey(ItemType, verbose_name='Item type', on_delete=models.CASCADE)
    url = models.SlugField(max_length=150, unique=True, default=None)

class Feedback(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment', max_length=250)
    value = models.FloatField(verbose_name='Value', default=5.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.FloatField(verbose_name='Value', default=5.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

class Release(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    version = models.CharField(verbose_name='Version', max_length=10)
    changelog = models.TextField(verbose_name='Changelog')
