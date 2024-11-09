from django.urls import path
from .views import SignUpView, LoginView
from .views import RealtorListView, RealtorView, TopSellerView, UserUpdateView, TestimonialListView


urlpatterns = [
    path('login', LoginView.as_view()),

    path('signup', SignUpView.as_view()),
    path('user-list', RealtorListView.as_view()),
    path('topseller', TopSellerView.as_view()),
    path('<pk>', RealtorView.as_view()),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('testimonials/', TestimonialListView.as_view())
]

