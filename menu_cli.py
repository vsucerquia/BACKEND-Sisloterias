"""Menú por consola que realiza CRUD consumiendo la API REST (HTTP).

Debes tener la API en marcha en otra terminal, por ejemplo::

    python main.py

Luego ejecuta::

    python menu_cli.py

La URL de la API puede configurarse en ``.env`` con ``API_BASE_URL`` (por defecto
``http://127.0.0.1:8000``). Este script no accede a la base de datos directamente.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from crud.crud_client import CrudClient

load_dotenv(Path(__file__).resolve().parent / ".env")

# (clave menú, path API, etiqueta)
RECURSOS: list[tuple[str, str, str]] = [
    ("1", "jugadores", "Jugadores"),
    ("2", "juegos", "Juegos"),
    ("3", "sorteos", "Sorteos"),
    ("4", "boletos", "Boletos"),
    ("5", "premios", "Premios"),
    ("6", "pagos", "Pagos"),
]


def _prompt(msg: str) -> str:
    return input(msg).strip()


def _prompt_int(msg: str) -> int:
    raw = _prompt(msg)
    return int(raw)


def _prompt_float(msg: str) -> float:
    raw = _prompt(msg)
    return float(raw)


def _prompt_optional(msg: str) -> str | None:
    raw = _prompt(msg)
    return raw if raw else None


def _print_result(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _parse_dt(text: str) -> datetime:
    """Acepta ISO (2025-03-27T14:30:00) o fecha simple."""
    text = text.strip()
    if "T" not in text and len(text) == 10:
        text = f"{text}T00:00:00"
    return datetime.fromisoformat(text)


def crud_submenu(client: CrudClient, path: str, label: str) -> None:
    """Submenú CRUD para un recurso."""
    while True:
        print(f"\n--- {label} ---")
        print("1. Listar todos")
        print("2. Ver por ID")
        print("3. Crear")
        print("4. Actualizar")
        print("5. Eliminar")
        print("0. Volver")
        op = _prompt("Opción: ")

        if op == "0":
            return
        if op == "1":
            _print_result(client.list_all(path))
        elif op == "2":
            i = _prompt_int("ID: ")
            _print_result(client.get_by_id(path, i))
        elif op == "3":
            payload = _build_create_payload(path)
            if payload is None:
                continue
            _print_result(client.create(path, payload))
        elif op == "4":
            i = _prompt_int("ID a actualizar: ")
            payload = _build_update_payload(path)
            if payload is None:
                continue
            if not payload:
                print("No hay campos para actualizar.")
                continue
            _print_result(client.update(path, i, payload))
        elif op == "5":
            i = _prompt_int("ID a eliminar: ")
            _print_result(client.delete(path, i))
        else:
            print("Opción no válida.")


def _build_create_payload(path: str) -> dict | None:
    try:
        if path == "jugadores":
            return {
                "nombre": _prompt("Nombre: "),
                "email": _prompt("Email: "),
            }
        if path == "juegos":
            return {
                "nombre": _prompt("Nombre del juego: "),
                "tipo": _prompt("Tipo: "),
            }
        if path == "sorteos":
            id_juego = _prompt_int("ID juego: ")
            dt = _parse_dt(
                _prompt("Fecha/hora sorteo (ISO, ej. 2025-03-27T15:00:00): ")
            )
            return {
                "id_juego": id_juego,
                "fecha_sorteo": dt.isoformat(),
                "numero_ganador": _prompt("Número ganador: "),
            }
        if path == "boletos":
            return {
                "id_jugador": _prompt_int("ID jugador: "),
                "id_sorteo": _prompt_int("ID sorteo: "),
                "numero_apostado": _prompt("Número apostado: "),
                "monto_apuesta": _prompt_float("Monto apuesta: "),
            }
        if path == "premios":
            return {
                "id_boleto": _prompt_int("ID boleto: "),
                "monto_premio": _prompt_float("Monto premio: "),
                "estado": _prompt("Estado (ej. pendiente): ") or "pendiente",
            }
        if path == "pagos":
            return {
                "id_premio": _prompt_int("ID premio: "),
                "metodo_pago": _prompt("Método de pago: "),
                "monto_pagado": _prompt_float("Monto pagado: "),
            }
    except (ValueError, OSError) as exc:
        print(f"Dato inválido: {exc}")
        return None
    print(f"Recurso desconocido: {path}")
    return None


def _build_update_payload(path: str) -> dict | None:
    """Solo incluye campos que el usuario rellene (vacío = omitir)."""
    try:
        if path == "jugadores":
            d = {}
            n = _prompt_optional("Nombre (Enter para omitir): ")
            e = _prompt_optional("Email (Enter para omitir): ")
            if n is not None:
                d["nombre"] = n
            if e is not None:
                d["email"] = e
            return d
        if path == "juegos":
            d = {}
            n = _prompt_optional("Nombre (Enter para omitir): ")
            t = _prompt_optional("Tipo (Enter para omitir): ")
            if n is not None:
                d["nombre"] = n
            if t is not None:
                d["tipo"] = t
            return d
        if path == "sorteos":
            d = {}
            raw = _prompt_optional("ID juego (Enter para omitir): ")
            if raw is not None:
                d["id_juego"] = int(raw)
            raw = _prompt_optional(
                "Fecha sorteo ISO (Enter para omitir): "
            )
            if raw is not None:
                d["fecha_sorteo"] = _parse_dt(raw).isoformat()
            ng = _prompt_optional("Número ganador (Enter para omitir): ")
            if ng is not None:
                d["numero_ganador"] = ng
            return d
        if path == "boletos":
            d = {}
            for key, label in (
                ("id_jugador", "ID jugador"),
                ("id_sorteo", "ID sorteo"),
            ):
                raw = _prompt_optional(f"{label} (Enter para omitir): ")
                if raw is not None:
                    d[key] = int(raw)
            na = _prompt_optional("Número apostado (Enter para omitir): ")
            if na is not None:
                d["numero_apostado"] = na
            raw = _prompt_optional("Monto apuesta (Enter para omitir): ")
            if raw is not None:
                d["monto_apuesta"] = float(raw)
            return d
        if path == "premios":
            d = {}
            raw = _prompt_optional("ID boleto (Enter para omitir): ")
            if raw is not None:
                d["id_boleto"] = int(raw)
            raw = _prompt_optional("Monto premio (Enter para omitir): ")
            if raw is not None:
                d["monto_premio"] = float(raw)
            es = _prompt_optional("Estado (Enter para omitir): ")
            if es is not None:
                d["estado"] = es
            return d
        if path == "pagos":
            d = {}
            raw = _prompt_optional("ID premio (Enter para omitir): ")
            if raw is not None:
                d["id_premio"] = int(raw)
            mp = _prompt_optional("Método pago (Enter para omitir): ")
            if mp is not None:
                d["metodo_pago"] = mp
            raw = _prompt_optional("Monto pagado (Enter para omitir): ")
            if raw is not None:
                d["monto_pagado"] = float(raw)
            return d
    except (ValueError, OSError) as exc:
        print(f"Dato inválido: {exc}")
        return None
    print(f"Recurso desconocido: {path}")
    return None


def main() -> None:
    base = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    client = CrudClient(base_url=base)

    print("===== SISTEMA LOTERÍA — menú cliente (API HTTP) =====")
    print(f"Conectando a: {base}")
    print("(Asegúrate de tener la API en ejecución, p. ej. python main.py)\n")

    try:
        r = requests.get(f"{base}/", timeout=5)
        r.raise_for_status()
        print("API respondiendo en la raíz.\n")
    except requests.RequestException:
        print(
            "Advertencia: no se pudo contactar la API. Arranca el servidor "
            "(python main.py) o revisa API_BASE_URL en .env\n"
        )

    while True:
        print("\n--- Entidad ---")
        for key, path, label in RECURSOS:
            print(f"{key}. {label}")
        print("0. Salir")
        choice = _prompt("Opción: ")

        if choice == "0":
            print("Hasta luego.")
            sys.exit(0)

        found = next((x for x in RECURSOS if x[0] == choice), None)
        if not found:
            print("Opción no válida.")
            continue
        _, path, label = found
        crud_submenu(client, path, label)


if __name__ == "__main__":
    main()
