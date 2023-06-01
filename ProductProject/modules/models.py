from django.db import models
from django.utils.translation import gettext_lazy as _

class CrudConstrained(models.Model):
    """
    	Abstract model that provides CRUD constrains 
    	for model objects.
    """
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(
        _("Date updated"), auto_now=True)
    date_deleted = models.DateTimeField(
        _("Date deleted"), auto_now=True)

    class Meta:
        abstract = True