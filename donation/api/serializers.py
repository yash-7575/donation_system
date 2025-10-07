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