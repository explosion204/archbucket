import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View
from django.views.generic import ListView, FormView
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

from .accounts import email
from .accounts.tokens import account_activation_token
from .forms import ItemForm, CommentForm, RatingForm, SignUpForm, SetPasswordForm, SendEmailForm
from .models import Item, ItemType, Release, Comment, Rating, User, Profile

from archbucket_index.settings import TEMPLATES_DIR

# GENERAL-PURPOSE VIEWS

class IndexView(View):
    '''Main page'''
    def get(self, request):
        item_types = ItemType.objects.all()
        # five latest records
        releases = Release.objects.all().order_by('-id')[0:5]

        return TemplateResponse(request, 'core/index.html', {'types': item_types, 'releases': releases})


class ItemsListView(ListView):
    '''List of items'''
    paginate_by = 10
    model = Item
    template_name = 'core/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context['items_type'] = ItemType.objects.get(url=self.kwargs['type_url'])
        context['user_profile'] = Profile.objects.get(user=self.request.user)
        context['search'] = False

        return context

    def get_queryset(self):
        items_type = ItemType.objects.get(url=self.kwargs['type_url'])
        if not self.request.user.is_anonymous:
            return Item.objects.filter(Q(item_type__name=items_type.name), Q(status='v') | Q(user=self.request.user))
        else:
            return Item.objects.filter(Q(item_type__name=items_type.name), Q(status='v'))


class SearchView(ListView):
    paginate_by = 10
    model = Item
    template_name = 'core/item_list.html'

    def get_queryset(self):
        return Item.objects.filter(name__icontains=self.request.GET.get('query'))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['items_type'] = ItemType.objects.get(url=self.kwargs['type_url'])
        context['user_profile'] = Profile.objects.get(user=self.request.user)
        context['search'] = True
        context['query'] = self.request.GET.get('query')

        return context

class ItemDetailView(View):
    '''Page with details of concrete item'''

    def get(self, request, type_url, item_url):
        item = Item.objects.get(url=item_url)
        comments = Comment.objects.filter(item__url=item_url)

        # permissions
        can_comment = False
        can_rate = False
        can_edit = False
        can_remove = False

        if not request.user.is_anonymous and request.user.profile.verified:
            can_comment = True
            can_rate = True

            if item.user == request.user or request.user.is_staff:
                can_edit = True
                can_remove = True

            comment_form = CommentForm(initial={'item': item, 'user': request.user})

            # rating
            is_user_rated = True if len(Rating.objects.filter(Q(user=request.user), Q(item=item))) != 0 else False
            user_rating = 0 if not is_user_rated else Rating.objects.get(Q(user=request.user), Q(item=item)).value
            rating_form = RatingForm(initial={'item': item, 'user': request.user})

            if item.status == 'v' or item.user == request.user:
                return TemplateResponse(request, 'core/item_detail.html', {
                    'item': item,
                    'can_comment': can_comment,
                    'can_rate': can_rate,
                    'can_edit': can_edit,
                    'can_remove': can_remove,
                    'comment_form': comment_form, 
                    'rating_form': rating_form,
                    'comments': comments, 
                    'user_rating': user_rating,
                    'is_user_rated': is_user_rated
                    })

        
        return TemplateResponse(request, 'core/item_detail.html', {
            'item': item,
            'can_comment': can_comment,
            'can_rate': can_rate,
            'can_edit': can_edit,
            'can_remove': can_remove,
            'comments': comments, 
            'item_rating': item.item_rating,
            })


class NewItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Create new item instance'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def get(self, request, type_url):
        status = 'v' if request.user.is_staff else 'n'
        form = ItemForm(initial={
            'url': None, 
            'user': request.user, 
            'status': status, 
            'votes': 0, 
            'item_type': ItemType.objects.get(url=type_url)})

        return TemplateResponse(request, 'core/modify_item.html', {'form': form, 'item_type_url': type_url, 'operation': 'add'})


class ModifyItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Page which provides functionality of editing/removing'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def get(self, request, type_url, item_url, operation):
        item = Item.objects.get(url=item_url)
        if item.user == request.user or request.user.is_staff:
            if operation == 'remove':
                item.delete()

                return redirect(reverse('items_list', kwargs={'type_url': type_url}))

            if operation == 'edit':
                form = ItemForm(initial={
                    'name': item.name,
                    'url': item_url,
                    'item_type': ItemType.objects.get(url=type_url),
                    'description': item.description,
                    'source_code': item.source_code,
                    'documentation': item.documentation
                })
                return TemplateResponse(request, 'core/modify_item.html', {'form': form, 'item_type_url': type_url, 'operation': 'edit'})
            
        return redirect('index')

class SaveItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Save edited or created Item instance'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['url'] != None:
                query = Item.objects.filter(url=form.cleaned_data['url'])

            # if form.cleaned_data['status'] == 'v' and not request.user.is_staff:
            #     return redirect('index')

            if query.exists():
                item = query.first()
                item.name = form.cleaned_data['name']
                item.description = form.cleaned_data['description']
                item.source_code = form.cleaned_data['source_code']
                item.documentation = form.cleaned_data['documentation']
            else:
                try:
                    latest_item = Item.objects.latest('pk')
                    item_id = latest_item.id
                except ObjectDoesNotExist:
                    item_id = 0

                form.cleaned_data['url'] = str(item_id + 1) + '_' + slugify(form.cleaned_data['name'])

                item = Item(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    source_code=form.cleaned_data['source_code'],
                    documentation=form.cleaned_data['documentation'],
                    item_type=form.cleaned_data['item_type'],
                    user=request.user,
                    url=str(item_id + 1) + '_' + slugify(form.cleaned_data['name'])
                )

            item.save()

            return redirect(reverse('item_detail', kwargs={'type_url': item.item_type.url, 'item_url': item.url}))


class SaveCommentView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Save created Comment instance'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def post(self, request):
        form = CommentForm(request.POST)

        if form.is_valid():
            item=form.cleaned_data['item']

            Comment(
                user=form.cleaned_data['user'],
                item=item,
                text=form.cleaned_data['text']
            ).save()

            return redirect(reverse('item_detail', kwargs={'type_url': item.item_type.url, 'item_url': item.url}))


class ModifyCommentView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Remove Comment instance'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def get(self, request, pk, operation):
        comment = Comment.objects.get(id=pk)

        if comment.user == request.user or request.user.is_staff:
            if operation == 'remove':
                comment.delete()

                return redirect(reverse('item_detail', kwargs={'type_url': comment.item.item_type.url, 'item_url': comment.item.url}))


        return redirect('index')


class SaveRatingView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''Save Rating instance'''
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.profile.verified

    def handle_no_permission(self):
        return redirect('index')

    def post(self, request):
        form = RatingForm(request.POST)
        
        if form.is_valid():
            item = item=form.cleaned_data['item']
            Rating(
                item=item,
                user=form.cleaned_data['user'],
                value=form.cleaned_data['value']
            ).save()

            return TemplateResponse(request, 'core/operation_result.html', {
                'op_name': 'save rating',
                'status': 'success',
                'message': 'Rating successfully saved.'
                })

            return redirect(reverse('item_detail', kwargs={'type_url': item.item_type.url, 'item_url': item.url}))

        return redirect('index')

# USER-RELATED VIEWS

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    )

class ProfileView(LoginRequiredMixin, View):
    """User's profile"""
    login_url = '/accounts/login'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = SetPasswordForm(initial={'user': request.user})

        return TemplateResponse(request, 'users/profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        form = SetPasswordForm(request.POST)
        profile = Profile.objects.get(user=request.user)

        if form.is_valid():
            try:
                validate_password(form.cleaned_data['new_password1'])
            except ValidationError as e:
                form.add_error('new_password1', e)
                return TemplateResponse(request, 'users/profile.html', {'form': form, 'profile': profile})

            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)

            return TemplateResponse(request, 'users/profile.html', {'form': form, 'profile': profile, 'message': 'Password successfully changed.'})
            
        return TemplateResponse(request, 'users/profile.html', {'form': form, 'profile': profile})

class SendEmailView(UserPassesTestMixin, View):
    login_url = '/accounts/login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        form = SendEmailForm(request.POST)

        if form.is_valid():
            users = form.cleaned_data['users']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            for user in users:
                email.send_email(user.email, subject, message)

            messages.info(request, 'Emails successfully sent.')
            
            return redirect('/admin/archbucket_index_core/user/')

        return redirect('index')

class SignUpView(UserPassesTestMixin, View): 
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse('profile'))

    def get(self, request):
        form = SignUpForm()
        
        return TemplateResponse(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            template = env.get_template('registration/activation_email.html')
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"http://{ get_current_site(request).domain }/activate/{uid}/{token}/"

            message = template.render(
                user=user,
                link=activation_link,
                time=datetime.datetime.now()
            )

            email.send_email(user.email, 'Activate your account', message)

            return redirect('activation_email_sent')
        
        return render(request, 'registration/register.html', {'form': form})

def activation_email_sent(request):
    return render(request, 'registration/activation_email_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.profile.verified = True
        user.save()
        return redirect('index')
    else:
        return TemplateResponse(request, 'registration/account_activation_invalid.html')
