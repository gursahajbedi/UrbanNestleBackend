from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'verified', 'price', 'list_date', 'Realtor', 'open_house')
    list_display_links = ('id', 'title')
    list_filter = ('Realtor', )
    list_editable = ('verified', )
    search_fields = ('title', 'desc', 'address', 'city', 'state', 'zipcode', 'price')
    list_per_page = 25

admin.site.register(Listing, ListingAdmin)
