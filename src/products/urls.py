from django.urls import path

from .views import (AllCategoryList, AllProductList, CateogoryDetail,
                    LatestProductsList, ProductDetail, ProductDetailById,
                    search)

urlpatterns = [
    path('latest-products/', LatestProductsList.as_view()),
    path('all-products/', AllProductList.as_view()),
    path('category/', AllCategoryList.as_view()),
    path('search/', search),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view()),
    path('<int:id>/', ProductDetailById.as_view()),
    path('<slug:category_slug>/', CateogoryDetail.as_view()),
]