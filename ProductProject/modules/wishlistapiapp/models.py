from django.db import models
from modules.models import CrudConstrained
import uuid
from django.utils.text import slugify
from modules.ProductApiApp.models import Product
from django.contrib.auth.models import User

# Create your models here.

class WishItems(CrudConstrained):
    gid = models.UUIDField(max_length=32, unique=True,default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_product')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wish_liker')
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ('product',)
        verbose_name = 'wishitem'
        verbose_name_plural = 'wishitems'

    def __str__(self):
        return self.product.name
    
    def _get_unique_slug(self):
        slug = slugify(self.product.name+self.customer.first_name)
        unique_slug = slug
        num = 1
        while WishItems.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num = num + 1
        return unique_slug


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(WishItems, self).save(*args, **kwargs)

    def get_item_price(self):
        return self.quantity * self.product.price