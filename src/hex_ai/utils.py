"""
Utilidades auxiliares: puentes, vecinos compartidos, etc.
"""
from .board import DIRECCIONES


def shared_neighbors(pos1, pos2, size):
    """
    Devuelve las celdas que son vecinas comunes de pos1 y pos2.
    Útil para detectar puentes en HEX.
    """
    r1, c1 = pos1
    r2, c2 = pos2
    n1 = set()
    n2 = set()
    for dr, dc in DIRECCIONES:
        nr, nc = r1 + dr, c1 + dc
        if 0 <= nr < size and 0 <= nc < size:
            n1.add((nr, nc))
        nr, nc = r2 + dr, c2 + dc
        if 0 <= nr < size and 0 <= nc < size:
            n2.add((nr, nc))
    return n1 & n2


def is_bridge(pos1, pos2):
    """
    Dos celdas forman un puente si están a distancia (2,1) o (1,2) en coordenadas offset.
    """
    r1, c1 = pos1
    r2, c2 = pos2
    dr, dc = abs(r1 - r2), abs(c1 - c2)
    return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)