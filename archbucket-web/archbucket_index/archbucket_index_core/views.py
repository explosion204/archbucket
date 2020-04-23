from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from .models import Item, ItemType, Release

class IndexView(View):
    def get(self, request):
        item_types = ItemType.objects.all()
        # five latest records
        releases = Release.objects.all().order_by('-id')[0:5]

        return render(request, 'index.html', {'item_types': item_types, 'releases': releases})

class ItemsListView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'

    def get(self, request, type_url):
        items_type = ItemType.objects.get(url=type_url)
        items = Item.objects.filter(item_type__name=items_type.name)

        return render(request, 'item_list.html', {'items_type': items_type, 'items': items})

class ItemDetailView(LoginRequiredMixin,View):
    login_url = 'accounts/login'

    def get(self, request, type_url, item_url):
        item = Item.objects.get(url=item_url)

        return render(request, 'item_detail.html', {'item': item})
