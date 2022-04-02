from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from ..models import Post, Group

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() #дополняем функционалом из родителя
        cls.user_author = User.objects.create_user(username='auth')
        cls.user_simple = User.objects.create_user(username='left')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовая пост',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        # self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user_simple)
        # Создаем третьего клиента
        self.authorized_client_author = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user_author)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_group_added_url_exists_at_desired_location(self):
        """Страница /group/test-slug/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_username_list_url_exists_at_desired_location(self):
        """Страница /username/auth/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/username/auth/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_post_detail_url_exists_at_desired_location_authorized(self):
        """Страница /post/id/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get(f'/post/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    # Проверяем редиректы для неавторизованного пользователя
    def test_post_edit_url_redirect_nonauth(self):
        """Страница /post/edit/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get(f'/post/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        response = self.authorized_client_author.get(f'/post/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        response = self.authorized_client.get(f'/post/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

    def test_post_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного
        пользователя.
        """
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_task_detail_url_redirect_anonymous(self):
        """Страница /unexisting_page/ выдает ошибку о несуществующей страницы
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
