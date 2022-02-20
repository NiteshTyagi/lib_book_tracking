from django.urls import path, include
from rest_framework import routers
from .views import LibraryView, BookView, LibraryBookView, LibraryActivityView, CheckOutView


app_name = "library"


router = routers.DefaultRouter()

router.register(r'books', BookView, basename='book_set')
router.register(r'lib-books', LibraryBookView, basename='lib_book_set')
router.register(r'lib-activity', LibraryActivityView, basename='lib_activity_set')
router.register(r'', LibraryView, basename='library_set')

urlpatterns = [
    path('', include(router.urls)),
    path('check/check-out/', CheckOutView.as_view()),
]