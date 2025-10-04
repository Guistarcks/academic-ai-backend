#!/usr/bin/env python3
"""
Test rápido del endpoint de registro
"""
import requests
import json

url = "http://127.0.0.1:5000/api/users"
data = {
    "email": "test@ejemplo.com",
    "password": "test123456",
    "nome": "Usuario Test",
    "rol": "user",
    "data_creacao": "2025-10-04"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
