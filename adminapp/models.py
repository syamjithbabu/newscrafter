from django.db import models

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