from django.db import models
from userAuth.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class Art(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    art_img = models.ImageField(upload_to=f'artsImages/%Y/%m/', null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='art_category')

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.category} - {self.created_at}'


class Comment(models.Model):
    art = models.ForeignKey(Art, related_name='comment_art', on_delete=models.CASCADE)

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ->{self.art} - {self.text} at {self.created_at}'
