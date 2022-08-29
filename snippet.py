from dataclasses import dataclass

@dataclass(slots=True)
class Snippet:

    language: str
    folder: str
    snippet: tuple

    