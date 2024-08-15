from django.db import models

from userAuth.models import User  # type: ignore[attr-defined]


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.created_at}'

    class Meta:
        db_table = 'Category'


class Art(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    art_img = models.ImageField(upload_to=f'artsImages/%Y/%m/', null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_accepted = models.BooleanField(default=False, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='art_user')

    def __str__(self):
        return f'{self.title} - {self.category} - {self.created_at}'

    class Meta:
        db_table = 'Art'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    art = models.ForeignKey(Art, related_name='comment_art', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.art} - {self.text} at {self.created_at}'

    class Meta:
        db_table = 'Comment'
