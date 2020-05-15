from django.utils import timezone
from mixer.backend.django import mixer
import pytest

from datetime import datetime

from archbucket_index_core.models import User, Profile, Item, ItemType

@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestModels:
    def test_update_user_profile(self):
        user = mixer.blend('archbucket_index_core.User', username='test_user')
        assert Profile.objects.get(user=user).user == user

    def test_item_save(self):
        item_type = mixer.blend('archbucket_index_core.ItemType', url='test_url1')
        item = mixer.blend('archbucket_index_core.Item', item_type=item_type, url='test_url2')

        assert item.created.year == datetime.now().year
        assert item.created.month == datetime.now().month
        assert item.created.day == datetime.now().day
        assert item.created.minute == datetime.now().minute
        assert item.modified.year == datetime.now().year
        assert item.modified.month == datetime.now().month
        assert item.modified.day == datetime.now().day
        assert item.modified.minute == datetime.now().minute

    @pytest.mark.parametrize('initial_rating, new_initial_rating, second_rating, result_rating',  
            [(1, 2, 4, 3), (2, 3, 1, 2), (3, 4, 5, 4.5), (4, 5, 3, 4), (5, 1, 2, 1.5)]
    )
    def test_rating_save(self, initial_rating, new_initial_rating, second_rating, result_rating):
        item_type = mixer.blend('archbucket_index_core.ItemType', url='test_url1')
        item = mixer.blend('archbucket_index_core.Item', item_type=item_type, url='test_url2')

        assert item.item_rating == 0
        assert item.votes == 0

        user1 = mixer.blend('archbucket_index_core.User')
        user2 = mixer.blend('archbucket_index_core.User')

        rating = mixer.blend('archbucket_index_core.Rating', user=user1, item=item, value=initial_rating)
        assert rating.value == initial_rating
        assert item.item_rating == initial_rating
        rating.value = new_initial_rating
        rating.save()
        assert rating.value == new_initial_rating
        assert item.item_rating == new_initial_rating

        rating = mixer.blend('archbucket_index_core.Rating', user=user2, item=item, value = second_rating)
        assert rating.value == second_rating
        assert item.item_rating == result_rating




