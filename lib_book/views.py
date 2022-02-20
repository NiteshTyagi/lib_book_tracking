from django.shortcuts import render

# Create your views here.
from .models import Library, Book, LibraryBook, LibraryActivity
from .serializers import LibrarySerializer, BookSerializer, LibraryBookSerializer, LibraryActivitySerializer
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import viewsets, pagination, permissions, status
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
User=get_user_model()




class Pagination(pagination.PageNumberPagination):
    page_size = 7



class LibraryView(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = Pagination
    serializer_class = LibrarySerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = Pagination
    serializer_class = BookSerializer


class LibraryBookView(viewsets.ModelViewSet):
    queryset = LibraryBook.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = Pagination
    serializer_class = LibraryBookSerializer


class LibraryActivityView(viewsets.ModelViewSet):
    queryset = LibraryActivity.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = Pagination
    serializer_class = LibraryActivitySerializer


class CheckOutView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        try:
            param = request.query_params.get('type',None)
            result = []
            if param == 'user':
                data  = LibraryActivity.objects.values('user','library_book_id__book_id').filter(activity_type='Check_out').annotate(Count=Count('library_book_id__book_id')).order_by()

                for obj in data:
                    result.append({
                        'count' : obj.get('Count'),
                        'user'          : User.objects.filter(pk=obj.get('user')).first().username,
                        'library_book'  : BookSerializer(Book.objects.filter(pk=obj.get('library_book_id__book_id')).first()).data,
                    })

            elif param == 'library':
                data  = LibraryActivity.objects.values('user','library_book_id__library_id').filter(activity_type='Check_out').annotate(Count=Count('library_book_id__library_id')).order_by()

                for obj in data:
                    result.append({
                        'count'         : obj.get('Count'),
                        'user'          : User.objects.filter(pk=obj.get('user')).first().username,
                        'library_book'  : LibrarySerializer(Library.objects.filter(pk=obj.get('library_book_id__library_id')).first()).data,
                    })

            return Response({'success': True, 'error': None, 'results': result}, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({'success': False, 'error': error.args[0], 'results': None},status=status.HTTP_400_BAD_REQUEST)