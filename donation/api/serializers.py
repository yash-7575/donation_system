from rest_framework import serializers
from .models import Donor, Recipient, NGO, Donation, Feedback


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'


class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


