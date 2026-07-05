from abc import ABC, abstractmethod


class MusicProvider(ABC):

    @abstractmethod
    async def search(self, artist: str, title: str):
        pass

    @abstractmethod
    async def download(self, candidate, output_path: str):
        pass

    @abstractmethod
    async def metadata(self, candidate):
        pass