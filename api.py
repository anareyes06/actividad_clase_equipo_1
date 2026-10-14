from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from calculadora import Calculadora

# Se desactiva la documentación interactiva para reducir
# las rutas expuestas durante el análisis de seguridad.
aplicacion = FastAPI(
    title="Calculadora",
    docs_url=None,
    redoc_url=None,
)


@aplicacion.exception_handler(RequestValidationError)
async def entrada_invalida(peticion, error):
    return JSONResponse(
        status_code=422,
        content={"error": "Envía una operación y sus números."},
    )


@aplicacion.middleware("http")
async def agregar_cabeceras(peticion, siguiente):
    respuesta = await siguiente(peticion)

    # Cabeceras de seguridad para las respuestas HTTP.
    respuesta.headers.update(
        {
            "Content-Security-Policy": (
                "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
            ),
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Cross-Origin-Resource-Policy": "same-origin",
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
        }
    )

    return respuesta


@aplicacion.get("/estado")
def estado():
    return {"estado": "correcto"}


@aplicacion.post("/calcular")
def calcular(datos: dict):
    # Traduce los nombres de operaciones a nuestro menú numérico.
    operaciones = {
        "suma": "1",
        "resta": "2",
        "multiplicacion": "3",
        "division": "4",
        "promedio": "5",
        "potencia": "6",
        "mayor": "7",
        "menor": "8",
    }

    try:
        numeros = datos.get("numeros", [])

        # Evita procesar listas excesivamente grandes.
        if isinstance(numeros, list) and len(numeros) > 1000:
            raise ValueError("Usa como máximo 1000 números.")

        operacion = datos.get("operacion")
        operacion = operaciones.get(operacion, operacion)

        calculadora = Calculadora(operacion, numeros)
        resultado = calculadora.resultado()

        return {"resultado": resultado}

    except (ValueError, OverflowError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
