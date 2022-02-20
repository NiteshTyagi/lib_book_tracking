import json
from rest_framework import status
from django.test import TestCase, Client
from django.db.models import Count
from .models import Library, Book, LibraryBook, LibraryActivity
from .serializers import LibrarySerializer, BookSerializer , LibraryBookSerializer, LibraryActivitySerializer
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your tests here.

# initialize the APIClient app
client = Client()

class LibraryTest(TestCase):

    def setUp(self):
        self.lib_1 = Library.objects.create(
            name='Library 1', city='Noida', state='Uttar Pradesh', postal_code='201301')
        self.lib_2 = Library.objects.create(
            name='Library 2', city='Gurugram', state='Haryana', postal_code='123456')


        self.valid_payload = {
            'name'          : 'Library 3',
            'city'          : 'Delhi',
            'state'         : 'Delhi',
            'postal_code'   : '345678'
        }

        self.put_payload = {
            'name'          : 'Library 2 updated',
            'city'          : 'Chennai',
            'state'         : 'Tamil Nadu',
            'postal_code'   : '345678'
        }

    
    def test_get_library(self):
        library_1 = Library.objects.get(name='Library 1')
        library_2 = Library.objects.get(name='Library 2')

        self.assertEqual(library_1.city, "Noida")
        self.assertEqual(library_2.state, "Haryana")


    def test_get_request_library(self):
        # get API response
        response = client.get('http://localhost:8080/api/')
        # get data from db
        libs = Library.objects.all()
        # serialize it
        serializer = LibrarySerializer(libs, many=True)
    
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # POST API
    def test_post_request_library(self):
        response = client.post(
            'http://localhost:8080/api/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_get_request_library()

    # PUT API
    def test_put_request_library(self):
        response = client.put(
            'http://localhost:8080/api/%d/'%(self.lib_2.library_id),
            data=json.dumps(self.put_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_get_request_library()



class BookTest(TestCase):

    def setUp(self):
        self.book_1 = Book.objects.create(
            title='Book Title 1', author_name='Book 1 author name', isbn_num='45632678', genre='Horror',description='Testing Description of book 1')
        self.book_2 = Book.objects.create(
            title='Book Title 2', author_name='Book 2 author name', isbn_num='98034292', genre='Comedy',description='Testing Description of book 2')


        self.valid_payload = {
            'title'             : 'Book Title 3',
            'author_name'       : 'Book 2 author name',
            'isbn_num'          : '435345354',
            'genre'             : 'science',
            'description'       : 'Testing Description of book 3'
        }

    
    def test_get_Book(self):
        book_1 = Book.objects.get(title='Book Title 1')
        book_2 = Book.objects.get(title='Book Title 2')

        self.assertEqual(book_1.author_name, "Book 1 author name")
        self.assertEqual(book_2.isbn_num, "98034292")


    def test_get_request_book(self):
        # get API response
        response = client.get('http://localhost:8080/api/books/')
        # get data from db
        books = Book.objects.all()
        # serialize it
        serializer = BookSerializer(books, many=True)
    
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # POST API
    def test_post_request_book(self):
        response = client.post(
            'http://localhost:8080/api/books/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_get_request_book()

    

class LibraryBookTest(TestCase):

    def setUp(self):
        self.lib_1 = Library.objects.create(
            name='Library 1', city='Noida', state='Uttar Pradesh', postal_code='201301')
        self.lib_2 = Library.objects.create(
            name='Library 2', city='Gurugram', state='Haryana', postal_code='123456')

        self.book_1 = Book.objects.create(
            title='Book Title 1', author_name='Book 1 author name', isbn_num='45632678', genre='Horror',description='Testing Description of book 1')
        self.book_2 = Book.objects.create(
            title='Book Title 2', author_name='Book 2 author name', isbn_num='98034292', genre='Comedy',description='Testing Description of book 2')

        self.lib_book_1 = LibraryBook.objects.create(
            library_id = self.lib_1, book_id = self.book_1
        )

        # self.lib_book_2 = LibraryBook.objects.create(
        #     library_id = self.lib_1, book_id = self.book_2
        # )

        self.lib_book_3 =  LibraryBook.objects.create(
            library_id = self.lib_2, book_id = self.book_1
        )

        self.lib_book_4 = LibraryBook.objects.create(
            library_id = self.lib_2, book_id = self.book_2
        )


        self.valid_payload = {
            'library_id'    : self.lib_1.library_id,
            'book_id'       : self.book_2.book_id,
        }


    def test_check_LibraryBook(self):
        libbook_1 = LibraryBook.objects.get(library_book_id = self.lib_book_1.library_book_id)
        libbook_2 = LibraryBook.objects.get(library_book_id = self.lib_book_3.library_book_id)

        self.assertEqual(libbook_1.book_id.author_name, "Book 1 author name")
        self.assertEqual(libbook_2.library_id.postal_code, "123456")

        
    
    def test_get_request_library_book(self):
        # get API response
        response = client.get('http://localhost:8080/api/lib-books/')
        # get data from db
        lib_books = LibraryBook.objects.all()
    
        serializer = LibraryBookSerializer(lib_books, many=True)
    
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # POST API
    def test_post_request_lib_book(self):
        response = client.post(
            'http://localhost:8080/api/lib-books/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_get_request_library_book()



class LibraryActivityTest(LibraryBookTest):

    def setUp(self):
        super(LibraryActivityTest, self).setUp()
        self.user_1 = User.objects.create(username='user1')
        self.user_2 = User.objects.create(username='user2')
        
        self.lib_act_1 = LibraryActivity.objects.create(
            activity_type='Check_in', user= self.user_1, library_book_id=self.lib_book_1)

        self.lib_act_2 = LibraryActivity.objects.create(
            activity_type='Check_in', user= self.user_1, library_book_id=self.lib_book_3)

        self.lib_act_3 = LibraryActivity.objects.create(
            activity_type='Check_out', user= self.user_2, library_book_id=self.lib_book_4)

        self.payload = {
            'activity_type'     : 'Check_out',
            'user'              : self.user_2.pk,
            'library_book_id'   : self.lib_book_3.library_book_id,
        }


    def test_check_LibraryActivity(self):
        lib_act_1 = LibraryActivity.objects.get(library_activity_id = self.lib_act_1.library_activity_id)
        lib_act_2 = LibraryActivity.objects.get(library_activity_id = self.lib_act_3.library_activity_id)

        self.assertEqual(lib_act_1.activity_type, "Check_in")
        self.assertEqual(lib_act_2.library_book_id.library_id.postal_code, "123456")


    def test_get_request_library_activity(self):
        # get API response
        response = client.get('http://localhost:8080/api/lib-activity/')
        # get data from db
        lib_books = LibraryActivity.objects.all()
    
        serializer = LibraryActivitySerializer(lib_books, many=True)
    
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # POST API
    def test_post_request_library_activity(self):
        response = client.post(
            'http://localhost:8080/api/lib-activity/',
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_get_request_library_activity()


    def tearDown(self):
        self.user_1.delete()
        self.user_2.delete()

    #  List all library books checked-out to a user 
    def test_get_request_checkout_user(self):
        # get API response 
        response = client.get('http://localhost:8080/api/check/check-out/?type=user')
        
        # get data from db
        result = []
        data  = LibraryActivity.objects.values('user','library_book_id__book_id').filter(activity_type='Check_out').annotate(Count=Count('library_book_id__book_id')).order_by()

        for obj in data:
            result.append({
                'count' : obj.get('Count'),
                'user'          : User.objects.filter(pk=obj.get('user')).first().username,
                'library_book'  : BookSerializer(Book.objects.filter(pk=obj.get('library_book_id__book_id')).first()).data,
            })
        
        self.assertEqual(response.data.get('results'), result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # List all library books checked-out of a library 
    def test_get_request_checkout_library(self):
        # get API response
        response = client.get('http://localhost:8080/api/check/check-out/?type=library')
        
        # get data from db
        result = []
        data  = LibraryActivity.objects.values('user','library_book_id__library_id').filter(activity_type='Check_out').annotate(Count=Count('library_book_id__library_id')).order_by()

        for obj in data:
            result.append({
                'count'         : obj.get('Count'),
                'user'          : User.objects.filter(pk=obj.get('user')).first().username,
                'library_book'  : LibrarySerializer(Library.objects.filter(pk=obj.get('library_book_id__library_id')).first()).data,
            })
        
        self.assertEqual(response.data.get('results'), result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



