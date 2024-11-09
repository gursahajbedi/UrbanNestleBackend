from django.urls import path
from .views import ListingView, ListingsView, SearchView, AddListingAPIView

urlpatterns = [
    path('', ListingsView.as_view()),
    path('serach', SearchView.as_view()),
    path('add', AddListingAPIView.as_view()),
    path('<slug>', ListingView.as_view()),
]
