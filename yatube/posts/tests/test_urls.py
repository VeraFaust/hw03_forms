from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тест-название группы',
            slug='test_slug',
            description='Тест-описание группы',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )

    def setUp(self):
        self.other_user = Client()
        self.post_auth = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_other_user_urls_status_code(self):
        """Проверка доступа для неавторизованного пользователя"""
        field_urls_code = {
            reverse('posts:index'): HTTPStatus.OK == 200,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): HTTPStatus.OK,
            reverse(
                'posts:profile',
                kwargs={'username': self.user}): HTTPStatus.OK,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}): HTTPStatus.OK,
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}): HTTPStatus.NOT_FOUND,
            reverse(
                'posts:post_create'): HTTPStatus.NOT_FOUND,
        }
        for url, template in field_urls_code.items():
            with self.subTest(url=url):
                response = self.other_user.get(url)
                self.assertEqual(response, template)

    def test_authorized_user_urls_status_code(self):
        """Проверка доступа для авторизованного пользователя"""
        field_urls_code = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): HTTPStatus.OK,
            reverse(
                'posts:profile',
                kwargs={'username': self.user}): HTTPStatus.OK,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}): HTTPStatus.OK,
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}): HTTPStatus.NOT_FOUND,
            reverse(
                'posts:post_create'): HTTPStatus.OK,
        }
        for url, template in field_urls_code.items():
            with self.subTest(url=url):
                response = self.authorized_user.get(url)
                self.assertEqual(response, template)
    
    def test_author_user_urls_status_code(self):
        """Проверка доступа для автора"""
        field_urls_code = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): HTTPStatus.OK,
            reverse(
                'posts:profile',
                kwargs={'username': self.user}): HTTPStatus.OK,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}): HTTPStatus.OK,
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}): HTTPStatus.OK,
            reverse(
                'posts:post_create'): HTTPStatus.OK,
        }
        for url, template in field_urls_code.items():
            with self.subTest(url=url):
                response = self.post_auth.get(url)
                self.assertEqual(response, template)

    def test_page_404_return_for_unexisting_page(self):
        """Возврат ошибки 404 при запросе к unexisting_page """
        self.page_url = '/unexisting/'
        other_response = self.other_user.get(self.page_url, follow=True)
        authorized_response = self.authorized_user.get(self.page_url)
        auth_response = self.post_auth.get(self.page_url)

        self.assertEqual(other_response.reason_phrase, 'Not Found')
        self.assertEqual(authorized_response.reason_phrase, 'Not Found')
        self.assertAlmostEqual(auth_response.reason_phrase, 'Not Found')

    def test_create_url_redirect_anonymous_on_admin_login(self):
        """Страница создания поста перенаправит любого
        пользователя на страницу логина"""
        response = self.other_user.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_post_edit_page_dont_exists_for_guest_client(self):
        """Страница редактирования поста перенаправит любого
        пользователя на страницу логина"""

        response = self.other_user.get(
            self.post.pk,
            follow=True
        )
        self.assertRedirects(
            response,
            '/auth/login/?next=/posts/{post_id}/edit/'

        )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): 
                'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user}):
                'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}):
                'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}):
                'posts/create_post.html',
            reverse(
                'posts:post_create'):
                'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_user.get(url)
                self.assertTemplateUsed(response, template)