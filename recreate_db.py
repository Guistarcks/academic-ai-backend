#!/usr/bin/env python3
"""
Script para recrear la base de datos con la nueva estructura
que incluye la restricción UNIQUE en el campo email de la tabla users.

ADVERTENCIA: Este script eliminará la base de datos existente.
Asegúrate de hacer un backup si tienes datos importantes.
"""

import os
import sqlite3
import db_controller

def recreate_database():
    db_file = 'academicia.db'
    
    # Crear backup si existe
    if os.path.exists(db_file):
        backup_file = f'{db_file}.backup'
        print(f"⚠️  Base de datos existente encontrada.")
        print(f"📦 Creando backup en: {backup_file}")
        
        # Copiar la base de datos actual
        import shutil
        shutil.copy2(db_file, backup_file)
        
        # Eliminar la base de datos actual
        os.remove(db_file)
        print(f"🗑️  Base de datos antigua eliminada.")
    
    # Crear nueva base de datos con la estructura actualizada
    print(f"🔨 Creando nueva base de datos con estructura actualizada...")
    db_controller.init_db()
    db_controller.create_forms_table()
    
    print(f"✅ Base de datos creada exitosamente!")
    print(f"\nEstructura actualizada:")
    print(f"  - Tabla 'users' con campo email UNIQUE NOT NULL")
    print(f"  - Tabla 'students'")
    print(f"  - Tabla 'forms'")
    
    # Mostrar estructura de la tabla users
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    
    print(f"\n📋 Estructura de la tabla 'users':")
    for col in columns:
        print(f"  - {col[1]} ({col[2]}){' NOT NULL' if col[3] else ''}{' UNIQUE' if 'email' in col[1] else ''}")
    
    conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("🔄 Recreación de Base de Datos - AcademicIA")
    print("=" * 60)
    print()
    
    response = input("¿Deseas continuar? Esto eliminará la base de datos actual. (s/n): ")
    
    if response.lower() in ['s', 'si', 'y', 'yes']:
        recreate_database()
    else:
        print("❌ Operación cancelada.")
