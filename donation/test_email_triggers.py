#!/usr/bin/env python3
"""
Test script to verify email validation triggers work correctly.
This script tests the MySQL triggers for email validation.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from api.models import Donor, NGO, Recipient
from django.db import IntegrityError


def test_email_validation_triggers():
    """Test that email validation triggers work for all models."""
    print("Testing email validation triggers...")
    
    # Test cases with invalid emails
    invalid_emails = [
        "invalid-email",           # No @ symbol
        "invalid@",               # No domain
        "@domain.com",           # No local part
        "invalid.email",         # No @ symbol
        "test@",                 # No domain part
        "test@domain",           # No TLD
    ]
    
    # Test cases with valid emails
    valid_emails = [
        "test@example.com",
        "user.name@domain.org",
        "valid+email@test.co.uk",
    ]
    
    print("\n=== Testing Invalid Emails (Should Fail) ===")
    
    # Test Donor model with invalid emails
    print("\nTesting Donor model:")
    for email in invalid_emails:
        try:
            donor = Donor(name="Test Donor", email=email)
            donor.save()
            print(f"❌ FAILED: {email} was accepted (should have been rejected)")
            donor.delete()  # Clean up if somehow saved
        except IntegrityError as e:
            print(f"✅ PASSED: {email} was correctly rejected - {str(e)}")
        except Exception as e:
            print(f"⚠️  UNEXPECTED ERROR for {email}: {str(e)}")
    
    # Test NGO model with invalid emails
    print("\nTesting NGO model:")
    for email in invalid_emails:
        try:
            ngo = NGO(ngo_name="Test NGO", email=email, city="Test City", state="Test State", pincode="12345")
            ngo.save()
            print(f"❌ FAILED: {email} was accepted (should have been rejected)")
            ngo.delete()  # Clean up if somehow saved
        except IntegrityError as e:
            print(f"✅ PASSED: {email} was correctly rejected - {str(e)}")
        except Exception as e:
            print(f"⚠️  UNEXPECTED ERROR for {email}: {str(e)}")
    
    # Test Recipient model with invalid emails
    print("\nTesting Recipient model:")
    for email in invalid_emails:
        try:
            recipient = Recipient(name="Test Recipient", email=email)
            recipient.save()
            print(f"❌ FAILED: {email} was accepted (should have been rejected)")
            recipient.delete()  # Clean up if somehow saved
        except IntegrityError as e:
            print(f"✅ PASSED: {email} was correctly rejected - {str(e)}")
        except Exception as e:
            print(f"⚠️  UNEXPECTED ERROR for {email}: {str(e)}")
    
    print("\n=== Testing Valid Emails (Should Pass) ===")
    
    # Test with valid emails
    print("\nTesting valid emails:")
    for i, email in enumerate(valid_emails):
        try:
            # Test Donor
            donor = Donor(name=f"Test Donor {i}", email=f"donor_{email}")
            donor.save()
            print(f"✅ PASSED: Donor with email donor_{email} was accepted")
            donor.delete()
            
            # Test NGO
            ngo = NGO(ngo_name=f"Test NGO {i}", email=f"ngo_{email}", city="Test City", state="Test State", pincode="12345")
            ngo.save()
            print(f"✅ PASSED: NGO with email ngo_{email} was accepted")
            ngo.delete()
            
            # Test Recipient
            recipient = Recipient(name=f"Test Recipient {i}", email=f"recipient_{email}")
            recipient.save()
            print(f"✅ PASSED: Recipient with email recipient_{email} was accepted")
            recipient.delete()
            
        except Exception as e:
            print(f"❌ FAILED: Valid email {email} was rejected - {str(e)}")


def test_email_update_triggers():
    """Test that email validation triggers work for updates."""
    print("\n=== Testing Update Triggers ===")
    
    # Create valid records first
    try:
        donor = Donor(name="Test Donor", email="valid@example.com")
        donor.save()
        
        # Try to update with invalid email
        try:
            donor.email = "invalid-email"
            donor.save()
            print("❌ FAILED: Update with invalid email was accepted")
            donor.delete()
        except IntegrityError as e:
            print(f"✅ PASSED: Update with invalid email was correctly rejected - {str(e)}")
            donor.delete()
        except Exception as e:
            print(f"⚠️  UNEXPECTED ERROR during update: {str(e)}")
            donor.delete()
            
    except Exception as e:
        print(f"❌ FAILED: Could not create initial valid record - {str(e)}")


if __name__ == "__main__":
    print("Email Validation Trigger Test")
    print("=" * 50)
    
    test_email_validation_triggers()
    test_email_update_triggers()
    
    print("\n" + "=" * 50)
    print("Test completed!")