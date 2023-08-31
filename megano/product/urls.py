from django.urls import path

from .views import (ProductsDetailView,
                    ReviewProductView,)

urlpatterns = [
    path('product/<id>', ProductsDetailView.as_view(), name='product'),
    path('product/<id>/reviews', ReviewProductView.as_view(), name='review')

]