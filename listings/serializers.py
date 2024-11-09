from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.should_show_tenant_type and 'tenant_type' in data:
            del data['tenant_type']
        return data


class ListingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        lookup_field = 'slug'

class AddListingSerializer(serializers.ModelSerializer):
    Realtor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Listing
        exclude = ['verified']

