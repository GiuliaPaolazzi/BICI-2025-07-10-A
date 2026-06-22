
from dataclasses import dataclass

from model.prodotto import Prodotto


@dataclass
class Arco:
    p1: Prodotto
    p2: Prodotto
    peso: int

