from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
import logging

from .models import UserProfile, Donor, NGO, Recipient, Donation, Feedback, Request
from .forms import SignupStep1Form, DonorProfileForm, NGOProfileForm, RecipientProfileForm

logger = logging.getLogger(__name__)


# ---------------- HOME ----------------
def home(request):
    # Calculate live statistics for the homepage
    try:
        # Sums the quantity of all donations. If no donations, defaults to 0.
        items_donated = Donation.objects.aggregate(total=Sum('quantity'))['total'] or 0
        families_helped = Recipient.objects.count()
        total_ngos = NGO.objects.count()
        active_donors = Donor.objects.count()
    except Exception as e:
        # In case of a database error, default all stats to 0
        logger.error(f"Error fetching homepage stats: {e}")
        items_donated = 0
        families_helped = 0
        total_ngos = 0
        active_donors = 0
        
    # Fetch recent feedback with user profile information
    try:
        recent_feedback = Feedback.objects.select_related('user__userprofile').order_by('-created_at')[:4]
        feedback_data = []
        for feedback in recent_feedback:
            # Get user role
            try:
                user_role = feedback.user.userprofile.role
            except UserProfile.DoesNotExist:
                user_role = "User"
            
            # Get user name based on role
            user_name = feedback.user.get_full_name() or feedback.user.username
            if not user_name:
                user_name = "Anonymous"
            
            # For donors, try to get donor name
            if user_role == "donor":
                try:
                    donor = Donor.objects.get(user=feedback.user)
                    user_name = donor.name
                except Donor.DoesNotExist:
                    pass
            # For recipients, try to get recipient name
            elif user_role == "recipient":
                try:
                    recipient = Recipient.objects.get(user=feedback.user)
                    user_name = recipient.name
                except Recipient.DoesNotExist:
                    pass
            # For NGOs, try to get NGO name
            elif user_role == "ngo":
                try:
                    ngo = NGO.objects.get(user=feedback.user)
                    user_name = ngo.ngo_name
                except NGO.DoesNotExist:
                    pass
            
            feedback_data.append({
                'name': user_name,
                'role': user_role.capitalize(),
                'rating': feedback.rating,
                'comment': feedback.comment,
                'created_at': feedback.created_at
            })
    except Exception as e:
        logger.error(f"Error fetching feedback: {e}")
        feedback_data = []
        
    context = {
        'home_stats': {
            'items_donated': items_donated,
            'families_helped': families_helped,
            'total_ngos': total_ngos,
            'active_donors': active_donors,
        },
        'feedback_data': feedback_data
    }
    return render(request, "home.html", context)

# ---------------- LOGIN ----------------
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            try:
                role = user.userprofile.role
                if role == "donor":
                    return redirect("donor")
                elif role == "ngo":
                    return redirect("ngo")
                elif role == "recipient":
                    return redirect("recipient")
            except UserProfile.DoesNotExist:
                pass

            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ---------------- LOGOUT ----------------
def logout_page(request):
    logout(request)
    return redirect("home")


# ---------------- SIGNUP STEP 1 ----------------
def signup_step1(request):
    if request.method == "POST":
        form = SignupStep1Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup_step1")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect("signup_step1")

            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, role=role)

            user = authenticate(request, username=username, password=password)
            login(request, user)

            if role == "donor":
                return redirect("signup_donor")
            elif role == "ngo":
                return redirect("signup_ngo")
            else:
                return redirect("signup_recipient")

    else:
        form = SignupStep1Form()

    return render(request, "signup_step1.html", {"form": form})


# ---------------- SIGNUP STEP 2 (DONOR) ----------------
def signup_donor(request):
    if request.method == "POST":
        form = DonorProfileForm(request.POST)
        if form.is_valid():
            Donor.objects.create(
                user=request.user,
                name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                pincode=form.cleaned_data["pincode"],
            )
            return redirect("signup_success")
    else:
        form = DonorProfileForm()

    return render(request, "signup_donor.html", {"form": form})


