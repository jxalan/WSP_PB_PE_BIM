# -*- coding: utf-8 -*-
"""
wsp_utils.py
Utilidades reusables para scripts pyRevit (WSP Perú).

Principios:
- Funciones pequeñas, testeables, robustas ante parámetros faltantes.
- No asume idioma excepto donde Revit 2024 está en inglés (p.ej. "Comments").
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Optional

from pyrevit import DB


def get_structural_walls(doc: DB.Document) -> List[DB.Element]:
    """
    Retorna muros marcados como estructurales.
    Estrategia:
      1) Filtra categoría OST_Walls
      2) Valida flag BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT (si existe)
    """
    walls = (
        DB.FilteredElementCollector(doc)
        .OfCategory(DB.BuiltInCategory.OST_Walls)
        .WhereElementIsNotElementType()
        .ToElements()
    )

    structural_walls = []
    for w in walls:
        try:
            p = w.get_Parameter(DB.BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT)
            if p and p.AsInteger() == 1:
                structural_walls.append(w)
        except Exception:
            # Si por alguna razón el parámetro no existe, no lo consideramos estructural
            continue

    return structural_walls


def get_structural_columns(doc: DB.Document) -> List[DB.Element]:
    """Retorna columnas estructurales (Instances) por categoría OST_StructuralColumns."""
    cols = (
        DB.FilteredElementCollector(doc)
        .OfCategory(DB.BuiltInCategory.OST_StructuralColumns)
        .WhereElementIsNotElementType()
        .ToElements()
    )
    return list(cols)


def get_text_param_value(elem: DB.Element, param_name: str) -> Optional"""
    Lee un parámetro de texto por nombre (LookupParameter).
    Retorna string o None si no existe/no es string.
    """
    p = elem.LookupParameter(param_name)
    if not p:
        return None
    try:
        return p.AsString()
    except Exception:
        return None


def is_text_param_not_empty(elem: DB.Element, param_name: str) -> bool:
    """True si el parámetro existe y su valor (trim) no está vacío."""
    val = get_text_param_value(elem, param_name)
    if val is None:
        return False
    return bool(val.strip())


def get_level_id(elem: DB.Element) -> Optional[DB.ElementId]:
    """
    Intenta obtener el LevelId de manera robusta.
    - Primero: propiedad LevelId si existe
    - Fallback: BuiltInParameter.LEVEL_PARAM (cuando aplica)
    """
    # 1) Propiedad LevelId
    if hasattr(elem, "LevelId"):
        try:
            lid = elem.LevelId
            if lid and lid != DB.ElementId.InvalidElementId:
                return lid
        except Exception:
            pass

    # 2) Fallback: parámetro LEVEL_PARAM
    try:
        p = elem.get_Parameter(DB.BuiltInParameter.LEVEL_PARAM)
        if p:
            lid = p.AsElementId()
            if lid and lid != DB.ElementId.InvalidElementId:
                return lid
    except Exception:
        pass

    return None


def is_level_assigned(elem: DB.Element) -> bool:
    """True si el elemento tiene LevelId válido."""
    return get_level_id(elem) is not None


def build_issue(elem: DB.Element, issue: str) -> Dict[str, str]:
    """
    Estructura estándar de hallazgo.
    """
    cat = elem.Category.Name if elem.Category else "N/A"
    name = getattr(elem, "Name", "") or ""
    return {
        "id": str(elem.Id.IntegerValue),
        "category": cat,
        "name": name,
        "issue": issue,
    }