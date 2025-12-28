"""
Script de Configuración de Ollama
Verifica e instala/configura Ollama para el proyecto
"""
import os
import sys
import subprocess
import requests
import time
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"

def check_ollama_installed():
    """Verifica si Ollama está instalado"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, None
    except FileNotFoundError:
        return False, None
    except Exception as e:
        return False, str(e)

def check_ollama_running():
    """Verifica si Ollama está corriendo"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except requests.exceptions.ConnectionError:
        return False, "No se puede conectar a Ollama. ¿Está corriendo?"
    except Exception as e:
        return False, str(e)

def check_model_available():
    """Verifica si el modelo está disponible"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            return OLLAMA_MODEL in model_names, model_names
        return False, []
    except Exception as e:
        return False, []

def pull_model():
    """Descarga el modelo si no está disponible"""
    print(f"\n📥 Descargando modelo {OLLAMA_MODEL}...")
    print("   Esto puede tomar varios minutos dependiendo de tu conexión...")
    
    try:
        # Usar requests para hacer pull del modelo
        response = requests.post(
            f"{OLLAMA_URL}/api/pull",
            json={"name": OLLAMA_MODEL},
            stream=True,
            timeout=300
        )
        
        if response.status_code == 200:
            print("   ✓ Modelo descargado exitosamente")
            return True
        else:
            print(f"   ❌ Error al descargar modelo: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model():
    """Prueba el modelo con una consulta simple"""
    print(f"\n🧪 Probando modelo {OLLAMA_MODEL}...")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": "Responde solo con 'OK'",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✓ Modelo responde correctamente")
            return True
        else:
            print(f"   ❌ Error al probar modelo: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def setup_ollama():
    """Configura Ollama paso a paso"""
    
    print("=" * 80)
    print("CONFIGURACIÓN DE OLLAMA")
    print("=" * 80)
    
    # 1. Verificar instalación
    print("\n1️⃣ Verificando instalación de Ollama...")
    is_installed, version = check_ollama_installed()
    
    if not is_installed:
        print("   ❌ Ollama NO está instalado")
        print("\n   📥 INSTRUCCIONES DE INSTALACIÓN:")
        print("   " + "-" * 76)
        print("   1. Visita: https://ollama.ai/download")
        print("   2. Descarga Ollama para Windows")
        print("   3. Ejecuta el instalador")
        print("   4. Reinicia tu terminal después de instalar")
        print("   5. Ejecuta este script nuevamente")
        print("\n   O instala desde línea de comandos:")
        print("   - PowerShell (como administrador):")
        print("     winget install Ollama.Ollama")
        return False
    else:
        print(f"   ✓ Ollama está instalado: {version}")
    
    # 2. Verificar que esté corriendo
    print("\n2️⃣ Verificando que Ollama esté corriendo...")
    is_running, response_data = check_ollama_running()
    
    if not is_running:
        print(f"   ❌ Ollama NO está corriendo")
        print(f"   Error: {response_data}")
        print("\n   💡 SOLUCIÓN:")
        print("   1. Abre Ollama desde el menú de inicio")
        print("   2. O ejecuta en PowerShell: ollama serve")
        print("   3. Espera a que aparezca 'Listening on...'")
        print("   4. Ejecuta este script nuevamente")
        return False
    else:
        print(f"   ✓ Ollama está corriendo en {OLLAMA_URL}")
        if response_data and 'models' in response_data:
            print(f"   Modelos disponibles: {len(response_data['models'])}")
    
    # 3. Verificar modelo
    print(f"\n3️⃣ Verificando modelo {OLLAMA_MODEL}...")
    model_available, available_models = check_model_available()
    
    if not model_available:
        print(f"   ❌ Modelo {OLLAMA_MODEL} NO está disponible")
        if available_models:
            print(f"   Modelos disponibles: {', '.join(available_models)}")
        
        print(f"\n   📥 ¿Descargar modelo {OLLAMA_MODEL}? (s/n): ", end="")
        try:
            respuesta = input().strip().lower()
            if respuesta == 's' or respuesta == 'y' or respuesta == 'si':
                if pull_model():
                    model_available = True
                else:
                    print("\n   ⚠ Intenta descargar manualmente:")
                    print(f"   ollama pull {OLLAMA_MODEL}")
                    return False
            else:
                print("   ⚠ Saltando descarga. El modelo debe estar disponible para usar Ollama.")
                return False
        except KeyboardInterrupt:
            print("\n   ⚠ Cancelado por el usuario")
            return False
    else:
        print(f"   ✓ Modelo {OLLAMA_MODEL} está disponible")
    
    # 4. Probar modelo
    print("\n4️⃣ Probando modelo...")
    if test_model():
        print("   ✓ Modelo funciona correctamente")
    else:
        print("   ⚠ El modelo está disponible pero no responde correctamente")
        print("   Intenta reiniciar Ollama")
        return False
    
    # 5. Verificar configuración en .env
    print("\n5️⃣ Verificando configuración en .env...")
    env_file = Path(".env")
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        needs_update = False
        if "LLM_PROVIDER=ollama" not in content and "LLM_PROVIDER=openai" in content:
            content = content.replace("LLM_PROVIDER=openai", "LLM_PROVIDER=ollama")
            needs_update = True
        elif "LLM_PROVIDER" not in content:
            content += f"\nLLM_PROVIDER=ollama\n"
            needs_update = True
        
        if "OLLAMA_URL" not in content:
            content += f"OLLAMA_URL={OLLAMA_URL}/api/generate\n"
            needs_update = True
        
        if "OLLAMA_MODEL" not in content:
            content += f"OLLAMA_MODEL={OLLAMA_MODEL}\n"
            needs_update = True
        
        if needs_update:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("   ✓ Archivo .env actualizado")
        else:
            print("   ✓ Archivo .env ya está configurado correctamente")
    else:
        print("   ⚠ Archivo .env no existe, creando uno nuevo...")
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"LLM_PROVIDER=ollama\n")
            f.write(f"OLLAMA_URL={OLLAMA_URL}/api/generate\n")
            f.write(f"OLLAMA_MODEL={OLLAMA_MODEL}\n")
        print("   ✓ Archivo .env creado")
    
    # 6. Verificación final
    print("\n" + "=" * 80)
    print("VERIFICACIÓN FINAL")
    print("=" * 80)
    
    print("\n✅ CONFIGURACIÓN COMPLETA")
    print(f"   - Ollama instalado: ✓")
    print(f"   - Ollama corriendo: ✓")
    print(f"   - Modelo disponible: ✓ ({OLLAMA_MODEL})")
    print(f"   - Configuración .env: ✓")
    
    print("\n📋 Configuración actual:")
    print(f"   LLM_PROVIDER=ollama")
    print(f"   OLLAMA_URL={OLLAMA_URL}/api/generate")
    print(f"   OLLAMA_MODEL={OLLAMA_MODEL}")
    
    print("\n💡 Próximos pasos:")
    print("   1. Ejecuta: python check_llm_provider.py")
    print("   2. Debería mostrar: ✅ PROVEEDOR ACTIVO: Ollama")
    print("   3. Prueba el agente: python main.py https://competitor.com")
    
    print("\n" + "=" * 80)
    
    return True

if __name__ == "__main__":
    try:
        success = setup_ollama()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

