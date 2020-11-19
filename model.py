from dataclasses import dataclass

@dataclass
class Trace:
    id: str
    hop: int
    ip: str
