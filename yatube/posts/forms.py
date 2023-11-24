from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from pytils.translit import slugify

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа нового поста',
        }
        labels = {
            'text': 'Текст поста'
        }

class PostCreateForm(forms.ModelForm):
    """Форма для создания поста"""
    class Meta:
        model = Post
        fields = '__all__'

    def clean_slug(self):
        """Обрабатывает случай, если slug не уникален"""
        cleaned_data = super().clean
        slug = cleaned_data.get('slug')
        if not slug:
            title = cleaned_data.get('title')
            slug = slugify(title)[:100]
        if Post.objects.filter(slug=slug).exists():
            raise ValidationError(
                f'Адрес "{slug}" уже существует, '
                'придумайте уникальное значение'
            )
        return slug