from django.urls import path

from .views import (CategoryView,
                    CatalogView,
                    ProductLimitedView,
                    BannersView,
                    TagsView,
                    PopularView,
                    SaleView)

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('products/limited', ProductLimitedView.as_view(), name='products_limited'),
    path('banners/', BannersView.as_view(), name='banners'),
    path('tags/', TagsView.as_view(), name='tags'),
    path('products/popular', PopularView.as_view(), name='products_popular'),
    path('sales/', SaleView.as_view(), name='sale')
]