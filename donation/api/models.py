from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class NGO(models.Model):
    ngo_id = models.AutoField(primary_key=True)
    ngo_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.ngo_name

class Donor(models.Model):
    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)  # For storing hashed passwords
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self) -> str:
        return self.name

class Recipient(models.Model):
    recipient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    family_size = models.IntegerField(default=1)
    urgency = models.CharField(max_length=20, default='medium', blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=12, blank=True)

    def __str__(self) -> str:
        return self.name

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