# ---------------- SIGNUP STEP 2 (NGO) ----------------
def signup_ngo(request):
    if request.method == "POST":
        form = NGOProfileForm(request.POST)
        if form.is_valid():
            NGO.objects.create(
                user=request.user,
                ngo_name=form.cleaned_data["ngo_name"],
                phone=form.cleaned_data["phone"],
                website=form.cleaned_data["website"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                pincode=form.cleaned_data["pincode"],
            )
            return redirect("signup_success")
    else:
        form = NGOProfileForm()

    return render(request, "signup_ngo.html", {"form": form})


# ---------------- SIGNUP STEP 2 (RECIPIENT) ----------------
def signup_recipient(request):
    if request.method == "POST":
        form = RecipientProfileForm(request.POST)
        if form.is_valid():
            Recipient.objects.create(
                user=request.user,
                name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                family_size=form.cleaned_data["family_size"],
                urgency=form.cleaned_data["urgency"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                pincode=form.cleaned_data["pincode"],
            )
            return redirect("signup_success")
    else:
        form = RecipientProfileForm()

    return render(request, "signup_recipient.html", {"form": form})


# ---------------- SIGNUP SUCCESS REDIRECT ----------------
def signup_success(request):
    role = request.user.userprofile.role
    if role == "donor":
        return redirect("donor")
    elif role == "ngo":
        return redirect("ngo")
    return redirect("recipient")


# ---------------- DONOR DASHBOARD ----------------
# Add these functions to your views.py

# ---------------- DONOR DASHBOARD (UPDATED) ----------------
def donor_dashboard(request):
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Must be donor
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'donor':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('login')

    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found')
        return redirect('home')

    # Get filter parameters
    selected_category = request.GET.get('category')
    selected_status = request.GET.get('status')
    
    # Handle new donation submission
    if request.method == 'POST':
        try:
            Donation.objects.create(
                donor=donor,
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                category=request.POST.get('category'),
                quantity=int(request.POST.get('quantity', 1)),
                status='pending',
                image_url=request.POST.get('image_url', '')
            )
            messages.success(request, 'Donation submitted successfully!')
        except Exception as e:
            logger.error(f'Error creating donation: {e}')
            messages.error(request, 'Failed to submit donation')
        
        return redirect('donor')

    # Get donor's past donations with filtering
    donations = Donation.objects.filter(donor=donor).order_by('-created_at')
    
    # Apply filters
    if selected_category:
        donations = donations.filter(category=selected_category)
    if selected_status:
        donations = donations.filter(status=selected_status)
    
    # Get all unique donation categories for filter dropdown
    available_categories = Donation.objects.filter(donor=donor).values_list('category', flat=True).distinct()
    
    # Get all unique donation statuses for filter dropdown
    available_statuses = Donation.objects.filter(donor=donor).values_list('status', flat=True).distinct()

    # Calculate dashboard stats
    total_donations = Donation.objects.filter(donor=donor).count()
    delivered_donations = Donation.objects.filter(donor=donor, status='delivered').count()
    
    # Calculate total items delivered (sum of quantities)
    total_items_delivered = Donation.objects.filter(
        donor=donor, 
        status='delivered'
    ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    
    # Impact score calculation (using total items delivered)
    impact_score = total_items_delivered * 10
    
    # Thank you notes count (you may need to adjust based on your Feedback model)
    thank_you_notes = 0  # Implement based on your feedback system

    context = {
        'donor': donor,
        'donations': donations,
        'total_donations': total_donations,
        'delivered_donations': delivered_donations,
        'impact_score': impact_score,
        'thank_you_notes': thank_you_notes,
        'available_categories': available_categories,
        'available_statuses': available_statuses,
        'selected_category': selected_category,
        'selected_status': selected_status,
    }
    return render(request, 'donor_dashboard.html', context)


# ---------------- UPDATE DONATION ----------------
def update_donation(request, donation_id):
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Must be donor
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'donor':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('login')

    # Use get_object_or_404 to fetch the donation only if it belongs to the logged-in user
    donation = get_object_or_404(Donation, id=donation_id, donor__user=request.user)

    # Handle update submission
    if request.method == 'POST':
        try:
            donation.title = request.POST.get('title')
            donation.description = request.POST.get('description', '')
            donation.category = request.POST.get('category')
            donation.quantity = int(request.POST.get('quantity', 1))
            donation.status = request.POST.get('status')
            donation.image_url = request.POST.get('image_url', '')
            donation.save()
            messages.success(request, 'Donation updated successfully!')
        except Exception as e:
            logger.error(f'Error updating donation: {e}')
            messages.error(request, 'Failed to update donation')
        
        return redirect('donor')
    else:
        # For GET request, render the edit form template
        context = {
            'donation_obj': donation
        }
        return render(request, 'edit_donation.html', context)


# ---------------- DELETE DONATION ----------------
def delete_donation(request, donation_id):
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Must be donor
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'donor':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('login')

    # Use get_object_or_404 to fetch the donation only if it belongs to the logged-in user
    donation = get_object_or_404(Donation, id=donation_id, donor__user=request.user)

    # Handle delete
    if request.method == 'POST':
        try:
            donation.delete()
            messages.success(request, 'Donation deleted successfully!')
        except Exception as e:
            logger.error(f'Error deleting donation: {e}')
            messages.error(request, 'Failed to delete donation')
        
        return redirect('donor')
    else:
        # For GET request, render a confirmation page
        context = {
            'donation_obj': donation
        }
        return render(request, 'delete_donation.html', context)

# ---------------- RECIPIENT DASHBOARD (Corrected) ----------------
def recipient_dashboard(request):
    # Ensure logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure user is recipient
    try:
        recipient = Recipient.objects.get(user=request.user)
    except Recipient.DoesNotExist:
        messages.error(request, 'Recipient profile not found.')
        return redirect('login')

    # Handle new request submission
    if request.method == "POST":
        title = request.POST.get('title')
        
        # --- VALIDATION ADDED HERE ---
        # Check if the title is empty or just whitespace
        if not title or not title.strip():
            messages.error(request, 'Title is a required field.')
            return redirect('recipient')
        
        # If validation passes, create the request
        Request.objects.create(
            recipient=recipient,
            title=title,
            description=request.POST.get('description', ''),
            category=request.POST.get('category'),
            urgency=request.POST.get('urgency'),
            status="pending"
        )
        messages.success(request, 'Request submitted successfully!')
        return redirect('recipient')

    # Read category from GET
    selected_category = request.GET.get("category")

    # Get recipient requests (changed from requests_list to my_requests as per requirements)
    my_requests = Request.objects.filter(recipient=recipient).order_by('-created_at')
    
    # Filter requests by category if selected
    if selected_category:
        my_requests = my_requests.filter(category=selected_category)
    
    # Fetch distinct request categories for dropdown
    categories = Request.objects.values_list("category", flat=True).distinct()

    # Get available donations to browse
    donations = Donation.objects.filter(status='pending')
    
    # --- ADDED STATS FOR DASHBOARD VIEW ---
    total_requests = my_requests.count()
    pending_requests = my_requests.filter(status='pending').count()
    fulfilled_requests = my_requests.filter(status='fulfilled').count()

    context = {
        'recipient': recipient,
        'my_requests': my_requests,  # Changed from 'requests' to 'my_requests'
        'requests': my_requests,     # Keep original for backward compatibility
        'donations': donations,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'fulfilled_requests': fulfilled_requests,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'recipient_dashboard.html', context)

# ---------------- UPDATE REQUEST ----------------
def update_request(request, request_id):
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Must be recipient
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'recipient':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('login')

    # Use get_object_or_404 to fetch the request only if it belongs to the logged-in user
    recipient_request = get_object_or_404(Request, id=request_id, recipient__user=request.user)

    # Handle update submission
    if request.method == 'POST':
        try:
            recipient_request.title = request.POST.get('title')
            recipient_request.description = request.POST.get('description', '')
            recipient_request.category = request.POST.get('category')
            recipient_request.urgency = request.POST.get('urgency')
            recipient_request.status = request.POST.get('status')
            recipient_request.save()
            messages.success(request, 'Request updated successfully!')
        except Exception as e:
            logger.error(f'Error updating request: {e}')
            messages.error(request, 'Failed to update request')
        
        return redirect('recipient')
    else:
        # For GET request, render the edit form template
        context = {
            'request_obj': recipient_request
        }
        return render(request, 'edit_request.html', context)


# ---------------- DELETE REQUEST ----------------
def delete_request(request, request_id):
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Must be recipient
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'recipient':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('login')

    # Use get_object_or_404 to fetch the request only if it belongs to the logged-in user
    recipient_request = get_object_or_404(Request, id=request_id, recipient__user=request.user)

    # Handle the actual deletion on POST
    if request.method == 'POST':
        try:
            recipient_request.delete()
            messages.success(request, 'Request deleted successfully!')
        except Exception as e:
            logger.error(f'Error deleting request: {e}')
            messages.error(request, 'Failed to delete request.')
        
        return redirect('recipient')
    
    # If it's a GET request, render a confirmation page
    context = {
        'request_obj': recipient_request
    }
    return render(request, 'delete_request.html', context)

# ---------------- NGO DASHBOARD ----------------
def ngo_dashboard(request):
    # Ensure logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')

    # Get filter parameters
    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    # ----- DASHBOARD STATISTICS -----
    
    # Total counts
    total_donations = Donation.objects.count()
    pending_requests = Request.objects.filter(status='pending').count()
    accepted_donations = Donation.objects.filter(status='accepted').count()
    delivered_donations = Donation.objects.filter(status='delivered').count()
    fulfilled_requests = Request.objects.filter(status='fulfilled').count()
    
    # Average rating
    avg_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    # Active donors (donors who have made at least one donation)
    active_donors = Donor.objects.filter(donation__isnull=False).distinct().count()

    stats = {
        'total_donations': total_donations,
        'pending_requests': pending_requests,
        'accepted_donations': accepted_donations,
        'delivered_donations': delivered_donations,
        'fulfilled_requests': fulfilled_requests,
        'avg_rating': avg_rating,
        'active_donors': active_donors,
    }

    # ----- DONATIONS DATA -----
    donations = Donation.objects.select_related('donor').all()
    
    # Apply category filter
    if selected_category:
        donations = donations.filter(category=selected_category)
    
    # Apply search filter
    if search_query:
        donations = donations.filter(
            Q(title__icontains=search_query) |
            Q(donor__name__icontains=search_query) |
            Q(donor__city__icontains=search_query)
        )
    
    donations = donations.order_by('-created_at')
    
    # Get all unique categories for filter dropdown
    available_categories = Donation.objects.values_list('category', flat=True).distinct().order_by('category')

    # ----- REQUESTS DATA -----
    requests = Request.objects.select_related('recipient').order_by('-created_at')



    # ----- ANALYTICS DATA -----
    
    # Donations by category
    donations_by_category = Donation.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')

    # Top 5 donor cities
    top_cities = Donation.objects.values('donor__city').annotate(
        count=Count('id')
    ).filter(donor__city__isnull=False).exclude(donor__city='').order_by('-count')[:5]

    # Format top cities data
    top_cities_formatted = []
    for city_data in top_cities:
        if city_data['donor__city']:
            top_cities_formatted.append({
                'city': city_data['donor__city'],
                'count': city_data['count']
            })

    # Request urgency distribution
    urgency_distribution = Request.objects.values('urgency').annotate(
        count=Count('id')
    ).order_by('urgency')

    # Monthly donation trend (last 6 months)
    from django.db.models.functions import TruncMonth
    from datetime import timedelta
    
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_donations = Donation.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    monthly_requests = Request.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # ----- CONTEXT -----
    context = {
        'ngo': ngo,
        'stats': stats,
        'donations': donations,
        'requests': requests,
        'available_categories': available_categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'donations_by_category': donations_by_category,
        'top_cities': top_cities_formatted,
        'urgency_distribution': urgency_distribution,
        'monthly_donations': monthly_donations,
        'monthly_requests': monthly_requests,
    }

    return render(request, 'ngo_dashboard.html', context)


# ---------------- API ENDPOINTS FOR NGO DASHBOARD ----------------
def donors_api(request):
    """
    API endpoint to get all donors data for the NGO dashboard
    """
    donors = Donor.objects.select_related('user').all()
    donors_data = []
    
    for donor in donors:
        donors_data.append({
            'name': donor.name,
            'email': donor.user.email if donor.user else '',
            'phone': donor.phone,
            'city': donor.city,
            'state': donor.state,
        })
    
    return JsonResponse(donors_data, safe=False)


def recipients_api(request):
    """
    API endpoint to get all recipients data for the NGO dashboard
    """
    recipients = Recipient.objects.select_related('user').all()
    recipients_data = []
    
    for recipient in recipients:
        recipients_data.append({
            'name': recipient.name,
            'email': recipient.user.email if recipient.user else '',
            'phone': recipient.phone,
            'family_size': recipient.family_size,
            'city': recipient.city,
            'urgency': recipient.urgency,
        })
    
    return JsonResponse(recipients_data, safe=False)


# ---------------- API ENDPOINTS FOR DBMS DEMO ----------------
def dbms_demo_inner_join(request):
    """
    API endpoint to demonstrate INNER JOIN between donations and donors
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        donations_with_donors = Donation.objects.select_related('donor').filter(
            donor__isnull=False
        ).values(
            'title', 'category', 'status', 'donor__name'
        )
        
        # Format the results
        results = []
        for item in donations_with_donors:
            results.append([
                item['title'] if item['title'] else 'N/A',
                item['category'] if item['category'] else 'N/A',
                item['donor__name'] if item['donor__name'] else 'N/A',
                item['status'] if item['status'] else 'N/A'
            ])
        
        # Handle case when no data is available
        if not results:
            results = [['No data available', 'N/A', 'N/A', 'N/A']]
    except Exception as e:
        results = [['Error loading data', str(e), '', '']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT D.title, D.category, DO.name AS donor_name, D.status
FROM donations AS D
INNER JOIN donors AS DO ON D.donor_id = DO.id;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Donation Title', 'Category', 'Donor Name', 'Status'],
        'results': results
    })


def dbms_demo_left_join(request):
    """
    API endpoint to demonstrate LEFT JOIN between requests and recipients
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        requests_with_recipients = Request.objects.select_related('recipient').values(
            'title', 'status', 'recipient__name', 'recipient__city'
        )
        
        # Format the results
        results = []
        for item in requests_with_recipients:
            recipient_name = item['recipient__name'] if item['recipient__name'] else 'NULL'
            recipient_city = item['recipient__city'] if item['recipient__city'] else 'NULL'
            results.append([
                item['title'] if item['title'] else 'N/A',
                recipient_name,
                item['status'] if item['status'] else 'N/A',
                recipient_city
            ])
        
        # Handle case when no data is available
        if not results:
            results = [['No data available', 'NULL', 'N/A', 'NULL']]
    except Exception as e:
        results = [['Error loading data', 'NULL', str(e), 'NULL']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT R.title, RE.name AS recipient_name, R.status, RE.city
FROM requests AS R
LEFT JOIN recipients AS RE ON R.recipient_id = RE.id;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Request Title', 'Recipient Name', 'Status', 'City'],
        'results': results
    })


def dbms_demo_right_join(request):
    """
    API endpoint to demonstrate RIGHT JOIN between donors and donations
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        donors_with_donations = Donor.objects.prefetch_related('donation_set').all()
        
        # Format the results
        results = []
        for donor in donors_with_donations:
            donations = donor.donation_set.all()
            if donations.exists():
                for donation in donations:
                    results.append([
                        donor.name if donor.name else 'N/A',
                        donor.city if donor.city else 'N/A',
                        donation.title if donation.title else 'N/A',
                        donation.status if donation.status else 'N/A'
                    ])
            else:
                results.append([
                    donor.name if donor.name else 'N/A',
                    donor.city if donor.city else 'N/A',
                    'NULL',
                    'NULL'
                ])
        
        # Handle case when no data is available
        if not results:
            results = [['No data available', 'N/A', 'NULL', 'NULL']]
    except Exception as e:
        results = [['Error loading data', str(e), 'NULL', 'NULL']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT DO.name AS donor_name, DO.city, D.title AS donation_title, D.status
FROM donors AS DO
RIGHT JOIN donations AS D ON DO.id = D.donor_id;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Donor Name', 'City', 'Donation Title', 'Status'],
        'results': results
    })


def dbms_demo_self_join(request):
    """
    API endpoint to demonstrate SELF JOIN between recipients
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the self join query using raw SQL since Django ORM doesn't directly support self joins
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT A.name, B.name, A.city
                FROM recipients A, recipients B
                WHERE A.id <> B.id AND A.city = B.city
                LIMIT 10
            """)
            rows = cursor.fetchall()
        
        # Format the results
        results = []
        for row in rows:
            results.append([row[0] if row[0] else 'N/A', row[1] if row[1] else 'N/A', row[2] if row[2] else 'N/A'])
        
        # Handle case when no data is available
        if not results:
            results = [['No matching recipients', 'N/A', 'N/A']]
    except Exception as e:
        results = [['Error loading data', str(e), 'N/A']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT A.name, B.name, A.city
FROM recipients A, recipients B
WHERE A.id <> B.id AND A.city = B.city;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Recipient Name', 'Other Recipient', 'City'],
        'results': results
    })


def dbms_demo_complex_join(request):
    """
    API endpoint to demonstrate COMPLEX JOIN between donations, donors, and NGOs
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        donations_with_donors_ngos = Donation.objects.select_related(
            'donor', 'ngo'
        ).filter(
            status='accepted'
        ).values(
            'title', 'category', 'status', 'donor__name', 'ngo__ngo_name'
        )
        
        # Format the results
        results = []
        for item in donations_with_donors_ngos:
            ngo_name = item['ngo__ngo_name'] if item['ngo__ngo_name'] else 'NULL'
            results.append([
                item['title'] if item['title'] else 'N/A',
                item['donor__name'] if item['donor__name'] else 'N/A',
                ngo_name,
                item['category'] if item['category'] else 'N/A',
                item['status'] if item['status'] else 'N/A'
            ])
        
        # Handle case when no data is available
        if not results:
            results = [['No accepted donations', 'N/A', 'NULL', 'N/A', 'accepted']]
    except Exception as e:
        results = [['Error loading data', str(e), 'NULL', 'N/A', 'N/A']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT D.title, DO.name AS donor_name, N.ngo_name, D.category, D.status
FROM donations AS D
INNER JOIN donors AS DO ON D.donor_id = DO.id
INNER JOIN ngos AS N ON D.ngo_id = N.id
WHERE D.status = 'accepted';"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Donation Title', 'Donor Name', 'NGO Name', 'Category', 'Status'],
        'results': results
    })


def dbms_demo_full_join(request):
    """
    API endpoint to demonstrate FULL JOIN between donations, donors, and NGOs
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        donations_with_all = Donation.objects.select_related(
            'donor', 'ngo'
        ).values(
            'title', 'category', 'status', 'donor__name', 'ngo__ngo_name'
        ).order_by('-created_at')
        
        # Format the results
        results = []
        for item in donations_with_all:
            donor_name = item['donor__name'] if item['donor__name'] else 'NULL'
            ngo_name = item['ngo__ngo_name'] if item['ngo__ngo_name'] else 'NULL'
            results.append([
                item['title'] if item['title'] else 'N/A',
                donor_name,
                ngo_name,
                item['status'] if item['status'] else 'N/A',
                item['category'] if item['category'] else 'N/A'
            ])
        
        # Handle case when no data is available
        if not results:
            results = [['No donations', 'NULL', 'NULL', 'N/A', 'N/A']]
    except Exception as e:
        results = [['Error loading data', 'NULL', 'NULL', str(e), 'N/A']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT D.title AS donation_title, DO.name AS donor_name, N.ngo_name, D.status, D.category
FROM donations AS D
LEFT JOIN donors AS DO ON D.donor_id = DO.id
LEFT JOIN ngos AS N ON D.ngo_id = N.id
ORDER BY D.created_at DESC;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Donation Title', 'Donor Name', 'NGO Name', 'Status', 'Category'],
        'results': results
    })


def dbms_demo_request_full_join(request):
    """
    API endpoint to demonstrate COMPLETE REQUEST JOIN with recipient details
    Returns both the query results and the SQL query string
    """
    try:
        # Execute the join query
        requests_with_recipients = Request.objects.select_related(
            'recipient'
        ).values(
            'title', 'status', 'category', 'urgency', 
            'recipient__name', 'recipient__family_size'
        ).order_by('-created_at')
        
        # Format the results
        results = []
        for item in requests_with_recipients:
            recipient_name = item['recipient__name'] if item['recipient__name'] else 'NULL'
            family_size = item['recipient__family_size'] if item['recipient__family_size'] else 'NULL'
            results.append([
                item['title'] if item['title'] else 'N/A',
                recipient_name,
                family_size,
                item['urgency'] if item['urgency'] else 'N/A',
                item['category'] if item['category'] else 'N/A',
                item['status'] if item['status'] else 'N/A'
            ])
        
        # Handle case when no data is available
        if not results:
            results = [['No requests', 'NULL', 'NULL', 'N/A', 'N/A', 'N/A']]
    except Exception as e:
        results = [['Error loading data', 'NULL', 'NULL', str(e), 'N/A', 'N/A']]
    
    # SQL query string for educational purposes
    sql_query = """SELECT R.title AS request_title, RE.name AS recipient_name, RE.family_size, 
       R.urgency, R.category, R.status
FROM requests AS R
INNER JOIN recipients AS RE ON R.recipient_id = RE.id
ORDER BY R.created_at DESC;"""
    
    return JsonResponse({
        'query': sql_query,
        'headers': ['Request Title', 'Recipient Name', 'Family Size', 'Urgency', 'Category', 'Status'],
        'results': results
    })


# ---------------- NGO ACTION ENDPOINTS ----------------
def accept_donation(request, donation_id):
    """Accept a pending donation"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the donation and update its status
    try:
        donation = Donation.objects.get(id=donation_id, status='pending')
        donation.status = 'accepted'
        donation.ngo = ngo  # Assign the NGO that accepted the donation
        donation.save()
        messages.success(request, 'Donation accepted successfully!')
    except Donation.DoesNotExist:
        messages.error(request, 'Donation not found or already processed.')
    
    return redirect('ngo')


def decline_donation(request, donation_id):
    """Decline a pending donation"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the donation and update its status
    try:
        donation = Donation.objects.get(id=donation_id, status='pending')
        donation.status = 'cancelled'
        donation.ngo = ngo  # Assign the NGO that declined the donation
        donation.save()
        messages.success(request, 'Donation declined successfully!')
    except Donation.DoesNotExist:
        messages.error(request, 'Donation not found or already processed.')
    
    return redirect('ngo')


def accept_request(request, request_id):
    """Accept a pending request"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the request and update its status
    try:
        recipient_request = Request.objects.get(id=request_id, status='pending')
        recipient_request.status = 'accepted'
        recipient_request.save()
        messages.success(request, 'Request accepted successfully!')
    except Request.DoesNotExist:
        messages.error(request, 'Request not found or already processed.')
    
    return redirect('ngo')


def decline_request(request, request_id):
    """Decline a pending request"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the request and update its status
    try:
        recipient_request = Request.objects.get(id=request_id, status='pending')
        recipient_request.status = 'cancelled'
        recipient_request.save()
        messages.success(request, 'Request declined successfully!')
    except Request.DoesNotExist:
        messages.error(request, 'Request not found or already processed.')
    
    return redirect('ngo')


def mark_delivered(request, donation_id):
    """Mark an accepted donation as delivered"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the donation and update its status
    try:
        donation = Donation.objects.get(id=donation_id, status='accepted')
        donation.status = 'delivered'
        donation.save()
        messages.success(request, 'Donation marked as delivered!')
    except Donation.DoesNotExist:
        messages.error(request, 'Donation not found or not in accepted status.')
    
    return redirect('ngo')


def mark_fulfilled(request, request_id):
    """Mark an accepted request as fulfilled"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Get the request and update its status
    try:
        recipient_request = Request.objects.get(id=request_id, status='accepted')
        recipient_request.status = 'fulfilled'
        recipient_request.save()
        messages.success(request, 'Request marked as fulfilled!')
    except Request.DoesNotExist:
        messages.error(request, 'Request not found or not in accepted status.')
    
    return redirect('ngo')


# ---------------- FEEDBACK VIEWS ----------------
def donor_feedback(request):
    """Handle feedback for donors"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is donor
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'donor':
            return redirect('home')
        donor = Donor.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, Donor.DoesNotExist):
        messages.error(request, 'Donor profile not found')
        return redirect('login')
    
    # Handle feedback submission
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        donation_id = request.POST.get('donation')
        
        # Validation
        if not rating or not comment or not donation_id:
            messages.error(request, 'All fields are required.')
        elif int(rating) < 1 or int(rating) > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
        else:
            try:
                # Verify the donation belongs to this donor
                donation = Donation.objects.get(id=donation_id, donor=donor)
                
                # Create feedback
                Feedback.objects.create(
                    user=request.user,
                    donation=donation,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Feedback submitted successfully!')
            except Donation.DoesNotExist:
                messages.error(request, 'Invalid donation selected.')
            except Exception as e:
                messages.error(request, 'Failed to submit feedback.')
        
        return redirect('donor_feedback')
    
    # Get donations related to this donor
    donations = Donation.objects.filter(donor=donor).order_by('-created_at')
    
    # Get past feedback from this user
    feedback_list = Feedback.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'donor': donor,
        'donations': donations,
        'feedback_list': feedback_list,
    }
    return render(request, 'donor_feedback.html', context)


