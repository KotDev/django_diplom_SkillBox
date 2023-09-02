from django.db.models import Case, When

from product.models import Product
from shop.models import Category


def filter_product(data_request) -> dict:
    """Функция для фильтрации продукта"""

    data = {
        "title__icontains": data_request.get(
            "filter[name]"
        ),  # Фильтр по названию продукта
        "price__lte": data_request.get("filter[maxPrice]"),  # Фильтр по макс цене
        "price__gte": data_request.get("filter[minPrice]"),  # Фильтр по мин цене
        "freeDelivery": True
        if eval(data_request.get("filter[freeDelivery]").title())
        else None,  # Фильтр по доставке
        "available": eval(
            data_request.get("filter[available]").title()
        ),  # Фильтр по наличии продукта
        "category_id": data_request.get("category"),  # Фильтр по категории
        "tags__in": data_request.get("tags[]"),  # Получаем тэги
    }  # Получаем словарь по фильтру из request
    for key in data.copy():
        if data[key] is None:  # Проверяем значения ключа
            data.pop(key)  # Удаляем ключи со значением None
    if data.get("category_id"):  # Проверяем удалилась ли категория из data
        if Category.objects.get(
            id=data.get("category_id")
        ).parent_id:  # Проверяем  id категории на субкатегорию
            return data
        else:
            # Получаем все субкатегории категории
            data["category_id__in"] = list(
                Category.objects.filter(parent_id=data.get("category_id"))
            )
            data.pop("category_id")  # Удаляем id категории
    return data


def filter_sorted(data_request, query):
    """Функция для сортировки продукта"""

    sort = data_request.get("sort")  # Получаем название сортировки
    if data_request.get("sortType") == "dec":  # Проверяем тип сортировки
        sort = "-" + sort  # Сортировка по убыванию
    if "rating" in sort:  # Сортировка по рейтингу продукта
        if "-" in sort:
            reverse = False  # Сортировка по убыванию
        else:
            reverse = True  # Сортировка по возрастанию
        ratings_list = sorted(
            [(product.id, product.rating) for product in query],
            key=lambda x: x[1],
            reverse=reverse,
        )
        # Сортируем нужные продукты по рейтингу
        pk_list = [
            idx for idx, rating in ratings_list
        ]  # Получаем id отсортированных продуктов
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)]
        )  # Создаём объект для order_by
        queryset = Product.objects.filter(pk__in=pk_list).order_by(
            preserved
        )  # Фильтруем продукты по id и order_by
        return queryset
    return query.order_by(sort)


def filter_popular_product(query) -> list:
    """Функция для фильтрации популярных продуктов"""
    products = sorted(list(query), key=lambda i: (i.sorted_index, len(i.orders.all())))
    # Сортируем продукты по кол-ву заказов
    return products
