from django.urls import path, include
from django.conf.urls import url

from .views import ItemsListView, IndexView, ItemDetailView, ModifyItemView, SaveItemView, SaveCommentView, CommentView, SaveRatingView

urlpatterns = [
    url('save_item', SaveItemView.as_view(), name='save_item'),
    url('save_comment', SaveCommentView.as_view(), name='save_comment'),
    url('save_rating', SaveRatingView.as_view(), name='save_rating'),

    path('', IndexView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:type_url>', ItemsListView.as_view()),
    path('<int:pk>/<str:operation>', CommentView.as_view()),
    path('<slug:type_url>/<slug:item_url>', ItemDetailView.as_view()),
    path('<slug:type_url>/<slug:item_url>/<str:operation>', ModifyItemView.as_view())
]
