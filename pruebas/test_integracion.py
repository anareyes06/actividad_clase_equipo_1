from unittest.mock import patch

from fastapi.testclient import TestClient

from api import aplicacion
from calculadora import main

cliente = TestClient(aplicacion)


# Comprueba que la API está funcionando.
def test_estado_api():
    respuesta = cliente.get("/estado")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "correcto"}


# Comprueba que la API reutiliza la calculadora.
def test_calcular_promedio_api():
    datos = {
        "operacion": "promedio",
        "numeros": [8, 9, 10],
    }
    respuesta = cliente.post("/calcular", json=datos)

    assert respuesta.status_code == 200
    assert respuesta.json() == {"resultado": 9}


# Comprueba el manejo de división entre cero.
def test_division_entre_cero_api():
    datos = {
        "operacion": "division",
        "numeros": [10, 0],
    }
    respuesta = cliente.post("/calcular", json=datos)

    assert respuesta.status_code == 400
    assert "cero" in respuesta.json()["detail"]


# Comprueba una operación no válida.
def test_operacion_invalida_api():
    datos = {
        "operacion": "desconocida",
        "numeros": [1, 2],
    }
    respuesta = cliente.post("/calcular", json=datos)

    assert respuesta.status_code == 400


# Comprueba que el menú recibe datos y muestra el resultado.
def test_menu_suma(capsys):
    entradas = ["1", "2", "5", "3", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 8" in salida


# Comprueba que se puede continuar y después salir.
def test_menu_varias_operaciones(capsys):
    entradas = ["1", "2", "2", "3", "2", "8", "3", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Resultado: 5" in salida
    assert "Resultado: 5" in salida
    assert "Hasta luego" in salida


# Comprueba que una opción incorrecta no cierra el programa.
def test_menu_opcion_invalida(capsys):
    entradas = ["15", "9"]

    with patch("builtins.input", side_effect=entradas):
        main()

    salida = capsys.readouterr().out
    assert "Opción inválida" in salida
    assert "Hasta luego" in salida
