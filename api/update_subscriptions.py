import os
from http.server import BaseHTTPRequestHandler
import requests
import json

API_KEY = os.getenv('API_KEY')

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)

        contact_email = request_data.get('email')

        if not contact_email:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Contact email is required.'}).encode('utf-8'))
            return

        try:
            subscription_types = self.get_all_subscription_types()
            if subscription_types:
                for subscription in subscription_types:
                    self.update_subscription_status(contact_email, subscription)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': f'Subscriptions successfully updated for {contact_email}'}).encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Failed to retrieve subscription types.'}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def get_all_subscription_types(self):
        url = 'https://api.hubapi.com/communication-preferences/v4/definitions'
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('results')
        else:
            raise Exception(f'Failed to retrieve subscription types: {response.status_code}, {response.text}')

    def update_subscription_status(self, contact_email, subscription):
        url = f'https://api.hubapi.com/communication-preferences/v4/statuses/{contact_email}'
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'subscriptionId': int(subscription['id']),
            'statusState': 'SUBSCRIBED',
            'legalBasis': 'LEGITIMATE_INTEREST_OTHER',
            'legalBasisExplanation': 'Updated via API script',
            'channel': 'EMAIL'
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f'Failed to update subscription {subscription["name"]} for {contact_email}: {response.status_code}, {response.text}')
