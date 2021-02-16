from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=50)
    posted_at = models.DateTimeField(auto_now_add=True)
    