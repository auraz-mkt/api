from abc import ABC, abstractmethod


class DependencyInjector(ABC):
    @abstractmethod
    def build(self):
        pass
