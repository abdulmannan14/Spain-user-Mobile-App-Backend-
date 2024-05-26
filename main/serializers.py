from rest_framework import serializers
from . import models as main_models


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.UserDetails
        fields = '__all__'


class GetCSVAndCreateUserDetailSerializer(serializers.Serializer):
    csv_file = serializers.FileField(required=True)

    class Meta:
        fields = ('csv_file',)


class UpdateUserCardImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    card = serializers.ImageField(required=True)

    class Meta:
        fields = ('id', 'card')
