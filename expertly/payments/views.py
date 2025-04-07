# payments/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from appointment.models import Appointment
from .models import Payment
from django.conf import settings
from .services.chapa import ChapaPayment
from .serializers import PaymentSerializer, InitiatePaymentSerializer

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = Appointment.objects.get(
                id=serializer.validated_data['appointment_id'],
                client=request.user.client_profile,
                status='accepted'  # Only allow payment for accepted appointments
            )
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Appointment not found or not eligible for payment'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent duplicate payments
        if hasattr(appointment, 'payment'):
            return Response(
                {'error': 'Payment already exists for this appointment'},
                status=status.HTTP_400_BAD_REQUEST
            )

        chapa = ChapaPayment()
        result = chapa.initialize_payment(
            amount=serializer.validated_data['amount'],
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            callback_url=settings.CHAPA_WEBHOOK_URL,
            return_url=settings.CHAPA_RETURN_URL,
            failure_url=settings.CHAPA_FAILURE_URL,
            metadata={
                'appointment_id': appointment.id,
                'user_id': request.user.id
            }
        )

        if not result['success']:
            return Response(
                {'error': result['message']},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.create(
            appointment=appointment,
            amount=serializer.validated_data['amount'],
            currency=serializer.validated_data['currency'],
            tx_ref=result['tx_ref'],
            status='pending'
        )

        return Response({
            'checkout_url': result['checkout_url'],
            'payment_id': payment.id,
            'appointment_id': appointment.id,
            'status_check_url': f'/api/payments/status/{payment.id}/'
        }, status=status.HTTP_200_OK)

class PaymentWebhookView(APIView):
    def post(self, request):
        tx_ref = request.data.get('tx_ref')
        if not tx_ref:
            return Response({'error': 'Missing transaction reference'}, status=400)
        
        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            if payment.status == 'completed':
                return Response({'status': 'already_processed'})
            
            chapa = ChapaPayment()
            verification = chapa.verify_payment(tx_ref)
            
            if verification['success']:
                payment.status = 'completed'
                payment.chapa_transaction_id = verification['data']['id']
                payment.save()
                
                # Confirm the appointment
                appointment = payment.appointment
                appointment.status = 'confirmed'
                appointment.save()
                
                # Notify expert and client
                # send_confirmation_notifications(appointment)
                
                return Response({'status': 'success'})
            
            # Mark as failed
            payment.status = 'failed'
            payment.save()
            return Response({'error': verification['message']}, status=400)
        
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=404)

class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(
                id=payment_id,
                appointment__client=request.user.client_profile
            )
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    def post(self, request):
        tx_ref = request.data.get('tx_ref')
        if not tx_ref:
            return Response({'error': 'Missing transaction reference'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            chapa = ChapaPayment()
            verification = chapa.verify_payment(tx_ref)
            
            if verification['success']:
                payment.status = 'completed'
                payment.chapa_transaction_id = verification['data']['id']
                payment.save()
                
                # Update related appointment status if exists
                if hasattr(payment, 'appointment'):
                    payment.appointment.status = 'confirmed'
                    payment.appointment.save()
                
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            
            payment.status = 'failed'
            payment.save()
            return Response({'error': verification['message']}, status=status.HTTP_400_BAD_REQUEST)
        
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PaymentSuccessView(APIView):

    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        if not tx_ref:
            return Response(
                {'error': 'Transaction reference (tx_ref) is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            
            # For API testing, verify payment status again
            chapa = ChapaPayment()
            verification = chapa.verify_payment(tx_ref)
            
            if verification['success']:
                payment.status = 'completed'
                payment.chapa_transaction_id = verification['data']['id']
                payment.save()
                
                if hasattr(payment, 'appointment'):
                    payment.appointment.status = 'confirmed'
                    payment.appointment.save()

                return Response({
                    'status': 'success',
                    'payment_id': payment.id,
                    'amount': payment.amount,
                    'chapa_transaction_id': payment.chapa_transaction_id
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 'failed',
                'message': 'Payment verification failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PaymentFailView(APIView):

    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        if not tx_ref:
            return Response(
                {'error': 'Transaction reference (tx_ref) is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            payment.status = 'failed'
            payment.save()

            return Response({
                'status': 'failed',
                'payment_id': payment.id,
                'message': 'Payment failed or was cancelled'
            }, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )