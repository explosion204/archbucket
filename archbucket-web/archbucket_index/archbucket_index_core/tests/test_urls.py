from django.test import TestCase
from django.urls import reverse, resolve

from archbucket_index_core.views import SaveItemView, SaveCommentView, SaveRatingView, IndexView, ItemsListView, ItemDetailView, NewItemView, ModifyItemView, ModifyCommentView, SearchView, activation_email_sent, SignUpView, ProfileView, activate, SendEmailView

class TestGeneralPurposeUrls:
    def test_save_item_url(self):
        path = reverse('save_item')
        assert resolve(path).view_name == 'save_item'
        assert resolve(path).func.view_class == SaveItemView

    def test_save_comment_url(self):
        path = reverse('save_comment')
        assert resolve(path).view_name == 'save_comment'
        assert resolve(path).func.view_class == SaveCommentView

    def test_save_rating_url(self):
        path = reverse('save_rating')
        assert resolve(path).view_name == 'save_rating'
        assert resolve(path).func.view_class == SaveRatingView

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'
        assert resolve(path).func.view_class == IndexView

    def test_items_list_url(self):
        path = reverse('items_list', kwargs={'type_url': 'modules'})
        assert resolve(path).view_name == 'items_list'        
        assert resolve(path).func.view_class == ItemsListView

    def test_item_detail_url(self):
        path = reverse('item_detail', kwargs={'type_url': 'api', 'item_url': 'test_url'})
        assert resolve(path).view_name == 'item_detail'
        assert resolve(path).func.view_class == ItemDetailView

    def test_new_item_url(self):
        path = reverse('new_item', kwargs={'type_url': 'another_type'})
        assert resolve(path).view_name == 'new_item'
        assert resolve(path).func.view_class == NewItemView

    def test_modify_item_url(self):
        path = reverse('modify_item', kwargs={'type_url': 'type', 'item_url': 'url', 'operation': 'op'})
        assert resolve(path).view_name == 'modify_item'
        assert resolve(path).func.view_class == ModifyItemView

    def test_modify_comment_url(self):
        path = reverse('modify_comment', kwargs={'pk': '1', 'operation': 'op'})
        assert resolve(path).view_name == 'modify_comment'
        assert resolve(path).func.view_class == ModifyCommentView

    def test_search_url(self):
        path = reverse('search', kwargs={'type_url': 'type'})
        assert resolve(path).view_name == 'search'
        assert resolve(path).func.view_class == SearchView


class TestAccountUrls:
    def test_account_activation_sent_url(self):
        path = reverse('activation_email_sent')
        assert resolve(path).view_name == 'activation_email_sent'
        assert resolve(path).func == activation_email_sent

    def test_signup_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'
        assert resolve(path).func.view_class == SignUpView
    
    def test_profile_url(self):
        path = reverse('profile')
        assert resolve(path).view_name == 'profile'
        assert resolve(path).func.view_class == ProfileView

    def test_activate_url(self):
        path = reverse('activate', kwargs={'uidb64': 'Njc', 'token': '5gg-0cb3b3b4f111ed7029fa'})
        assert resolve(path).view_name == 'activate'
        assert resolve(path).func == activate

    def test_send_email_url(self):
        path = reverse('email')
        assert resolve(path).view_name == 'email'
        assert resolve(path).func.view_class == SendEmailView