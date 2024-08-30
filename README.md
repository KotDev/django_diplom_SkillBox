
 <div align="center">
 <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9-__tiF2dsxD0-ro5O6rnGx63DxxpukFmig&s)" width="500">
 </div>

# Интернет магазин Megano (Pet-project)

Интернет магазин разработанный на Django Rest


## 🛠 Стэк
**Backend:** Python 3, Django 4, DRF

**Frontend:** JS, CSS, HTML

**Linterst:** Black, Mypy

**DB:** Django ORM, Sqlite








## Запуск проекта

Необходимо склонировать репозиторий на локальное устройство

```bash
  git clone https://github.com/OreoLand123/django_diplom_SkillBox.git
```

Перейти в репозиторий с проектом куда вы склонировали репозиторий

```bash
  cd your-project
```

Переходим в requirements.txt и изменяем строку diploma-frontend на абсолютный путь где хранится проект, который вы склонировали, это необходимо для установки файла фронтенда
```bash
  diploma-frontend @ file:your-disc/PycharmProjects/django_diplom_SkillBox/diploma-frontend/dist/diploma-frontend-0.6.tar.gz#sha256=1dbc829d230c282fac60273448bb15389378304d82fa53bb16e16304480b9664

```

Устанавливаем зависимости из requirements.txt
```bash
  pip install -r requirements.txt
```

Запускаем приложение
```bash
  python3 manage.py runserver
```




## API 

Для просмотра полной документации API приложения необходимо перейти по пути
```bash
cd your-ptoject/diploma-frontend/swagger
```
и скопировать содержимое swagger.yaml и вставить его в https://editor.swagger.io/




## Главная страница магазина

![App Screenshot](https://github.com/OreoLand123/django_diplom_SkillBox/raw/master/diploma-frontend/root-page.png)

## Приложения которые бали реализованны в проекте:
- accounts - приложение по работе с профилем (изменение, вход, выход, регистрация и т.д)
- cart - приложение корзины (удаление товара из корзины, добавление товара в корзину и т.д)
- order - приложение по работе с заказами (создание заказа, просмотр заказа и т.д)
- product - приложение по работе с товарами (создать продукт, удалить продукт, оставить коммент к продукту и т.д)
- shop - приложение по работе с основной страницей магазина (фильтрация по категориям, цене. Пагинация страниц и т.д)

### БД

Для бзы данных были созданы фикстуры в каждом приложении, а так же для удобства проверки бд была загружена в репозиторий.


## Автор

- [@KotDev](https://github.com/KotDev)

