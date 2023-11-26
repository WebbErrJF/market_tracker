from django.test import TestCase
from users.models import Profile
from django.contrib.auth.models import User


class MessageModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='testuser',
                                             password='testpassword')
        self.test_profile = Profile.objects.get(user=self.test_user)

    def test_if_test_profile_is_instance_of_profile(self):
        self.assertTrue(isinstance(self.test_profile, Profile))

    def test_profile_image_default_value(self):
        expected_default_value = 'profile_pics/default.png'
        self.assertEqual(self.test_profile.image.name, expected_default_value)

    def test_if_instance_of_ProfileModel_returns_name_when_its_called(self):
        profile_representation = str(self.test_profile)
        self.assertEqual(profile_representation, self.test_user.username)

    def test_profile_upload_to_value(self):
        expected_default_value = 'profile_pics/'
        upload_to = self.test_profile._meta.get_field('image').upload_to
        self.assertEqual(upload_to, expected_default_value)
