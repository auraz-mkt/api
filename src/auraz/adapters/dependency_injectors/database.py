from auraz.adapters.dependency_injectors.database_in_memory import DatabaseInMemoryDependencyInjector
from auraz.adapters.dependency_injectors.database_relational import DatabaseRelationalDependencyInjector
from auraz.adapters.settings import DatabaseType, Settings
from auraz.ports.dependency_injection.dependency_injector import DependencyInjector
from auraz.ports.dependency_injection.types.database import Repositories


class DatabaseInjector(DependencyInjector[Repositories]):
    def __init__(self, settings: Settings):
        self.injector = self.__create_injector(settings)

    def build(self) -> Repositories:
        return self.injector.build()

    @staticmethod
    def __create_injector(settings: Settings) -> DependencyInjector[Repositories]:
        match settings.db.type:
            case DatabaseType.IN_MEMORY:
                return DatabaseInMemoryDependencyInjector(settings)
            case DatabaseType.RELATIONAL:
                return DatabaseRelationalDependencyInjector(settings)

        raise ValueError(f"Database type is invalid {settings.db.type}")
