from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
import json
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def login_page(request):
    return render(request, 'login.html')


@csrf_protect
def register_page(request):
    if request.method == 'POST':
        # Handle donor registration
        try:
            # Prepare data for API call
            donor_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone', ''),
                'address': request.POST.get('address', ''),
                'city': request.POST.get('city', ''),
                'state': request.POST.get('state', ''),
                'pincode': request.POST.get('pincode', '')
            }
            
            logger.info(f"Attempting to create donor with data: {donor_data}")
            
            # Make API call to create donor
            # Use direct localhost URL instead of constructing from request
            api_url = "http://127.0.0.1:8000/api/donors/"
            response = requests.post(api_url, json=donor_data)
            
            logger.info(f"API response status: {response.status_code}")
            logger.info(f"API response text: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                # Successfully created donor, redirect to donor dashboard
                logger.info("Donor created successfully, redirecting to dashboard")
                return redirect('donor')
            else:
                # Handle error
                error_msg = response.text
                logger.error(f"API Error: {error_msg}")
                return render(request, 'register.html', {'error': f"API Error: {error_msg}"})
        except Exception as e:
            logger.error(f"Exception in donor registration: {str(e)}")
            return render(request, 'register.html', {'error': f"Exception: {str(e)}"})
    
    return render(request, 'register.html')


def donor_dashboard(request):
    if request.method == 'POST':
        # Handle donation submission
        try:
            # For now, we'll use the first donor in the database
            # In a real implementation, you would get the actual donor ID from the session
            from api.models import Donor
            donor = Donor.objects.first()
            
            if not donor:
                logger.error("No donors found in database")
                return JsonResponse({'success': False, 'error': 'No donors found. Please register first.'})
            
            donation_data = {
                'donor': donor.donor_id,  # Use the actual donor ID
                'title': request.POST.get('title'),
                'description': request.POST.get('description', ''),
                'category': request.POST.get('category'),
                'quantity': int(request.POST.get('quantity', 1)),
                'status': 'pending'
            }
            
            logger.info(f"Attempting to create donation with data: {donation_data}")
            
            # Make API call to create donation
            api_url = "http://127.0.0.1:8000/api/donations/"
            response = requests.post(api_url, json=donation_data)
            
            logger.info(f"API response status: {response.status_code}")
            logger.info(f"API response text: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                # Successfully created donation
                logger.info("Donation created successfully")
                # Return success response
                return JsonResponse({'success': True})
            else:
                # Handle error
                error_msg = response.text
                logger.error(f"API Error: {error_msg}")
                return JsonResponse({'success': False, 'error': f"API Error: {error_msg}"})
        except Exception as e:
            logger.error(f"Exception in donation submission: {str(e)}")
            return JsonResponse({'success': False, 'error': f"Exception: {str(e)}"})
    
    # GET request - display donor dashboard with donor information
    try:
        # For now, we'll use the first donor in the database
        # In a real implementation, you would get the actual donor ID from the session
        from api.models import Donor
        donor = Donor.objects.first()
        
        if donor:
            # Pass donor information to the template
            context = {
                'donor': {
                    'donor_id': donor.donor_id,
                    'name': donor.name,
                    'email': donor.email,
                    'phone': donor.phone,
                    'address': donor.address,
                    'city': donor.city,
                    'state': donor.state,
                    'pincode': donor.pincode
                }
            }
        else:
            context = {}
    except Exception as e:
        logger.error(f"Error fetching donor information: {str(e)}")
        context = {}
    
    # In a real implementation, you would check if the user is authenticated
    # For now, we'll just show the dashboard
    return render(request, 'donor_dashboard.html', context)


def recipient_dashboard(request):
    # Placeholder: replicate donor layout for now
    return render(request, 'recipient_dashboard.html')


def ngo_dashboard(request):
    return render(request, 'ngo_dashboard.html')