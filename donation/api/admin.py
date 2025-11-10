from django.contrib import admin
from .models import UserProfile, NGO, Donor, Recipient, Donation, Feedback

admin.site.register(UserProfile)
admin.site.register(NGO)
admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Donation)
admin.site.register(Feedback)
