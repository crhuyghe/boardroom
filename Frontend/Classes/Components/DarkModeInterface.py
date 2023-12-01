from abc import ABC, abstractmethod

class DarkMode(ABC):
    @abstractmethod
    def swap_mode(self):
        pass
