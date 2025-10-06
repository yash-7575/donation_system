from rest_framework import serializers
from .models import Donor, Recipient, NGO, Donation, Feedback


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['donor_id', 'name', 'email', 'phone', 'address', 'city', 'state', 'pincode']
        read_only_fields = ['donor_id']


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['recipient_id', 'name', 'email', 'phone', 'family_size', 'urgency', 'address', 'city', 'state', 'pincode']
        read_only_fields = ['recipient_id']


class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = ['ngo_id', 'ngo_name', 'email', 'phone', 'website', 'address', 'city', 'state', 'pincode']
        read_only_fields = ['ngo_id']


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'