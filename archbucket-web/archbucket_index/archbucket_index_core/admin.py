from django.contrib import admin
from django.contrib.admin import helpers
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .models import Rating, Item, ItemType, Comment, Release, Profile, User
from .forms import SendEmailForm

from .accounts.email import send_email

admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Release)
admin.site.register(Profile)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    actions = ['send_email', ]

    def send_email(self, request, queryset):
        form = SendEmailForm(initial={'users': queryset})

        return render(request, 'users/send_email.html', {'form': form})
