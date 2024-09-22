from .argentina_strategy import ArgentinaFiscalStrategy
from .españa_strategy import EspañaFiscalStrategy  # Si tienes más países
from .strategy import ObligacionesFiscalesStrategy

class FiscalStrategyFactory:
    """Fábrica para obtener la estrategia fiscal según el país del usuario."""

    @staticmethod
    def get_strategy(usuario) -> ObligacionesFiscalesStrategy:
        pais = usuario.pais_residencia.lower()

        if pais == 'argentina':
            return ArgentinaFiscalStrategy(usuario)
        elif pais == 'españa':
            return EspañaFiscalStrategy(usuario)
        # Agregar más países aquí según sea necesario
        else:
            raise ValueError(f"No hay estrategia fiscal definida para el país: {pais}")