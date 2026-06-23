from dataclasses import dataclass

from model.track import Track


@dataclass
class Arco:
    t1 : Track
    t2 : Track
    peso : int