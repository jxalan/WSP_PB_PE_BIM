#! python3
# -*- coding: utf-8 -*-
"""
Structural QC (WSP BIM Peru)
QA/QC rápido para muros/columnas estructurales.

Motor: CPython 3 (hashbang) [2](https://docs.pyrevitlabs.io/reference/pyrevit/extensions/)
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

# Local imports from lib (these modules are kept free of side-effects)
# These are resolved at runtime within pyRevit; IDE path resolution may warn here.
try:
    from wsp_utils import (  # type: ignore[import]
        get_structural_walls,
        get_structural_columns,
        is_text_param_not_empty,
        is_level_assigned,
        build_issue,
    )

    from wpf_dialog import show_structuralqc_dialog  # type: ignore[import]
except ImportError:
    # IDE import check; modules available at runtime in pyRevit
    get_structural_walls = None  # type: ignore[assignment]
    get_structural_columns = None  # type: ignore[assignment]
    is_text_param_not_empty = None  # type: ignore[assignment]
    is_level_assigned = None  # type: ignore[assignment]
    build_issue = None  # type: ignore[assignment]
    show_structuralqc_dialog = None  # type: ignore[assignment]


def _describe_elem(elem: Any) -> str:
    cat = elem.Category.Name if elem.Category else "N/A"
    name = getattr(elem, "Name", "") or ""
    return "{} | {} | {}".format(elem.Id.IntegerValue, cat, name)


def run() -> None:
    # Import pyRevit/Revit wrappers lazily to avoid side-effects at module import
    # These are only available at runtime within pyRevit/Revit environment
    try:
        from pyrevit import DB, UI, script, revit  # type: ignore[import]
    except Exception as exc:  # pragma: no cover - runtime environment
        raise RuntimeError("pyRevit environment not available: {}".format(exc))

    # Try DocumentManager if available (Dynamo/other hosts), otherwise use revit.doc
    try:
        from RevitServices.Persistence import DocumentManager  # type: ignore
        doc = DocumentManager.Instance.CurrentDBDocument
    except Exception:
        doc = revit.doc

    if not doc:
        UI.TaskDialog.Show("Structural QC", "No hay documento activo.")
        return None

    OUTPUT = script.get_output()

    cfg = show_structuralqc_dialog()
    if cfg is None:
        # Cancelado
        return None

    # 1) Recojo elementos según selección
    elements = []

    if cfg.check_walls:
        elements.extend(get_structural_walls(doc))

    if cfg.check_columns:
        elements.extend(get_structural_columns(doc))

    # 2) Ejecutar checks
    issues = []
    counters = defaultdict(int)

    for e in elements:
        if cfg.check_comments:
            ok = is_text_param_not_empty(e, "Comments")  # requerido: LookupParameter("Comments")
            if not ok:
                issues.append(build_issue(e, "Comments vacío o inexistente"))
                counters["fail_comments"] += 1

        if cfg.check_level:
            ok = is_level_assigned(e)
            if not ok:
                issues.append(build_issue(e, "Level no asignado / inválido"))
                counters["fail_level"] += 1

    # 3) Output por consola pyRevit
    OUTPUT.print_md("# Structural QC – Resultados")
    OUTPUT.print_md("**Elementos revisados:** {}".format(len(elements)))
    OUTPUT.print_md("**Incidencias:** {}".format(len(issues)))
    OUTPUT.print_md("---")

    if issues:
        for it in issues:
            # linkify hace clickable el id (muy útil en consola)
            eid = int(it["id"])
            OUTPUT.print_md(
                "- {} | **{}** | {} | ❌ {}".format(
                    OUTPUT.linkify(DB.ElementId(eid)),
                    it["category"],
                    it["name"],
                    it["issue"],
                )
            )
    else:
        OUTPUT.print_md("✅ No se encontraron incidencias con los checks seleccionados.")

    # 4) TaskDialog resumen
    msg = (
        f"Resumen Structural QC\n\n"
        f"Elementos revisados: {len(elements)}\n"
        f"Fallas por Comments: {counters['fail_comments']}\n"
        f"Fallas por Level: {counters['fail_level']}\n"
        f"Incidencias totales: {len(issues)}\n"
    )
    UI.TaskDialog.Show("Structural QC – WSP BIM Peru", msg)
    return None


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:  # pragma: no cover - runtime error reporting
        # Try to show a friendly dialog/console output when running inside pyRevit
        try:
            from pyrevit import script, UI  # type: ignore[import]

            OUT = script.get_output()
            OUT.print_md("**Structural QC - Error:** {}".format(exc))
            UI.TaskDialog.Show("Structural QC - Error", str(exc))
        except Exception:
            # Fallback to printing
            print("Structural QC - Error:", exc)
        raise
