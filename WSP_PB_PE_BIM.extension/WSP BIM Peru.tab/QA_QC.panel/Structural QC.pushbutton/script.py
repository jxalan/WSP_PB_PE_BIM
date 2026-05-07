#! python3
# -*- coding: utf-8 -*-
"""
Structural QC (WSP BIM Peru)
QA/QC rápido para muros/columnas estructurales.

Motor: CPython 3 (hashbang) [2](https://docs.pyrevitlabs.io/reference/pyrevit/extensions/)
"""

from __future__ import annotations

from collections import defaultdict

from pyrevit import DB, UI
from pyrevit import script, revit

# Intento "RevitServices" (si existe en tu entorno). En pyRevit puro normalmente NO es necesario.
try:
    from RevitServices.Persistence import DocumentManager  # type: ignore
    DOC = DocumentManager.Instance.CurrentDBDocument
except Exception:
    DOC = revit.doc  # pyRevit wrapper estándar


# Import local (lib)
# En pyRevit, la carpeta /lib de la extensión es un lugar típico para módulos compartidos. [4](https://pyrevitlabs.notion.site/pyRevit-Bundles-12323e3090904d9aa7cdc3d82095d3e3)
from wsp_utils import (
    get_structural_walls,
    get_structural_columns,
    is_text_param_not_empty,
    is_level_assigned,
    build_issue,
)

from wpf_dialog import show_structuralqc_dialog


OUTPUT = script.get_output()


def _describe_elem(elem: DB.Element) -> str:
    cat = elem.Category.Name if elem.Category else "N/A"
    name = getattr(elem, "Name", "") or ""
    return "{} | {} | {}".format(elem.Id.IntegerValue, cat, name)


def run():
    doc = DOC
    if not doc:
        UI.TaskDialog.Show("Structural QC", "No hay documento activo.")
        return

    cfg = show_structuralqc_dialog()
    if cfg is None:
        # Cancelado
        return

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
        "Resumen Structural QC\n\n"
        "Elementos revisados: {total}\n"
        "Fallas por Comments: {fc}\n"
        "Fallas por Level: {fl}\n"
        "Incidencias totales: {ti}\n"
    ).format(
        total=len(elements),
        fc=counters["fail_comments"],
        fl=counters["fail_level"],
        ti=len(issues),
    )
    UI.TaskDialog.Show("Structural QC – WSP BIM Peru", msg)


if __name__ == "__main__":
    run()