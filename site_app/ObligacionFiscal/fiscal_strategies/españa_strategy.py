from .strategy import ObligacionesFiscalesStrategy

class EspañaFiscalStrategy(ObligacionesFiscalesStrategy):
    """Estrategia para las obligaciones fiscales en Brasil."""

    def __init__(self, usuario):
        self.usuario = usuario

    def calcular_obligaciones(self):
        # Implementar lógica fiscal para españa
        pass