from django.urls import path, include
from django.conf.urls import url

from .views import ItemsListView, IndexView, NewItemView, ItemDetailView, ModifyItemView, SaveItemView, SaveCommentView, ModifyCommentView, SaveRatingView, SearchView
from .views import activation_email_sent, activate, SignUpView, ProfileView, SendEmailView

urlpatterns = [
    url(r'^account_activation_sent$', activation_email_sent, name='activation_email_sent'),
    url(r'^save_item$', SaveItemView.as_view(), name='save_item'),
    url(r'^save_comment$', SaveCommentView.as_view(), name='save_comment'),
    url(r'^save_rating$', SaveRatingView.as_view(), name='save_rating'),
    url(r'^accounts/signup$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/profile$', ProfileView.as_view(), name='profile'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^items/(?P<type_url>\w+)/new_item$', NewItemView.as_view()),
    url(r'^items/(?P<type_url>\w+)$', ItemsListView.as_view()),
    url(r'^items/(?P<type_url>\w+)/search$', SearchView.as_view(), name='search'),
    url(r'^items/(?P<type_url>\w+)/(?P<item_url>\w+)$', ItemDetailView.as_view()),
    url(r'^items/(?P<type_url>\w+)/(?P<item_url>\w+)/(?P<operation>\w+)$', ModifyItemView.as_view()),
    url(r'^comment/(?P<pk>\w+)/(?P<operation>\w+)$', ModifyCommentView.as_view()),
    url(r'^send_email$', SendEmailView.as_view(), name='email'),
    url(r'^$', IndexView.as_view(), name='index'),
]
