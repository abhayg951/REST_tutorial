from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('book', BookViewSet, basename='books')
# router.register('book/<slug:slug>', BookdetailsViewSet, basename='booksdetails')

urlpatterns = [
    path('', include(router.urls)),
    # path('book/<slug:slug>', BookdetailsViewSet.as_view({'get': 'retrieve',
    # 'put': 'update',
    # 'delete': 'destroy'})),

    # path('book/', Booklist.as_view()),
    # path('book/<slug:slug>', Bookdetails.as_view()),
    # path('book/', book_list),
    # path('book/<slug:slug>', single_book)
]


