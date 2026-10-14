import pytest

from calculadora import Calculadora

# Pruebas de las operaciones matemáticas


def test_suma():
    assert Calculadora("1", [2, 3]).resultado() == 5


def test_suma_con_decimales_y_negativos():
    # Prueba propia con datos diferentes a los ejemplos.
    assert Calculadora("1", [1.5, 2, -1]).resultado() == pytest.approx(2.5)


def test_resta():
    assert Calculadora("2", [3, 8]).resultado() == -5


def test_multiplicacion():
    assert Calculadora("3", [2, 3, 0.5]).resultado() == 3


def test_division():
    assert Calculadora("4", [9, 2]).resultado() == pytest.approx(4.5)


def test_promedio():
    assert Calculadora("5", [8, 9, 10]).resultado() == 9


def test_promedio_con_decimales():
    assert Calculadora("5", [7.5, 8.5, 9.5]).resultado() == pytest.approx(8.5)


def test_potencia():
    assert Calculadora("6", [2, 3]).resultado() == 8


def test_mayor():
    assert Calculadora("7", [4, -2, 8]).resultado() == 8


def test_menor():
    assert Calculadora("8", [4, -2, 8]).resultado() == -2


# Pruebas de manejo de errores


def test_division_entre_cero():
    with pytest.raises(ValueError, match="cero"):
        Calculadora("4", [5, 0]).resultado()


def test_operacion_invalida():
    with pytest.raises(ValueError):
        Calculadora("10", [1, 2]).resultado()


def test_promedio_sin_numeros():
    with pytest.raises(ValueError):
        Calculadora("5", []).resultado()


def test_suma_con_dato_invalido():
    with pytest.raises(ValueError):
        Calculadora("1", ["hola", 2]).resultado()


def test_potencia_resultado_complejo():
    with pytest.raises(ValueError):
        Calculadora("6", [-2, 0.5]).resultado()


def test_suma_resultado_infinito():
    with pytest.raises(ValueError):
        Calculadora("1", [1e308, 1e308]).resultado()
