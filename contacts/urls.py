from django.urls import path
from .views import ContactCreationView

urlpatterns = [
    path('', ContactCreationView.as_view()),
]
