from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from django.utils import timezone
import logging

from .models import UserProfile, Donor, NGO, Recipient, Donation, Feedback, Request, Match
from .forms import SignupStep1Form, DonorProfileForm, NGOProfileForm, RecipientProfileForm

logger = logging.getLogger(__name__)


# ---------------- HOME ----------------
def home(request):
    return render(request, "home.html")


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
# ---------------- DONOR DASHBOARD ----------------
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

    # ✅ Handle new donation submission
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
        
        return redirect('donor')  # Refresh page

    # ✅ Get donor's past donations
    donations = Donation.objects.filter(donor=donor).order_by('-created_at')

    # ✅ Calculate dashboard stats using aggregate functions
    from django.db.models import Count, Sum
    
    # Total donations count
    total_donations = donations.count()
    
    # Delivered donations count
    delivered_donations = donations.filter(status='delivered').count()
    
    # Calculate total items delivered (sum of quantities)
    total_items_delivered = donations.filter(status='delivered').aggregate(
        total_quantity=Sum('quantity')
    )['total_quantity'] or 0
    
    # Impact score calculation (using total items delivered)
    impact_score = total_items_delivered * 10
    
    # Thank you notes (assuming these come from feedback related to this donor's delivered donations)
    # For now, we'll count feedback entries related to matches of this donor's delivered donations
    from .models import Match, Feedback
    donor_matches = Match.objects.filter(donation__donor=donor, donation__status='delivered')
    thank_you_notes = Feedback.objects.filter(match_id__in=donor_matches.values_list('id', flat=True)).count()

    context = {
        'donor': donor,
        'donations': donations,
        'total_donations': total_donations,
        'delivered_donations': delivered_donations,
        'impact_score': impact_score,
        'thank_you_notes': thank_you_notes,
    }
    return render(request, 'donor_dashboard.html', context)

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

    try:
        donor = Donor.objects.get(user=request.user)
        donation = Donation.objects.get(donation_id=donation_id, donor=donor)
    except (Donor.DoesNotExist, Donation.DoesNotExist):
        messages.error(request, 'Donation not found')
        return redirect('donor')

    # Handle update submission
    if request.method == 'POST':
        try:
            donation.title = request.POST.get('title')
            donation.description = request.POST.get('description', '')
            donation.category = request.POST.get('category')
            donation.quantity = int(request.POST.get('quantity', 1))
            donation.image_url = request.POST.get('image_url', '')
            donation.save()
            messages.success(request, 'Donation updated successfully!')
        except Exception as e:
            logger.error(f'Error updating donation: {e}')
            messages.error(request, 'Failed to update donation')
        
        return redirect('donor')
    else:
        # For GET request, return donation data as JSON for the modal
        donation_data = {
            'donation_id': donation.donation_id,
            'title': donation.title,
            'description': donation.description,
            'category': donation.category,
            'quantity': donation.quantity,
            'image_url': donation.image_url
        }
        return JsonResponse(donation_data)

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

    try:
        donor = Donor.objects.get(user=request.user)
        donation = Donation.objects.get(donation_id=donation_id, donor=donor)
    except (Donor.DoesNotExist, Donation.DoesNotExist):
        messages.error(request, 'Donation not found')
        return redirect('donor')

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
        # For GET request, return donation data for confirmation
        donation_data = {
            'donation_id': donation.donation_id,
            'title': donation.title,
            'category': donation.category,
            'quantity': donation.quantity
        }
        return JsonResponse(donation_data)

# ---------------- RECIPIENT DASHBOARD ----------------
def recipient_dashboard(request):
    # Ensure logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure user is recipient
    recipient = Recipient.objects.get(user=request.user)

    # Handle new request submission
    if request.method == "POST":
        Request.objects.create(
            recipient=recipient,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            category=request.POST.get('category'),
            urgency=request.POST.get('urgency'),
            status="pending"
        )
        return redirect('recipient')  # Refresh page after submit

    # Get recipient requests
    requests_list = Request.objects.filter(recipient=recipient).order_by('-created_at')

    # Get available donations to browse
    donations = Donation.objects.filter(status='pending')

    context = {
        'recipient': recipient,
        'requests': requests_list,
        'donations': donations,
    }
    return render(request, 'recipient_dashboard.html', context)


# ---------------- NGO DASHBOARD ----------------
def ngo_dashboard(request):
    # Example NGO (temporary until authentication)
    ngo = NGO.objects.first()

    # Category filter from GET
    selected_category = request.GET.get('category')

    # Get all unique donation categories
    available_categories = Donation.objects.values_list('category', flat=True).distinct()

    # Filter donations by selected category (if provided)
    donations = Donation.objects.all()
    if selected_category:
        donations = donations.filter(category=selected_category)

    # ----- Dashboard Statistics -----
    donor_count = Donor.objects.count()
    recipient_count = Recipient.objects.count()
    donation_count = donations.count()
    delivered_count = donations.filter(status='delivered').count()

    # Donations by category (use correct PK field)
    donations_by_category = donations.values('category').annotate(
        count=Count('donation_id')
    ).filter(count__gt=0).order_by('-count')

    # Top cities by donation count (from Donors)
    top_cities = Donor.objects.values('city').annotate(
        count=Count('city')
    ).filter(count__gt=0).order_by('-count')[:5]

    # Average rating (handle no feedback gracefully)
    avg_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    stats = {
        'donor_count': donor_count,
        'recipient_count': recipient_count,
        'donation_count': donation_count,
        'delivered_count': delivered_count,
        'avg_rating': avg_rating,
        'top_cities': top_cities,
        'donations_by_category': donations_by_category,
    }

    # ----- Table Data -----
    donors = Donor.objects.select_related('user').all()
    recipients = Recipient.objects.select_related('user').all()

    # ✅ Fetch all matches (join with Donation, Request, NGO)
    matches = Match.objects.select_related('donation', 'request', 'ngo').all()

    # ----- Context -----
    context = {
        'ngo': ngo,
        'stats': stats,
        'available_categories': available_categories,
        'selected_category': selected_category,
        'donors': donors,
        'recipients': recipients,
        'matches': matches,
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
            'email': donor.user.email,
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
            'email': recipient.user.email,
            'phone': recipient.phone,
            'family_size': recipient.family_size,
            'city': recipient.city,
            'urgency': recipient.urgency,
        })
    
    return JsonResponse(recipients_data, safe=False)

