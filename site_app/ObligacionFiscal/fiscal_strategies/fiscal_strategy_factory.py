from .argentina_strategy import (
    ArgentinaFiscalStrategy,
)  # Importa la estrategia fiscal para Argentina
from .españa_strategy import (
    EspañaFiscalStrategy,
)  # Importa la estrategia fiscal para España
from .strategy import (
    ObligacionesFiscalesStrategy,
)  # Importa la clase base de estrategias fiscales


class FiscalStrategyFactory:
    """Fábrica para obtener la estrategia fiscal según el país del usuario."""

    @staticmethod
    def get_strategy(usuario) -> ObligacionesFiscalesStrategy:
        """
        Devuelve la estrategia fiscal correspondiente según el país de residencia del usuario.

        Parámetros:
        - usuario: objeto que contiene la información del usuario, incluyendo su país de residencia.

        Retorna:
        - Una instancia de una estrategia fiscal específica (ArgentinaFiscalStrategy, EspañaFiscalStrategy, etc.).
        """

        # Mapeo de códigos de país a nombres completos
        pais_mapping = {
            "ar": "argentina",
            "es": "españa",
            # Agrega más códigos y nombres según sea necesario
        }

        # Obtiene el país de residencia del usuario y lo convierte a minúsculas
        pais = usuario.pais_residencia.lower()

        # Si el país es un código, lo convierte al nombre completo
        pais = pais_mapping.get(pais, pais)  # Convierte el código al nombre completo

        # Selecciona la estrategia fiscal según el país
        if pais == "argentina":
            return ArgentinaFiscalStrategy(
                usuario
            )  # Retorna la estrategia fiscal para Argentina
        elif pais == "españa":
            return EspañaFiscalStrategy(
                usuario
            )  # Retorna la estrategia fiscal para España
        # Se pueden agregar más países y sus estrategias aquí
        else:
            # Si no hay estrategia definida para el país, lanza una excepción
            raise ValueError(f"No hay estrategia fiscal definida para el país: {pais}")
