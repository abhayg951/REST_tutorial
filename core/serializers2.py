from rest_framework import serializers
from .models import *

# If we are using this type of serializer than we have to define all the models in the class
# which makes very difficult for the large models
#so we will use ModelSeriallizer for the this 

class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    publish_date = serializers.DateField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    description = serializers.CharField()


    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.publish_date = validated_data.get('publish_date', instance.publish_date)

        instance.save()
        return instance