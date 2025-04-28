Culturology Backend
Это бэкенд на основе Django для проекта Culturology, предоставляющий API для управления и получения информации о народах (tribes). API построен с использованием Django REST Framework и обслуживает данные для React-фронтенда.
Требования
Перед началом убедитесь, что у вас установлены следующие инструменты:

Python 3.8 или выше
pip (менеджер пакетов Python)
Virtualenv (необязательно, но рекомендуется)
Git (необязательно, для клонирования репозитория)

Инструкции по установке
Следуйте этим шагам, чтобы настроить и запустить бэкенд локально.
1. Клонирование репозитория (если применимо)
Если у вас есть Git-репозиторий, клонируйте его на свой компьютер:
git clone https://github.com/Znbmels/culturology.git
cd culturology

Или, если вы начинаете с нуля, создайте новую папку и перейдите в неё:
mkdir cultur_backend
cd culturology

2. Настройка виртуального окружения
Рекомендуется использовать виртуальное окружение для изоляции зависимостей:
python -m venv venv

Активируйте виртуальное окружение:

source venv/bin/activate((mac ос






3. Установка зависимостей
Установите необходимые пакеты Python с помощью pip:
pip install django djangorestframework
((requirements.txt забыла 

4. Инициализация Django-проекта
Если проект Django ещё не создан, инициализируйте его:
django-admin startproject cultur_backend .
python manage.py startapp tribes

5. Настройка проекта
Обновление cultur_backend/settings.py
Добавьте rest_framework и приложение tribes в список INSTALLED_APPS, а также настройте разрешения REST Framework:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tribes',
]

# Настройка разрешений для API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

Создание модели в tribes/models.py
Создайте модель для хранения данных о народах:
from django.db import models

class Tribe(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=50)
    traditions = models.TextField()
    history = models.TextField()

    def __str__(self):
        return self.name

Создание сериализатора в tribes/serializers.py
Создайте файл tribes/serializers.py и добавьте сериализатор:
from rest_framework import serializers
from .models import Tribe

class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = '__all__'

Создание представлений в tribes/views.py
Настройте представления для API:
from rest_framework import viewsets
from .models import Tribe
from .serializers import TribeSerializer

class TribeViewSet(viewsets.ModelViewSet):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
    permission_classes = []  # Открытый доступ

Настройка маршрутов в cultur_backend/urls.py
Настройте маршруты API:
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tribes.views import TribeViewSet

router = DefaultRouter()
router.register(r'tribes', TribeViewSet, basename='tribe')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

6. Применение миграций
Создайте и примените миграции для базы данных:
python manage.py makemigrations
python manage.py migrate

7. Создание суперпользователя
Создайте суперпользователя для доступа к админ-панели:
python manage.py createsuperuser

Следуйте инструкциям, чтобы задать имя пользователя, email и пароль.
8. Запуск сервера
Запустите сервер разработки Django:
python manage.py runserver 8000

Сервер будет доступен по адресу http://localhost:8000.
9. Добавление тестовых данных

Перейдите в админ-панель по адресу http://localhost:8000/admin/.
Войдите, используя данные суперпользователя.
Добавьте несколько записей в модель Tribe (например, "Казанские татары", "Сибирские татары").

10. Проверка API
API будет доступен по следующим эндпоинтам:

Получение списка народов: http://localhost:8000/api/tribes/
Получение информации о конкретном народе: http://localhost:8000/api/tribes/<id>/

Вы можете проверить API с помощью браузера или инструментов, таких как Postman.
Интеграция с фронтендом
Чтобы фронтенд (например, React-приложение) мог обращаться к этому бэкенду:

Убедитесь, что фронтенд настроен на проксирование запросов. Добавьте в package.json фронтенда:
"proxy": "http://localhost:8000"


Выполняйте запросы к API с относительными путями, например:
fetch('/api/tribes/')



Дополнительно

Если вы работаете с фронтендом на другом порту, убедитесь, что CORS настроен. Для этого установите пакет django-cors-headers:
pip install django-cors-headers

 Добавьте его в INSTALLED_APPS и настройте в settings.py:
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # Для разработки; настройте для продакшена

проверяйте апи через постман,он насстроен на получение шаблонов поэтому в браузере пока не будет отображаться))

фронтенд написан на REACT.js 
