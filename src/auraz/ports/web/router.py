from abc import ABC, abstractmethod

from fastapi import APIRouter


class Router(ABC):
    @abstractmethod
    def create(self) -> APIRouter:
        pass
