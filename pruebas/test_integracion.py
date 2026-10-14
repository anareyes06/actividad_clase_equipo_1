import json
import subprocess
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import aplicacion
from calculadora import main

cliente = TestClient(aplicacion)


def test_programa_completo():
    respuesta = subprocess.run(
        [sys.executable, "calculadora.py"],
        input="5\n3\n8\n9\n10\n9\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert "Resultado: 9.0" in respuesta.stdout
    assert "Hasta luego" in respuesta.stdout


def test_estado_api():
    respuesta = cliente.get("/estado")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "correcto"}


def test_calcular_promedio_api():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "promedio", "numeros": [8, 9, 10]},
    )
    assert respuesta.status_code == 200
    assert respuesta.json() == {"resultado": 9}


def test_division_entre_cero_api():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "division", "numeros": [10, 0]},
    )
    assert respuesta.status_code == 400
    assert "cero" in respuesta.json()["detail"]


def test_operacion_invalida_api():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "desconocida", "numeros": [1, 2]},
    )
    assert respuesta.status_code == 400


def test_menu_suma(capsys):
    entradas = ["1", "2", "5", "3", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 8" in salida


def test_menu_varias_operaciones(capsys):
    entradas = ["1", "2", "2", "3", "2", "8", "3", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert salida.count("Resultado: 5") == 2
    assert "Hasta luego" in salida


def test_menu_opcion_invalida(capsys):
    entradas = ["15", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Opción inválida" in salida
    assert "Hasta luego" in salida


def test_menu_division(capsys):
    entradas = ["4", "8", "2", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 4.0" in salida


def test_menu_potencia(capsys):
    entradas = ["6", "2", "3", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 8" in salida


def test_menu_division_entre_cero(capsys):
    entradas = ["4", "2", "0", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "cero" in salida


def test_menu_numeros_decimales(capsys):
    entradas = ["1", "2", "1.5", "2.5", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 4.0" in salida


def test_api_documentacion_y_seguridad():
    respuesta = cliente.post(
        "/calcular",
        json={"operacion": "promedio", "numeros": [8, 9, 10]},
    )

    assert respuesta.status_code == 200
    assert "/calcular" in cliente.get("/openapi.json").json()["paths"]
    assert respuesta.headers["Cross-Origin-Resource-Policy"] == "same-origin"
    assert respuesta.headers["Cache-Control"] == "no-store"


def test_api_con_errores():
    casos = [
        {"operacion": "division", "numeros": [5, 0]},
        {"operacion": "suma", "numeros": [float("inf")]},
        {"operacion": "suma", "numeros": [1] * 1001},
        {},
    ]

    for datos in casos:
        respuesta = cliente.post(
            "/calcular",
            content=json.dumps(datos),
            headers={"Content-Type": "application/json"},
        )

        assert respuesta.status_code == 400
        assert "detail" in respuesta.json()

    assert cliente.post("/calcular", json=[1, 2]).status_code == 422
