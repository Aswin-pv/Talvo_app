import requests
from django.shortcuts import render


class CheckInternetMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
       
        try:
            # Attempt to connect to a reliable website
            requests.get("https://www.google.com", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            # If the connection fails, render the offline page
            return render(request, 'user/offline.html')

        response = self.get_response(request)
        return response    
