from django.contrib import admin
from .models import Feedback, Item, ItemType, Rating, Release

admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Feedback)
admin.site.register(Rating)
admin.site.register(Release)