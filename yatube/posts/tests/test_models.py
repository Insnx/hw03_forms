from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    #добавляем декоратор , класс метод принимает на вход класс
    @classmethod
    def setUpClass(cls):
        super().setUpClass() #дополняем функционалом из родителя
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )


    def test_models_have_correct_object_names(self): #self обьект класса 
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(self.group.title, 'Тестовая группа', 'Не совпадает название группы')
        self.assertEqual(self.post.text[:15], 'Тестовая пост', 'Не совпадает текст поста')
