from django.urls import path

from .views import ItemsListView, IndexView, ItemDetailView

urlpatterns = [
    path("", IndexView.as_view()),
    path("<slug:type_url>", ItemsListView.as_view()),
    path("<slug:type_url>/<slug:item_url>", ItemDetailView.as_view()),
]
