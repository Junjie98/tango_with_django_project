from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    #unique means the given field's value must be unique thruout the underlying database table.

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
