"""
Generador de correos y contraseñas temporales
------------------------------------------------
Crea una cuenta de correo desechable usando la API pública de mail.tm
(no requiere API key) y genera una contraseña segura de forma automática.

Uso:
    python main.py
"""

import secrets
import string
import sys
import time
import requests

API_BASE = "https://api.mail.tm"


def generar_password(longitud: int = 16) -> str:
    """Genera una contraseña aleatoria segura."""
    alfabeto = string.ascii_letters + string.digits + "!@#$%^&*_-"
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))


def obtener_dominio() -> str:
    """Obtiene un dominio disponible desde mail.tm."""
    resp = requests.get(f"{API_BASE}/domains", timeout=10)
    resp.raise_for_status()
    datos = resp.json()
    dominios = datos.get("hydra:member") or datos.get("member") or []
    if not dominios:
        raise RuntimeError("No hay dominios disponibles en este momento.")
    return dominios[0]["domain"]


def generar_usuario(longitud: int = 10) -> str:
    """Genera un nombre de usuario aleatorio para el correo."""
    letras = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(letras) for _ in range(longitud))


def crear_cuenta_temporal():
    """Crea la cuenta y devuelve (correo, password, token)."""
    dominio = obtener_dominio()
    usuario = generar_usuario()
    password = generar_password()
    correo = f"{usuario}@{dominio}"

    payload = {"address": correo, "password": password}
    resp = requests.post(f"{API_BASE}/accounts", json=payload, timeout=10)

    if resp.status_code not in (200, 201):
        raise RuntimeError(f"No se pudo crear la cuenta: {resp.status_code} {resp.text}")

    # Obtener token de autenticación
    resp_token = requests.post(f"{API_BASE}/token", json=payload, timeout=10)
    resp_token.raise_for_status()
    token = resp_token.json()["token"]

    return correo, password, token


def revisar_bandeja(token: str):
    """Consulta los mensajes recibidos en la cuenta temporal."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_BASE}/messages", headers=headers, timeout=10)
    resp.raise_for_status()
    datos = resp.json()
    mensajes = datos.get("hydra:member") or datos.get("member") or []

    if not mensajes:
        print("  (Sin mensajes por ahora)")
        return

    for m in mensajes:
        remitente = m.get("from", {}).get("address", "desconocido")
        asunto = m.get("subject", "(sin asunto)")
        fecha = m.get("createdAt", "")
        print(f"  - De: {remitente} | Asunto: {asunto} | Fecha: {fecha}")


def main():
    print("=== Generador de correo y contraseña temporal ===\n")

    try:
        correo, password, token = crear_cuenta_temporal()
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Cuenta creada con éxito:\n")
    print(f"  Correo:      {correo}")
    print(f"  Contraseña:  {password}\n")

    while True:
        opcion = input(
            "Elige una opción:\n"
            "  [1] Revisar bandeja de entrada\n"
            "  [2] Generar otra cuenta\n"
            "  [3] Salir\n> "
        ).strip()

        if opcion == "1":
            print("\nRevisando bandeja de entrada...")
            try:
                revisar_bandeja(token)
            except requests.exceptions.RequestException as e:
                print(f"Error al consultar mensajes: {e}")
            print()
        elif opcion == "2":
            main()
            return
        elif opcion == "3":
            print("¡Listo! Recuerda que esta cuenta es temporal.")
            break
        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    main()
