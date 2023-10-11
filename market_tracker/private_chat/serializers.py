from rest_framework import serializers
from .models import Message
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MessageSerializer(serializers.ModelSerializer):
    formatted_time_stamp = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_formatted_time_stamp(self, obj):
        return obj.time_stamp.strftime("%I:%M %p, %d-%m-%Y")

    def get_username(self,obj):
        return obj.sender.username
