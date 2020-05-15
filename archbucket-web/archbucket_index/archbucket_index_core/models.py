from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from datetime import datetime

# USER-RELATED MODELS

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    instance.profile.save()


# GENERAL-PURPOSE MODELS

class ItemType(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    description = models.TextField(verbose_name='Description', default='desc')
    url = models.SlugField(max_length=150, unique=True, default=None)

class Item(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Description', max_length=50)
    source_code = models.TextField(verbose_name='Source code')
    documentation = models.TextField(verbose_name='Documentation')
    item_type = models.ForeignKey(ItemType, verbose_name='Item type', on_delete=models.CASCADE)
    item_rating = models.FloatField(verbose_name='Value', default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    votes = models.IntegerField(verbose_name='Votes', default=0)
    status = models.CharField(max_length=1, choices=[('v', 'Verified'), ('n', 'Not verified')], default='n')
    url = models.SlugField(max_length=150, unique=True, default=None)

    created = models.DateTimeField(verbose_name='Created', default=timezone.now())
    modified = models.DateTimeField(verbose_name='Modified', default=timezone.now())

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Item, self).save(*args, **kwargs)


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Text', max_length=250)
    datetime = models.DateTimeField(verbose_name='Datetime', default=datetime.now())

class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='Value', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        count = len(Rating.objects.filter(item=self.item))

        try:
            former_rating = Rating.objects.get(Q(user=self.user), Q(item=self.item))
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
