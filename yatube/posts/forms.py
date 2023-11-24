from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """Форма поста."""

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
