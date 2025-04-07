import requests
import uuid
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class ChapaPayment:
    def __init__(self):
      self.secret_key = settings.CHAPA_SECRET_KEY
      self.public_key = settings.CHAPA_PUBLIC_KEY
      self.base_url = settings.CHAPA_API_URL
      self.webhook_url = settings.CHAPA_WEBHOOK_URL

    def initialize_payment(self, amount, email, currency='ETB', **kwargs):
        """Initialize payment with Chapa"""
        tx_ref = kwargs.get('tx_ref', str(uuid.uuid4()))
        
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": str(amount),
            "currency": currency,
            "email": email,
            "tx_ref": tx_ref,
            "callback_url": kwargs.get('callback_url', ''),
            "return_url": kwargs.get('return_url', ''),
            "first_name": kwargs.get('first_name', ''),
            "last_name": kwargs.get('last_name', ''),
            "customization": {
                "title": kwargs.get('title', 'Payment'),
                "description": kwargs.get('description', '')
            }
        }

        response = requests.post(
            f"{self.base_url}/initialize",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            return {
                'success': True,
                'checkout_url': response.json()['data']['checkout_url'],
                'tx_ref': tx_ref
            }
        return {
            'success': False,
            'message': response.json().get('message', 'Payment initialization failed')
        }

    def verify_payment(self, tx_ref):
        """Verify payment status with Chapa"""
        headers = {
            "Authorization": f"Bearer {self.secret_key}"
        }

        response = requests.get(
            f"{self.base_url}/verify/{tx_ref}",
            headers=headers
        )

        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()['data']
            }
        return {
            'success': False,
            'message': response.json().get('message', 'Payment verification failed')
        }