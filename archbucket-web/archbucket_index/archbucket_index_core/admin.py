from django.contrib import admin
from .models import Rating, Item, ItemType, Comment, Release

admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Release)