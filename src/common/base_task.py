from abc import ABC, abstractmethod
import numpy as np

class BaseTask(ABC):
    """AeroMind Görev Arayüzü: Tüm tasklar bu sınıftan türetilmelidir."""
    
    @abstractmethod
    def process(self, frame: np.ndarray):
        """Her frame için yapılacak işlemi tanımlar."""
        pass

    @abstractmethod
    def get_output(self) -> dict:
        """İşlem sonucunu standart bir sözlük formatında döndürür."""
        pass