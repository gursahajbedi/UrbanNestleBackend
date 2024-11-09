from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import permissions, status
from .models import Listing
from .serializers import ListingSerializer, ListingDetailSerializer, AddListingSerializer
from datetime import datetime, timezone, timedelta
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from accounts.models import UserAccount
import functools

class ListingsView(ListAPIView):
    queryset = Listing.objects.order_by('-list_date').filter()
    permission_classes = (permissions.AllowAny, )
    serializer_class = ListingSerializer
    lookup_field = 'slug'

class ListingView(RetrieveAPIView):
    queryset = Listing.objects.order_by('-list_date').filter()
    serializer_class = ListingDetailSerializer
    lookup_field = 'slug'

class SearchView(APIView,PageNumberPagination):
    serializer_class = ListingSerializer

    def post(self, request, format=None):
        queryset = Listing.objects.order_by('-list_date').filter()
        data = self.request.data

        for field, value in data.items():
            if field == 'sale_type':
                queryset = queryset.filter(sale_type__iexact=value)
            elif field == 'price':
                price = self.convert_price_range(value)
                if price is not None:
                    queryset = queryset.filter(price__lte=price)
            elif field == 'bedrooms':
                if value:
                    bedrooms = int(value.rstrip('+'))
                    queryset = queryset.filter(bedrooms__gte=bedrooms)
            elif field == 'home_type':
                home_type = self.convert_home_type(value)
                if home_type is not None:
                    queryset = queryset.filter(home_type__iexact=value)
            elif field == 'bathrooms':
                if value: 
                    bathrooms = (value.rstrip('+'))
                    queryset = queryset.filter(bathrooms__gte=bathrooms)
            elif field == 'sqft':
                sqft = self.convert_sqft(value)
                if sqft is not None:
                    queryset = queryset.filter(sqft__gte=sqft)
            elif field == 'days_listed':
                days_passed = self.convert_days_listed(value)
                if days_passed is not None:
                    queryset = queryset.filter(list_date__gte=timezone.now() - timezone.timedelta(days=days_passed))

            elif field == 'property_age':
                if value:
                    property_age = int(value.rstrip('-'))
                    queryset = queryset.filter(property_age__lte=property_age)

            elif field == 'furniture_type':
                furniture_type = self.convert_furniture_type(value)
                if furniture_type is not None:
                    queryset = queryset.filter(furniture_type__iexact=value)

            elif field == 'open_house':
                open_house = self.convert_open_house(value)
                if open_house is not None:
                    queryset = queryset.filter(open_house__iexact=open_house)
            elif field == 'keywords':
                if value:
                    queryset = queryset.filter(desc__icontains=value)

            elif field == 'state':
                if value:
                    queryset = queryset.filter(state__icontains=value)

        queryset2=self.paginate_queryset(queryset,request)
        serializer = ListingSerializer(queryset2, many=True)
        return self.get_paginated_response(serializer.data)

    def convert_price_range(self, price_str):
        if price_str == 'Any':
            return None
        elif price_str.endswith('-'):
            return int(price_str.replace('-', '').replace(',', ''))
        else:
            return None

    def convert_sqft(self, sqft_str):
        if sqft_str == 'Any':
            return None
        elif sqft_str.endswith('+'):
            return int(sqft_str.replace('+', '').replace(',', ''))
        else:
            return None

    def convert_days_listed(self, days_listed_str):
        if days_listed_str == 'Any':
            return None
        elif ' or less' in days_listed_str:
            return int(days_listed_str.split(' ')[0])
        else:
            return None

    def convert_open_house(self, open_house_str):
        if str(open_house_str).lower() in ['true', 'false']:
            return str(open_house_str).lower()
        else:
            return None


    def convert_furniture_type(self, furniture_type_str):
        if furniture_type_str == 'Any':
            return None

    def convert_home_type(self, home_type_str):
        if home_type_str == 'Any':
            return None
        return home_type_str

@method_decorator(csrf_exempt, name='dispatch')
class AddListingAPIView(CreateAPIView):
    serializer_class = AddListingSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        # Check if the logged-in user is recognized as a Realtor
        user = self.request.user

        # Assuming your user model is 'UserAccount'
        user_account = UserAccount.objects.get(email=user.email)

        if user_account:
            # If the user is recognized as a UserAccount, associate the UserAccount with the listing
            serializer.save(Realtor=user_account)
        else:
            # If the user is not recognized as a UserAccount, proceed with the existing logic
            serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data['message'] = 'Listing added successfully!'
        return response