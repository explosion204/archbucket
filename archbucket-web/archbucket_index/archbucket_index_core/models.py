from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator

class ItemType(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    description = models.TextField(verbose_name='Description', default='desc')
    url = models.SlugField(max_length=150, unique=True, default=None)

class Item(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Description', max_length=50)
    source_code = models.TextField(verbose_name='Source code')
    documentation = models.TextField(verbose_name='Documentation')
    item_type = models.ForeignKey(ItemType, verbose_name='Item type', on_delete=models.CASCADE)
    item_rating = models.FloatField(verbose_name='Value', default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    votes = models.IntegerField(verbose_name='Votes', default=0)
    status = models.CharField(max_length=1, choices=[('v', 'Verified'), ('n', 'Not verified')], default='n')
    url = models.SlugField(max_length=150, unique=True, default=None)

    class Meta:
        permissions = [
            ('can_save_directly', 'Can save or modify directly.')
        ]


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Text', max_length=250)
    datetime = models.DateTimeField(verbose_name='Datetime', auto_now_add=True)

class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Value', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        count = len(Rating.objects.filter(item=self.item))

        try:
            former_rating = Rating.objects.get(Q(user=self.user) | Q(item=self.item))
            former_rating_value = Rating.objects.get(user=self.user).value
            former_rating.delete()
            self.item.item_rating = (self.item.item_rating * count - former_rating_value + int(self.value)) / count
        except ObjectDoesNotExist:
            self.item.item_rating = (self.item.item_rating * count + int(self.value)) / (count + 1)
            self.item.votes += 1

        self.item.save()
        super(Rating, self).save(*args, **kwargs)


class Release(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    version = models.CharField(verbose_name='Version', max_length=10)
    changelog = models.TextField(verbose_name='Changelog')
