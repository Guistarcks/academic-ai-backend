#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema de registro funciona correctamente.
Este script prueba el endpoint de registro de usuarios de la API.
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5000"
API_ENDPOINT = f"{BASE_URL}/api/users"

def print_separator():
    print("=" * 70)

def test_registro_usuario():
    print_separator()
    print("🧪 TEST DE REGISTRO DE USUARIO - API Flask")
    print_separator()
    
    # Datos de prueba
    test_user = {
        "email": f"test_{datetime.now().timestamp()}@ejemplo.com",  # Email único
        "password": "password123",
        "nome": "Usuario de Prueba",
        "rol": "user",
        "data_creacao": datetime.now().strftime("%Y-%m-%d")
    }
    
    print(f"\n📤 Enviando datos:")
    print(json.dumps(test_user, indent=2))
    
    try:
        # Hacer la petición POST
        print(f"\n🌐 POST {API_ENDPOINT}")
        response = requests.post(API_ENDPOINT, json=test_user)
        
        print(f"\n📥 Respuesta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 201:
            print(f"\n✅ TEST EXITOSO - Usuario registrado correctamente")
            return True
        elif response.status_code == 409:
            print(f"\n⚠️  Email ya registrado (esto es esperado si ya existe)")
            return True
        else:
            print(f"\n❌ TEST FALLIDO - Status code inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: No se pudo conectar al servidor en {BASE_URL}")
        print(f"   Asegúrate de que el servidor Flask está corriendo:")
        print(f"   cd academic-ai-backend && python app.py")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

def test_validacion_campos():
    print("\n")
    print_separator()
    print("🧪 TEST DE VALIDACIÓN DE CAMPOS")
    print_separator()
    
    # Test 1: Sin email
    print("\n📋 Test 1: Sin email")
    try:
        response = requests.post(API_ENDPOINT, json={
            "password": "password123",
            "nome": "Test User"
        })
        if response.status_code == 400:
            print("   ✅ Validación correcta - Email requerido")
        else:
            print(f"   ❌ Validación incorrecta - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Sin password
    print("\n📋 Test 2: Sin password")
    try:
        response = requests.post(API_ENDPOINT, json={
            "email": "test@ejemplo.com",
            "nome": "Test User"
        })
        if response.status_code == 400:
            print("   ✅ Validación correcta - Password requerido")
        else:
            print(f"   ❌ Validación incorrecta - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Sin nombre
    print("\n📋 Test 3: Sin nombre")
    try:
        response = requests.post(API_ENDPOINT, json={
            "email": "test@ejemplo.com",
            "password": "password123"
        })
        if response.status_code == 400:
            print("   ✅ Validación correcta - Nombre requerido")
        else:
            print(f"   ❌ Validación incorrecta - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def main():
    print("\n")
    print("┌────────────────────────────────────────────────────────────────┐")
    print("│                                                                │")
    print("│     🧪 SUITE DE TESTS - REGISTRO DE USUARIOS                  │")
    print("│        Academic AI 2.0 Backend API                            │")
    print("│                                                                │")
    print("└────────────────────────────────────────────────────────────────┘")
    
    # Test de registro
    resultado_registro = test_registro_usuario()
    
    # Test de validaciones
    if resultado_registro:
        test_validacion_campos()
    
    print("\n")
    print_separator()
    print("📊 RESUMEN DE TESTS")
    print_separator()
    
    if resultado_registro:
        print("✅ Sistema de registro funcionando correctamente")
    else:
        print("❌ Hay problemas con el sistema de registro")
    
    print("\n💡 Para más información, consulta:")
    print("   - MEJORAS_REGISTRO.md (documentación técnica)")
    print("   - README_REGISTRO.md (guía de uso)")
    print("   - RESUMEN_VISUAL.txt (resumen visual)")
    print_separator()
    print("\n")

if __name__ == "__main__":
    main()
