"""Dias habiles en Colombia (festivos fijos, Ley 51 de 1983 y los de Semana Santa)."""
from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache


def _pascua(anio: int) -> date:
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    mes = (h + l - 7 * m + 90) // 25
    dia = (h + l - 7 * m + 33 * mes + 19) % 32
    return date(anio, mes, dia)


def _al_lunes(d: date) -> date:
    return d + timedelta(days=(7 - d.weekday()) % 7)


@lru_cache(maxsize=None)
def festivos(anio: int) -> frozenset[date]:
    fijos = [(1, 1), (5, 1), (7, 20), (8, 7), (12, 8), (12, 25)]
    trasladables = [(1, 6), (3, 19), (6, 29), (8, 15), (10, 12), (11, 1), (11, 11)]
    p = _pascua(anio)
    dias = {date(anio, m, d) for m, d in fijos}
    dias |= {_al_lunes(date(anio, m, d)) for m, d in trasladables}
    dias |= {p - timedelta(days=3), p - timedelta(days=2)}  # jueves y viernes santo
    dias |= {p + timedelta(days=n) for n in (43, 64, 71)}  # Ascension, Corpus, Sagrado Corazon
    return frozenset(dias)


def es_habil(d: date) -> bool:
    return d.weekday() < 5 and d not in festivos(d.year)


def dias_habiles_entre(inicio: date, fin: date) -> int:
    """Dias habiles transcurridos despues de `inicio` y hasta `fin` inclusive."""
    n, d = 0, inicio
    while d < fin:
        d += timedelta(days=1)
        if es_habil(d):
            n += 1
    return n


def sumar_anios(d: date, anios: int) -> date:
    try:
        return d.replace(year=d.year + anios)
    except ValueError:  # 29 de febrero
        return d.replace(year=d.year + anios, day=28)
