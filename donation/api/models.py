from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("donor", "Donor"),
        ("ngo", "NGO"),
        ("recipient", "Recipient"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user} ({self.role})"


class NGO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ngo_profile', null=True, blank=True)
    ngo_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=12)

    def __str__(self):
        return str(self.ngo_name)

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile', null=True, blank=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.name)

class Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recipient_profile', null=True, blank=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    family_size = models.IntegerField(default=1)
    urgency = models.CharField(max_length=20, default='medium', blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return str(self.name)

class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=30, default='pending')
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    match_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)