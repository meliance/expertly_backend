from django.urls import path
from .views import (
    InitiatePaymentView,
    PaymentWebhookView,
    PaymentSuccessView,
    PaymentFailView,
    PaymentStatusView
)

urlpatterns = [
    path('initialize/', InitiatePaymentView.as_view(), name='initialize-payment'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('fail/', PaymentFailView.as_view(), name='payment-fail'),
    path('status/<int:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),
]