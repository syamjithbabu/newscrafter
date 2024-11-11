from django.db import models
from django.utils.text import slugify

# Create your models here.

class NewsCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class NewsSubCategory(models.Model):
    category = models.ForeignKey(NewsCategory,on_delete=models.CASCADE,null=True,blank=True)
    sub_category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.category_name} - {self.sub_category_name}"
    
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    content = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(NewsSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.BooleanField(null=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)