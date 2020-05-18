from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import Client, RequestFactory
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
import pytest

from archbucket_index_core.accounts.tokens import account_activation_token
from archbucket_index_core.admin import CustomUserAdmin
from archbucket_index_core.models import User, Item, Comment, Profile
from archbucket_index_core.views import IndexView, ItemsListView, SearchView, ItemDetailView, NewItemView, ModifyItemView, SaveItemView, SaveCommentView, ModifyCommentView, SaveRatingView
from archbucket_index_core.views import ProfileView, SendEmailView, SignUpView, activate

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def anonymous_user():
    return AnonymousUser()

@pytest.fixture
def not_staff_user(db):
    user = mixer.blend('archbucket_index_core.User', is_staff=False, password='test_pass123')
    user.profile.verified = True
    return user

@pytest.fixture
def staff_user(db):
    user = mixer.blend('archbucket_index_core.User', is_staff=True, password='test_pass123')
    user.profile.verified = True
    return user

@pytest.fixture
def test_type(db):
    return mixer.blend('archbucket_index_core.ItemType', name='test_type', url='test_type_url')

def middleware_anotate(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware()
    middleware.process_request(request)
    request.session.save()


@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestGeneralPurposeViews:
    def test_index_view(self, client):
        path = reverse('index')

        assert client.get(path).status_code == 200

    def test_items_list_view_authenticated(self, request_factory, test_type, staff_user, not_staff_user):
        item1 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url1', status='v')
        item2 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url2', status='n')
        path = reverse('items_list', kwargs={'type_url': test_type.url})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ItemsListView()
        view.setup(request)
        view.kwargs['type_url'] = test_type.url

        assert len(list(view.get_queryset())) == 2

        request.user = staff_user
        view.setup(request)
        view.kwargs['type_url'] = test_type.url

        assert len(list(view.get_queryset())) == 1

        view.object_list = view.get_queryset()
        context = view.get_context_data()

        assert context['search'] == False

    def test_items_list_view_not_authenticated(self, request_factory, test_type, not_staff_user, anonymous_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url1', status='n')
        path = reverse('items_list', kwargs={'type_url': test_type.url})
        request = request_factory.get(path)
        request.user = anonymous_user

        view = ItemsListView()
        view.setup(request)
        view.kwargs['type_url'] = test_type.url

        assert len(list(view.get_queryset())) == 0

    def test_search_view(self, request_factory, test_type, not_staff_user):
        path = reverse('search', kwargs={'type_url': test_type.url})
        request = request_factory.get(path, {'query': 'foo'})
        request.user = not_staff_user

        view = SearchView()
        view.setup(request)
        view.kwargs['type_url'] = test_type.url
        view.object_list = view.get_queryset()
        context = view.get_context_data()

        assert context['search'] == True

    @pytest.mark.parametrize('query', ['foo', 'bar', 'Frank Sinatra', 'barrr', 'ffoof'])
    def test_search_view_results(self, request_factory, test_type, not_staff_user, query):
        item1 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, name='foo', item_type=test_type, url='test_item_url1', status='v')
        item2 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, name='bar', item_type=test_type, url='test_item_url2', status='v')
        item3 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, name='fof', item_type=test_type, url='test_item_url3', status='v')
        item4 = mixer.blend('archbucket_index_core.Item', user=not_staff_user, name='bar', item_type=test_type, url='test_item_url4', status='v')
        path = reverse('search', kwargs={'type_url': test_type.url})
        request = request_factory.get(path, {'query': query})
        request.user = not_staff_user

        view = SearchView()
        view.setup(request)
        view.kwargs['type_url'] = test_type.url
        objects = view.get_queryset()

        for obj in objects:
            assert query in obj.name

        view.object_list = view.get_queryset()
        context = view.get_context_data()

        assert context['query'] == query
        
    def test_item_detail_view_not_authenticated(self, request_factory, test_type, not_staff_user, anonymous_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('item_detail', kwargs={'type_url': test_type.url, 'item_url': item.url})
        request = request_factory.get(path)
        request.user = anonymous_user

        view = ItemDetailView()
        view.setup(request)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['can_comment'] == False
        assert context['can_rate'] == False
        assert context['can_edit'] == False
        assert context['can_remove'] == False


    def test_item_detail_view_authenticated_not_author_not_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=staff_user, item_type=test_type, url='test_item_ur1', status='v')
        path = reverse('item_detail', kwargs={'type_url': test_type.url, 'item_url': item.url})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ItemDetailView()
        view.setup(view)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['can_comment'] == True
        assert context['can_rate'] == True
        assert context['can_edit'] == False
        assert context['can_remove'] == False

    def test_item_detail_view_authenticated_author_not_staff(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('item_detail', kwargs={'type_url': test_type.url, 'item_url': item.url})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ItemDetailView()
        view.setup(view)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['can_edit'] == True
        assert context['can_remove'] == True

    def test_item_detail_view_authenticated_not_author_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('item_detail', kwargs={'type_url': test_type.url, 'item_url': item.url})
        request = request_factory.get(path)
        request.user = staff_user

        view = ItemDetailView()
        view.setup(view)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['can_edit'] == True
        assert context['can_remove'] == True

    def test_item_detail_view_is_user_rated(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('item_detail', kwargs={'type_url': test_type.url, 'item_url': item.url})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ItemDetailView()
        view.setup(view)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['is_user_rated'] == False

        rating = mixer.blend('archbucket_index_core.Rating', user=not_staff_user, item=item, value=1)
        context = view.get(request, test_type.url, item.url).context_data

        assert context['is_user_rated'] == True

    def test_new_item_view(self, request_factory, not_staff_user, staff_user, test_type):
        path = reverse('new_item', kwargs={'type_url': test_type.url})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = NewItemView()
        view.setup(request)
        context = view.get(request, test_type.url).context_data

        assert context['form'].initial['status'] == 'n'

        request.user = staff_user
        view.setup(request)
        context = view.get(request, test_type.url).context_data

        assert context['form'].initial['status'] == 'v'

    def test_modify_item_view_authenticated_not_author_not_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('modify_item', kwargs={'type_url': test_type.url, 'item_url': item.url, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ModifyItemView()

        assert view.get(request, test_type.url, item.url, 'edit').status_code == 302
        assert view.get(request, test_type.url, item.url, 'remove').status_code == 302

    def test_modify_item_view_authenticated_author_not_staff(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('modify_item', kwargs={'type_url': test_type.url, 'item_url': item.url, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ModifyItemView()

        assert view.get(request, test_type.url, item.url, 'edit').status_code == 200
        assert view.get(request, test_type.url, item.url, 'remove').status_code == 302

    def test_modify_item_view_authenticated_not_author_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('modify_item', kwargs={'type_url': test_type.url, 'item_url': item.url, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = staff_user

        view = ModifyItemView()

        assert view.get(request, test_type.url, item.url, 'edit').status_code == 200
        assert view.get(request, test_type.url, item.url, 'remove').status_code == 302

    def test_save_item_view(self, request_factory, test_type, not_staff_user):
        path = reverse('save_item')
        request = request_factory.post(path, {'name': 'name', 'description': 'desc', 'source_code': 'src', 'documentation': 'docs', 'status': 'v', 'item_type': '1', 'votes': '0'})
        request.user = not_staff_user

        view = SaveItemView()
        view.post(request)

        assert Item.objects.all()[0].url == '1_name'

        request = request_factory.post(path, {'name': 'new', 'description': 'desc', 'source_code': 'src', 'documentation': 'docs', 'status': 'v', 'item_type': '1', 'votes': '0'})
        request.user = not_staff_user
        view.post(request)

        assert Item.objects.all()[1].url == '2_new'

        request = request_factory.post(path, {'name': 'new', 'description': 'desc_new', 'source_code': 'src', 'documentation': 'docs', 'status': 'v', 'item_type': '1', 'votes': '0', 'url': '1_name'})
        request.user = not_staff_user
        view.post(request)

        assert Item.objects.all()[0].description == 'desc_new'

    def test_save_comment_view(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('save_comment')
        request = request_factory.post(path, {'text': 'text', 'item': '1', 'user': not_staff_user.pk})
        request.user = not_staff_user

        view = SaveCommentView()
        view.setup(request)

        assert view.post(request).status_code == 302

    def test_modify_comment_view_authenticated_not_author_not_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        comment = mixer.blend('archbucket_index_core.Comment', user=staff_user, item=item, text='text')
        path = reverse('modify_comment', kwargs={'pk': comment.pk, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ModifyCommentView()
        view.setup(request)

        assert view.get(request, comment.pk, 'edit').status_code == 302
        assert view.get(request, comment.pk, 'remove').status_code == 302

    def test_modify_comment_view_authenticated_author_not_staff(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        comment = mixer.blend('archbucket_index_core.Comment', user=not_staff_user, item=item, text='text')
        path = reverse('modify_comment', kwargs={'pk': comment.pk, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ModifyCommentView()
        view.setup(request)

        assert view.get(request, comment.pk, 'remove').status_code == 302

    def test_modify_comment_view_authenticated_not_author_staff(self, request_factory, test_type, not_staff_user, staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        comment = mixer.blend('archbucket_index_core.Comment', user=not_staff_user, item=item, text='text')
        path = reverse('modify_comment', kwargs={'pk': comment.pk, 'operation': 'edit'})
        request = request_factory.get(path)
        request.user = staff_user

        view = ModifyCommentView()
        view.setup(request)

        assert view.get(request, comment.pk, 'remove').status_code == 302

    def test_save_rating_view(self, request_factory, test_type, not_staff_user):
        item = mixer.blend('archbucket_index_core.Item', user=not_staff_user, item_type=test_type, url='test_item_url', status='v')
        path = reverse('save_rating')
        request = request_factory.post(path, {'user': not_staff_user.pk, 'item': item.pk, 'value': '4'})
        request.user = not_staff_user

        view = SaveRatingView()
        view.setup(request)

        assert view.post(request).status_code == 200


@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestUserRelatedViews:
    def test_profile_view_authenticated_get(self, request_factory, not_staff_user):
        path = reverse('profile')
        request = request_factory.get(path)
        request.user = not_staff_user

        view = ProfileView()
        view.setup(request)

        assert view.get(request).status_code == 200

    def test_profile_view_authenticated_post(self, request_factory, not_staff_user, staff_user):
        path = reverse('profile')
        request = request_factory.post(path, {'user': not_staff_user, 'current_password': 'test_pass123', 'new_password1': 'fefsa6d54fd5', 'new_password2': 'fefsa6d54fd5'})
        request.user = not_staff_user

        view = ProfileView()
        view.setup(request)

        assert view.post(request).status_code == 200

    def test_send_email_admin_action(self, request_factory, staff_user):
        model = CustomUserAdmin(User, AdminSite())

        assert model.send_email(HttpRequest(), [staff_user]).status_code == 200

    def test_send_email_view(self, request_factory, not_staff_user, staff_user):
        path = reverse('email')
        request = request_factory.post(path, {'subject': 'test', 'message': 'test', 'users': [not_staff_user.pk]})
        request.user = staff_user
        middleware_anotate(request)

        view = SendEmailView()
        view.setup(request)

        assert view.post(request).status_code == 302

        request = request_factory.post(path, {'message': 'test', 'users': [not_staff_user.pk]})
        request.user = staff_user
        view.setup(request)

        assert view.post(request).status_code == 302

    def test_signup_view_not_authenticated_get(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.get(path)
        request.user = anonymous_user

        view = SignUpView()
        view.setup(request)

        assert view.get(request).status_code == 200

    def test_signup_view_not_authenticated_post(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.post(path, {'username': 'test_user', 'email': 'test@test.com', 'password1': 'eokdo254ihjb', 'password2': 'eokdo254ihjb'})
        request.user = anonymous_user

        view = SignUpView()
        view.setup(request)

        assert view.post(request).status_code == 302

        request = request_factory.post(path, {'email': 'test@test.com', 'password1': 'eokdo254ihjb', 'password2': 'eokdo254ihjb'})
        request.user = anonymous_user
        view.setup(request)

        assert view.post(request).status_code == 200

    def test_activation_email_sent(self, client):
        path = reverse('activation_email_sent')
        
        assert client.get(path).status_code == 200

    def test_activate(self, request_factory):
        user = mixer.blend('archbucket_index_core.User', username='new_user', password='test_pass123')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)

        assert activate(request, uid, token).status_code == 302
        assert activate(request, uid, token).status_code == 200
        
        uid = urlsafe_base64_encode(force_bytes('33'))
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)

        assert activate(request, uid, token).status_code == 200