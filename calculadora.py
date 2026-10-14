import math


class Calculadora:
    def __init__(self, operacion, numeros):
        # Se validan los datos antes de realizar cualquier cálculo.
        operaciones_validas = {str(i) for i in range(1, 9)}

        if operacion not in operaciones_validas:
            raise ValueError("La operación seleccionada no es válida.")

        if not isinstance(numeros, (list, tuple)) or not numeros:
            raise ValueError("Debes ingresar al menos un número.")

        if operacion in {"2", "4", "6"} and len(numeros) != 2:
            raise ValueError("Esta operación requiere exactamente dos números.")

        for numero in numeros:
            if (
                isinstance(numero, bool)
                or not isinstance(numero, (int, float))
                or not math.isfinite(numero)
            ):
                raise ValueError("Todos los valores deben ser números válidos.")

        self.operacion = operacion
        # Se guarda una copia para evitar modificaciones externas.
        self.numeros = list(numeros)

    def suma(self):
        return sum(self.numeros)

    def resta(self):
        return self.numeros[0] - self.numeros[1]

    def multiplicacion(self):
        producto = 1
        for numero in self.numeros:
            producto *= numero
        return producto

    def division(self):
        if self.numeros[1] == 0:
            raise ValueError("No se puede dividir entre cero.")
        return self.numeros[0] / self.numeros[1]

    def promedio(self):
        return self.suma() / len(self.numeros)

    def potencia(self):
        return self.numeros[0] ** self.numeros[1]

    def mayor(self):
        return max(self.numeros)

    def menor(self):
        return min(self.numeros)

    def resultado(self):
        # Cada opción del menú se relaciona con su método.
        operaciones = {
            "1": self.suma,
            "2": self.resta,
            "3": self.multiplicacion,
            "4": self.division,
            "5": self.promedio,
            "6": self.potencia,
            "7": self.mayor,
            "8": self.menor,
        }

        respuesta = operaciones[self.operacion]()

        # Evita devolver resultados complejos o infinitos.
        if isinstance(respuesta, complex) or not math.isfinite(respuesta):
            raise ValueError("El resultado matemático no es válido.")

        return respuesta


def pedir_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Valor inválido. Ingresa un número válido, por ejemplo 8 o 8.5.")


def pedir_cantidad():
    while True:
        try:
            cantidad = int(input("Cantidad de números: "))
            if cantidad >= 1:
                return cantidad
            print("Debes ingresar al menos un número.")
        except ValueError:
            print("Ingresa una cantidad entera válida.")


def main():
    while True:
        print("\n--- CALCULADORA ---")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")
        print("5. Promedio")
        print("6. Potencia")
        print("7. Número mayor")
        print("8. Número menor")
        print("9. Salir")

        operacion = input("Elige una operación (1-9): ").strip()
        if operacion == "9":
            print("¡Hasta luego!")
            break
        if operacion not in {str(i) for i in range(1, 9)}:
            print("Opción inválida. Elige un número del 1 al 9.")
            continue

        if operacion in {"2", "4", "6"}:
            print("Se calculará: primero menos/entre/elevado al segundo, según la operación.")
            numeros = [pedir_numero("Primer número: "), pedir_numero("Segundo número: ")]
        else:
            cantidad = pedir_cantidad()
            numeros = [pedir_numero(f"Número {i}: ") for i in range(1, cantidad + 1)]

        objeto = Calculadora(operacion, numeros)
        try:
            respuesta = objeto.resultado()
            print(f"Resultado: {respuesta}")
        except (ValueError, OverflowError, ZeroDivisionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
