from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def insert() -> None:
        pass

    @abstractmethod
    def find() -> None:
        pass

    @abstractmethod
    def update() -> None:
        pass

    @abstractmethod
    def delete() -> None:
        pass