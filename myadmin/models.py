from django.db import models
# Create your models here.

#管理员表
class admin(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    add_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)

#网站基本信息表
class config(models.Model):
    title=models.CharField(max_length=200,null=True)
    logo=models.ImageField(upload_to='static')
    description=models.CharField(max_length=200)
    keywords=models.CharField(max_length=100)
    about_us=models.TextField()
    connect_us=models.CharField(max_length=200)
#留言表
class message(models.Model):
    name=models.CharField(max_length=100)
    content=models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

#文章分类表
class article_cat(models.Model):
    cat_name=models.CharField(max_length=100)

#文章表
class article(models.Model):
    title=models.CharField(max_length=100,null=True)
    image=models.ImageField(null=True)
    count=models.IntegerField(default=10)
    desc=models.CharField(max_length=200)
    content=models.TextField(null=True)
    sort=models.IntegerField(null=True)
    add_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
    cat =models.ForeignKey('article_cat',to_field='id')



