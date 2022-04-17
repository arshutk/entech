from django.db import models
from django.template.defaultfilters import slugify
import uuid
import os

from meta.models import ModelMeta
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from user.models import Account


class Post(ModelMeta, models.Model):

   class STATUS(models.TextChoices):
      ACTIVE = 'Active'
      INACTIVE = 'Inactive'
   
   def cover_img_or_default(self, default_path="static/blog/default-cover-img.jpg"):
        if self.cover_img:
            return self.cover_img.url
        return default_path

   def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('cover_img', filename)

   title             = models.CharField(max_length=100)
   subtitle          = models.CharField(max_length=200)
   content           = RichTextUploadingField()
   cover_img         = models.ImageField(upload_to=upload_location, blank = True, null = True) 
   slug              = models.SlugField(max_length=200, unique=True, blank=True)
   written_by        = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="articles")  
   bookmarked_by     = models.ManyToManyField(Account, related_name="bookmarked_posts", blank = True)
   posted_at         = models.DateTimeField(auto_now_add = True)
   status            = models.CharField(choices=STATUS.choices, max_length=8, default=STATUS.ACTIVE) 

   objects           = models.Manager()

   def __str__(self):
      return f'{self.written_by.email} : {self.title}'
    
   class Meta:
      ordering = ('-posted_at',)
   
   def save(self, *args, **kwargs):
      self.slug = f'{slugify(self.title)}-{uuid.uuid4()}'
      super().save(*args, **kwargs)
   
   _metadata = {
        'title': 'title',
        'subtitle': 'subtitle',
        'description': 'content',
    }


   
class Vote(models.Model):
   class CHOICES(models.TextChoices):
      LIKE = 'like'
      LOVE = 'love'
      INSIGHTFUL = 'insightful'
   
   post              = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "reactions")
   vote_type         = models.CharField(choices=CHOICES.choices, max_length = 10)
   voter             = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = "votes")

   class Meta:
      unique_together = ('post', 'voter')


class Comment(models.Model):

   class STATUS(models.TextChoices):
      ACTIVE = 'Active'
      INACTIVE = 'Inactive'

   post         = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments", null=True)
   comment      = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True) 
   written_by   = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = "comments_made")
   text         = models.TextField()
   posted_at    = models.DateTimeField(auto_now_add = True)
   liked_by     = models.ManyToManyField(Account, blank = True, related_name = "comments_liked")
   status       = models.CharField(choices=STATUS.choices, max_length=8, default=STATUS.ACTIVE, blank=True) 

   objects      = models.Manager()

   
   def __str__(self):
      return f'{self.written_by.email} > {self.post.title}'
    
   class Meta:
      ordering = ('-posted_at',)
  
      