def recipient_feedback(request):
    """Handle feedback for recipients"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is recipient
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'recipient':
            return redirect('home')
        recipient = Recipient.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, Recipient.DoesNotExist):
        messages.error(request, 'Recipient profile not found')
        return redirect('login')
    
    # Handle feedback submission
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        donation_id = request.POST.get('donation')
        
        # Validation
        if not rating or not comment or not donation_id:
            messages.error(request, 'All fields are required.')
        elif int(rating) < 1 or int(rating) > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
        else:
            try:
                # Verify the donation is accepted
                donation = Donation.objects.get(id=donation_id, status='accepted')
                
                # Create feedback
                Feedback.objects.create(
                    user=request.user,
                    donation=donation,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Feedback submitted successfully!')
            except Donation.DoesNotExist:
                messages.error(request, 'Invalid donation selected.')
            except Exception as e:
                messages.error(request, 'Failed to submit feedback.')
        
        return redirect('recipient_feedback')
    
    # Get accepted donations
    donations = Donation.objects.filter(status='accepted').order_by('-created_at')
    
    # Get past feedback from this user
    feedback_list = Feedback.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'recipient': recipient,
        'donations': donations,
        'feedback_list': feedback_list,
    }
    return render(request, 'recipient_feedback.html', context)


def edit_feedback(request, id):
    """Edit recipient feedback"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is recipient
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'recipient':
            return redirect('home')
        recipient = Recipient.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, Recipient.DoesNotExist):
        messages.error(request, 'Recipient profile not found')
        return redirect('login')
    
    # Get the feedback object, ensuring it belongs to the current user
    try:
        feedback = Feedback.objects.get(feedback_id=id, user=request.user)
    except Feedback.DoesNotExist:
        messages.error(request, 'Feedback not found.')
        return redirect('recipient_feedback')
    
    # Handle feedback update
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Validation
        if not rating or not comment:
            messages.error(request, 'All fields are required.')
        elif int(rating) < 1 or int(rating) > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
        else:
            try:
                # Update feedback
                feedback.rating = rating
                feedback.comment = comment
                feedback.save()
                messages.success(request, 'Feedback updated successfully!')
                return redirect('recipient_feedback')
            except Exception as e:
                messages.error(request, 'Failed to update feedback.')
    
    # Get accepted donations for the dropdown (but keep the current donation)
    donations = Donation.objects.filter(status='accepted').order_by('-created_at')
    
    context = {
        'recipient': recipient,
        'feedback': feedback,
        'donations': donations,
    }
    return render(request, 'recipient_feedback.html', context)


