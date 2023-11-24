import shutil
import tempfile

from posts.forms import PostForm
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post, Group

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тест-заголовок группы',
            slug='first',
            description='Тест-описание группы',
        )
        cls.post = Post.objects.create(
            text='Тест-описание поста',
            author=cls.user,
            group=cls.group,
        )
        cls.form = PostForm

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.other_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_posts(self):
        """Валидная форма создает пост в Post"""
        posts_count = Post.objects.count()
        """Пост с картинкой добавляется в бд"""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name = 'small.gif',
            content = small_gif,
            content_type = 'image/gif'
        )
        form_data = {
            'title': 'Тест-заголовок группы',
            'text': 'Тест-описание поста',
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'auth'})
        )
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(
            Post.objects.filter(
                slug='test-slug',
                text='Тест-описание поста',
                image='posts/small.gif'
            ).exists()
        )

    def test_cant_create_existing_slug(self):
        posts_count = Post.objects.count()
        form_data = {
            'title': 'Заголовок из формы',
            'text': 'Текст из формы',
            'slug': 'first',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response,
            'form',
            'slug',
            'Адрес "first" уже существует, придумайте уникальное значение'
        )
        self.assertEqual(response.status_code, 200)

    def test_cant_create_post(self):
        """Авторизированный пользователь может создавать пост"""
        data = {
            'text': 'Текст из формы',
            'group.title': 'group',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=data,
            follow=True,
        )
        path = reverse('posts:profile', kwargs={'username': 'auth'})
        self.assertTrue(
            Post.objects.filter(
                text='Текст из формы',
            ).exists()
        )
        return [response, path]

    def test_can_edit_post(self):
        """Авторизированный пользователь может редактировать пост"""
        form_data = {
            'text': 'Текст из формы',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True,
        )
        path = reverse(
            'posts:post_detail', kwargs={'post_id': '1'})
        new_post = Post.objects.get(id='1')
        self.assertEqual(new_post.id, self.post.id)
        self.assertNotEqual(new_post.text, self.post.text)
        return [response, path]

    def test_cant_create_post(self):
        """Неавторизированный пользователь не может создавать пост"""
        form_data = {
            'text': 'Текст из формы',
            'group.title': 'group',
        }
        response = self.other_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        return [response, '/auth/login/?next=/create/']