from ..services.auth import public_auth_client
from django.shortcuts import render
from django.http import JsonResponse


def get_token(request):
    return JsonResponse({'access_token': public_auth_client['access_token'],
                         'expires_in': public_auth_client['expires_in']})
