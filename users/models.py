from django.db import models
from web.models import CustomUser
from adminapp.models import NewsCategory, NewsSubCategory

# Create your models here.

class MyCategory(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.category.category_name}"
    
class MySubCategory(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(NewsSubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.category.category_name} - {self.sub_category.sub_category_name}"