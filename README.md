# Социальная сеть «Yatube»

## Описание:
Yatube - это социальная сеть.  
В этом проекте реализовано следующее:
- Создана форма регистрации, авторизации и выхода из аккаунта;
- Создана форма для создания/редактирования нового поста;
- Настроена эмуляция работы почтового сервера;
- Создан профайл пользователя с отображением постов автора;
- Добавлены разделы "Об авторе" и "Технологии";
- Реализована возможность просмотра информации каждого поста;
- Подключен паджинатор;
- Создан контекст-процессор, добавляющий текущий год на все страницы;
- Создана навигация по страницам.

## Технологии:
- Python;
- Django;
- Git;
- HTML;
- CSS;
- Bootstrap;
- Django ORM;
- SQL.

## Запуск проекта:
- Клонируйте репозиторий:
```
git clone https://github.com/VeraFaust/hw03_forms.git
```

- Установите и активируйте виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

- Установите зависимости из файла requirements.txt:
```
py -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

- В папке с файлом manage.py запустите миграции:
```
py manage.py makemigrations
```
```
py manage.py migrate
```

- В папке с файлом manage.py создайте админа и запустите проект:
```
py manage.py createsuperuser
```
```
python manage.py runserver
```

- Остановить работу:
```
Ctrl+C
```

## Ссылки:
- Сайт: http://127.0.0.1:8000/
- Админ-зона: http://127.0.0.1:8000/admin

Благодаря формам, создавать посты, группы и аккаунты можно на самом сайте в роли обычного пользователя.

## Автор
Вера Фауст
