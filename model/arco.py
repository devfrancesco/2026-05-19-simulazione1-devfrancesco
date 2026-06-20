from dataclasses import dataclass

from model.employee import Employee


@dataclass
class Arco:
    e1 : Employee
    e2 : Employee
    peso : float