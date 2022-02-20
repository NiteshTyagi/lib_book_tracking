from tabnanny import verbose
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

# Create your models here.


class Library(models.Model):

    library_id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Name',max_length=100)
    city = models.CharField(max_length=100, default="City Name")
    state = models.CharField(max_length=100, default="State Name")
    postal_code = models.CharField(max_length=100, default="Postal Code")


    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('library_id',)
        verbose_name_plural = _("Libraries")



class Book(models.Model):

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='Title',max_length=100)
    author_name = models.CharField(max_length=100, default="Author Name")
    isbn_num = models.CharField(max_length=100, default="ISBN NUMBER",unique=True)
    genre = models.CharField(max_length=100, default="Genre")
    description = models.TextField(blank=True,null=True)


    def __str__(self) -> str:
        return self.title


    class Meta:
        ordering = ('book_id',)
        verbose_name_plural = _("Books")


class LibraryBook(models.Model):

    library_book_id = models.AutoField(primary_key=True)
    library_id = models.ForeignKey(Library, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    # last_library_activity_id = models.ForeignKey(LibraryActivity,on_delete=models.CASCADE,)


    def __str__(self) -> str:
        return "%s-%s"%(self.library_id, self.book_id)

    
    class Meta:
        unique_together = ('library_id', 'book_id')
        ordering = ('library_book_id',)
        verbose_name_plural = _("Library Book")



class LibraryActivity(models.Model):

    library_activity_id = models.AutoField(primary_key=True)
    activity_type = models.CharField(verbose_name='Activity Type', choices=[('Check_in','Check-In'),('Check_out','Check-Out')], max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    library_book_id = models.ForeignKey(LibraryBook, on_delete=models.CASCADE, related_name='libraryActivities')
    check_in_at = models.DateTimeField(blank=True,null=True)
    check_out_at = models.DateTimeField(blank=True,null=True)


    

    def __str__(self) -> str:
        return "%s - %s"%(self.user,self.activity_type)

    
    class Meta:
        ordering = ('library_activity_id',)
        verbose_name_plural = _("Library Activities")


def _post_save_signal(sender, instance, created,*args, **kwargs):
    if created:
        if instance.activity_type == 'Check_in':
            instance.check_in_at = timezone.now()
        else:
            instance.check_out_at = timezone.now()
        instance.save()

post_save.connect(_post_save_signal, sender=LibraryActivity)



    




