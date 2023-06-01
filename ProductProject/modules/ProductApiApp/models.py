from django.db import models
from django.urls import reverse
import uuid
from django.utils.text import slugify
from modules.models import CrudConstrained

# Create your models here.

class Category(CrudConstrained):
    gid = models.UUIDField(max_length=32, unique=True,default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)
    name = models.CharField(max_length=200,db_index=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num = num + 1
        return unique_slug


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Category, self).save(*args, **kwargs)


class Product(CrudConstrained):
    gid = models.UUIDField(max_length=32, unique=True,default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    image_url = models.URLField(null=True,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num = num + 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Product, self).save(*args, **kwargs)