def delete_feedback(request, id):
    """Delete recipient feedback"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is recipient
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'recipient':
            return redirect('home')
        recipient = Recipient.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, Recipient.DoesNotExist):
        messages.error(request, 'Recipient profile not found')
        return redirect('login')
    
    # Get the feedback object, ensuring it belongs to the current user
    try:
        feedback = Feedback.objects.get(feedback_id=id, user=request.user)
    except Feedback.DoesNotExist:
        messages.error(request, 'Feedback not found.')
        return redirect('recipient_feedback')
    
    # Handle feedback deletion
    if request.method == 'POST':
        try:
            feedback.delete()
            messages.success(request, 'Feedback deleted successfully!')
        except Exception as e:
            messages.error(request, 'Failed to delete feedback.')
        return redirect('recipient_feedback')
    
    # For GET request, show confirmation page
    context = {
        'recipient': recipient,
        'feedback': feedback,
    }
    return render(request, 'recipient_feedback.html', context)


def ngo_feedback(request):
    """Handle feedback for NGOs"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user is NGO
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'ngo':
            return redirect('home')
        ngo = NGO.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, NGO.DoesNotExist):
        messages.error(request, 'NGO profile not found')
        return redirect('login')
    
    # Handle feedback submission
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        donation_id = request.POST.get('donation')
        
        # Validation
        if not rating or not comment or not donation_id:
            messages.error(request, 'All fields are required.')
        elif int(rating) < 1 or int(rating) > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
        else:
            try:
                # Verify the donation belongs to this NGO
                donation = Donation.objects.get(id=donation_id, ngo=ngo)
                
                # Create feedback
                Feedback.objects.create(
                    user=request.user,
                    donation=donation,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Feedback submitted successfully!')
            except Donation.DoesNotExist:
                messages.error(request, 'Invalid donation selected.')
            except Exception as e:
                messages.error(request, 'Failed to submit feedback.')
        
        return redirect('ngo_feedback')
    
    # Get donations related to this NGO
    donations = Donation.objects.filter(ngo=ngo).order_by('-created_at')
    
    # Get past feedback from this user
    feedback_list = Feedback.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'ngo': ngo,
        'donations': donations,
        'feedback_list': feedback_list,
    }
    return render(request, 'ngo_feedback.html', context)
