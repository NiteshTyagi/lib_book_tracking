from rest_framework import serializers
from lib_book.models import Library, Book, LibraryBook, LibraryActivity



class LibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Library
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class LibraryBookSerializer(serializers.ModelSerializer):
    # library_id = serializers.SlugRelatedField(
    #     queryset=Library.objects.all(), slug_field='name'
    # )

    library_name = serializers.SerializerMethodField()
    book_name = serializers.SerializerMethodField()
    library_activities = serializers.SerializerMethodField()

    def get_library_name(self, obj):
        return (obj.library_id and obj.library_id.name) or ''

    def get_book_name(self, obj):
        return (obj.book_id and obj.book_id.title) or ''

    def get_library_activities(self,obj):
        return LibraryActivitySerializer(obj.libraryActivities.order_by('-library_activity_id'),many=True).data



    class Meta:
        model = LibraryBook
        fields = '__all__'


class LibraryActivitySerializer(serializers.ModelSerializer):


    class Meta:
        model = LibraryActivity
        fields = '__all__'