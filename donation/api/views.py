from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .models import Donor, Recipient, NGO, Donation, Feedback
from .serializers import DonorSerializer, RecipientSerializer, NGOSerializer, DonationSerializer, FeedbackSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def superadmin_demo(request):
    # Demonstrate a couple of SQL features for the viva; expand as needed
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_donation")
        donation_count = cursor.fetchone()[0]
        cursor.execute("SELECT city, COUNT(*) AS c FROM api_recipient GROUP BY city HAVING COUNT(*) > 0 ORDER BY c DESC LIMIT 5")
        top_cities = cursor.fetchall()
    return Response({
        'donation_count': donation_count,
        'top_cities': [{'city': row[0], 'count': row[1]} for row in top_cities],
    })


@csrf_exempt
@api_view(['GET', 'POST'])
def donors_list_create(request):
    if request.method == 'GET':
        donors = Donor.objects.all()
        # Don't include password in the response
        serializer = DonorSerializer(donors, many=True)
        data = serializer.data
        for donor in data:
            donor.pop('password', None)
        return Response(data)
    elif request.method == 'POST':
        # Handle password hashing
        password = request.data.get('password')
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor = serializer.save()
            if password:
                donor.set_password(password)
                donor.save()
            # Don't include password in the response
            response_data = serializer.data
            response_data.pop('password', None)
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def recipients_list_create(request):
    if request.method == 'GET':
        items = Recipient.objects.all()
        return Response(RecipientSerializer(items, many=True).data)
    serializer = RecipientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET', 'POST'])
def ngos_list_create(request):
    if request.method == 'GET':
        items = NGO.objects.all()
        return Response(NGOSerializer(items, many=True).data)
    serializer = NGOSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET', 'POST'])
def donations_list_create(request):
    if request.method == 'GET':
        items = Donation.objects.select_related('donor', 'ngo').all()
        return Response(DonationSerializer(items, many=True).data)
    serializer = DonationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def donor_detail(request, donor_id):
    try:
        donor = Donor.objects.get(donor_id=donor_id)
        serializer = DonorSerializer(donor)
        # Don't include password in the response
        data = serializer.data
        data.pop('password', None)
        return Response(data)
    except Donor.DoesNotExist:
        return Response({'error': 'Donor not found'}, status=404)


@csrf_exempt
@api_view(['POST'])
def match_donation(request):
    # naive matching by city: assign an NGO in same city as donor if available
    donation_id = request.data.get('donation_id')
    try:
        donation = Donation.objects.select_related('donor').get(donation_id=donation_id)
    except Donation.DoesNotExist:
        return Response({'error': 'donation not found'}, status=404)
    ngo = NGO.objects.filter(city=donation.donor.city).first()
    if ngo:
        donation.ngo = ngo
        donation.status = 'matched'
        donation.save()
        return Response({'matched': True, 'ngo_id': ngo.ngo_id})
    return Response({'matched': False})