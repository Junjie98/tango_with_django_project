from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True) #OR, to allow empty space. models.SlugField(blank=True)
    #unique means the given field's value must be unique thruout the underlying database table.

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs) #defined in the base django.db.models.Model class.
        #^ this call performs necessary logic to take the changes and save the said changes to correct database table.
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. It links the user profile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #attributes that we wish to add in additionally. (Outside of what the User model provide by default.)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #^ the upload_to attribute is conjoined with project's MEDIA_ROOT
    
    def __str__(self):
        return self.user.username
