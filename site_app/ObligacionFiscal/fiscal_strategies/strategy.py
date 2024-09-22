from abc import ABC, abstractmethod

class ObligacionesFiscalesStrategy(ABC):
    """
    Interfaz para definir la estrategia fiscal de cada país.
    Cada país debe implementar esta interfaz y proporcionar su propia lógica fiscal.
    """

    @abstractmethod
    def calcular_obligaciones(self):
        pass