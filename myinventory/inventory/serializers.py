from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from .models import Item


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for the Item model."""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ('user', 'name', 'upc', 'quantity', 'tags')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
