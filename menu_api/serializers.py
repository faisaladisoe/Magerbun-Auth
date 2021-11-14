from rest_framework import serializers
from menu_api.models import Menu


class MenuSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(decimal_places=2, max_digits=10000)
    stock = serializers.IntegerField()
    description = serializers.CharField()
    category = serializers.ChoiceField(choices=Menu.list_category)

    def create(self, validated_data):
        """
        Create and return a new `Menu` instance, given the validated data.
        """
        return Menu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Menu` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
