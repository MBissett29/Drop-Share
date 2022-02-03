from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):


    title = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DS_blog_posts") # Need to think of name
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='DS_blog_likes', blank=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class UserPost(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='user_post'
        )
    title = models.CharField(max_length=500)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    def __str__(self):
        return self