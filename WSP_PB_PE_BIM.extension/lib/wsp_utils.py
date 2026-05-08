# -*- coding: utf-8 -*-
"""
wsp_utils.py
Utilidades reusables para scripts pyRevit (WSP Perú).

Principios:
- Funciones pequeñas, testeables, robustas ante parámetros faltantes.
- No asume idioma excepto donde Revit 2024 está en inglés (p.ej. "Comments").
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Optional, Any


def _get_db_module():
    """Lazily import Revit DB module.

    Prefer Autodesk.Revit.DB to avoid pyRevit wrapper side-effects at import time.
    """
    try:
        import Autodesk.Revit.DB as DB  # type: ignore
        return DB
    except Exception:
        try:
            from pyrevit import DB  # type: ignore
            return DB
        except Exception:
            raise RuntimeError("Revit DB module not available. This function must run inside Revit or pyRevit.")


def get_structural_walls(doc: Any) -> List[Any]:
    """
    Retorna muros marcados como estructurales.
    Estrategia:
      1) Filtra categoría OST_Walls
      2) Valida flag BuiltInParameter.WALL_STRUCTURAL_SIGNIFICANT (si existe)
    """
    DB = _get_db_module()
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


def get_structural_columns(doc: Any) -> List[Any]:
    """Retorna columnas estructurales (Instances) por categoría OST_StructuralColumns."""
    DB = _get_db_module()
    cols = (
        DB.FilteredElementCollector(doc)
        .OfCategory(DB.BuiltInCategory.OST_StructuralColumns)
        .WhereElementIsNotElementType()
        .ToElements()
    )
    return list(cols)


def get_text_param_value(elem: Any, param_name: str) -> Optional[str]:
    """
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


def is_text_param_not_empty(elem: Any, param_name: str) -> bool:  # type: ignore[name-defined]
    """True si el parámetro existe y su valor (trim) no está vacío."""
    val = get_text_param_value(elem, param_name)
    if val is None:
        return False
    return bool(val.strip())


def get_level_id(elem: Any) -> Optional[Any]:
    """
    Intenta obtener el LevelId de manera robusta.
    - Primero: propiedad LevelId si existe
    - Fallback: BuiltInParameter.LEVEL_PARAM (cuando aplica)
    """
    # 1) Propiedad LevelId
    if hasattr(elem, "LevelId"):
        try:
            lid = elem.LevelId
            DB = _get_db_module()
            if lid and lid != DB.ElementId.InvalidElementId:
                return lid
        except Exception:
            pass

    # 2) Fallback: parámetro LEVEL_PARAM
    try:
        DB = _get_db_module()
        p = elem.get_Parameter(DB.BuiltInParameter.LEVEL_PARAM)
        if p:
            lid = p.AsElementId()
            if lid and lid != DB.ElementId.InvalidElementId:
                return lid
    except Exception:
        pass

    return None


def is_level_assigned(elem: Any) -> bool:
    """True si el elemento tiene LevelId válido."""
    return get_level_id(elem) is not None


def build_issue(elem: Any, issue: str) -> Dict[str, str]:
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