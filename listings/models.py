from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

class Listing(models.Model):

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        TOWNHOUSE = 'Townhouse'
        APARTMENT = 'Apartment'

    class FurnitureType(models.TextChoices):
        FULLY_FURNISHED = 'Fully Furnished'
        SEMI_FURNISHED = 'Semi Furnished'
        UNFURNISHED = 'Unfurnished'

    class TenantType(models.TextChoices):
        SINGLE_MEN = 'Single men'
        SINGLE_WOMEN = 'Single women'
        COUPLES = 'Couples'


    Realtor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    slug = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=15)
    desc = models.TextField(blank = True)

    sale_type = models.CharField(max_length=50, choices=SaleType.choices, default=SaleType.FOR_SALE)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()

    home_type = models.CharField(max_length=50, choices=HomeType.choices, default=HomeType.HOUSE)
    sqft = models.IntegerField()
    open_house = models.BooleanField(default=False)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_7 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_8 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_9 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_10 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_11 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_12 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_13 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_14 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_15 = models.ImageField(upload_to='photos/%Y/%2/%d/', blank=True)
    photo_16 = models.ImageField(upload_to='photos/%Y/%3/%d/', blank=True)
    photo_17 = models.ImageField(upload_to='photos/%Y/%4/%d/', blank=True)
    photo_18 = models.ImageField(upload_to='photos/%Y/%4/%d/', blank=True)
    photo_19 = models.ImageField(upload_to='photos/%Y/%4/%d/', blank=True)
    photo_20 = models.ImageField(upload_to='photos/%Y/%4/%d/', blank=True)

    list_date = models.DateTimeField(default=now, blank=True)
    verified = models.BooleanField(default=False)
    property_age = models.IntegerField(validators=[MinValueValidator(limit_value=0)])

    furniture_type = models.CharField(max_length=50, choices=FurnitureType.choices, default=FurnitureType.UNFURNISHED)
    tenant_type = models.CharField(null=True, blank=True, choices=TenantType.choices, default=None, max_length=50)

    def __str__(self):
        return self.title

    @property
    def should_show_tenant_type(self):
        # Determine whether to show the tenant_type field based on sale_type
        return self.sale_type == Listing.SaleType.FOR_RENT

    def save(self, *args, **kwargs):

        # Set tenant_type to None if the property is not listed for rent
        if not self.should_show_tenant_type:
            self.tenant_type = None
        super().save(*args, **kwargs)
