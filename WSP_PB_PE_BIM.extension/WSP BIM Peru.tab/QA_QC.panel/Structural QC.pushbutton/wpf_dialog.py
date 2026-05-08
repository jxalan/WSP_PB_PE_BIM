# -*- coding: utf-8 -*-
"""
wpf_dialog.py
Helper para cargar y manejar el diálogo WPF (XAML) del comando Structural QC.

- Carga XAML desde ./ui/StructuralQC_Dialog.xaml
- Lee estados de CheckBoxes al presionar 'Ejecutar'
- Devuelve dict con flags o None si se canceló
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

# These are available only at runtime within pyRevit environment
# IDE linting will warn; use type: ignore comments to suppress
try:
    import clr  # type: ignore[import] - pythonnet (CPython) inside pyRevit

    clr.AddReference("PresentationFramework")
    clr.AddReference("PresentationCore")
    clr.AddReference("WindowsBase")

    from System.IO import File, FileAccess, FileMode, FileShare  # type: ignore[import]
    from System.Windows import Window  # type: ignore[import]
    from System.Windows.Markup import XamlReader  # type: ignore[import]
except ImportError:
    # IDE import check; modules available at runtime in pyRevit
    clr = None  # type: ignore[assignment]
    File = None  # type: ignore[assignment]
    FileAccess = None  # type: ignore[assignment]
    FileMode = None  # type: ignore[assignment]
    FileShare = None  # type: ignore[assignment]
    Window = None  # type: ignore[assignment]
    XamlReader = None  # type: ignore[assignment]


@dataclass(frozen=True)
class StructuralQCConfig:
    check_walls: bool
    check_columns: bool
    check_comments: bool
    check_level: bool


def _load_window_from_xaml(xaml_path: str) -> Window:
    """Carga un Window desde un archivo XAML."""
    if not os.path.exists(xaml_path):
        raise IOError("No se encontró el XAML en: {}".format(xaml_path))

    # Abrir archivo como stream .NET (más robusto que parsear text plano)
    fs = File.Open(xaml_path, FileMode.Open, FileAccess.Read, FileShare.Read)
    try:
        win = XamlReader.Load(fs)
    finally:
        fs.Close()
    return win


def show_structuralqc_dialog() -> Optional[StructuralQCConfig]:
    """
    Muestra el diálogo modal y retorna configuración seleccionada.
    Retorna None si el usuario cancela/cierra.
    """
    base_dir = os.path.dirname(__file__)
    xaml_path = os.path.join(base_dir, "ui", "StructuralQC_Dialog.xaml")

    win = _load_window_from_xaml(xaml_path)

    # Controles
    chk_walls = win.FindName("chkWalls")
    chk_cols = win.FindName("chkColumns")
    chk_comm = win.FindName("chkComments")
    chk_lvl = win.FindName("chkLevel")
    btn_run = win.FindName("btnRun")
    btn_cancel = win.FindName("btnCancel")

    # Estado interno para capturar resultado
    result_config: Optional[StructuralQCConfig] = None
    user_confirmed = False

    def _is_checked(chk) -> bool:
        # IsChecked es Nullable[bool] en WPF
        try:
            return bool(chk.IsChecked)
        except Exception:
            return False

    def on_run(sender, args) -> None:
        nonlocal result_config, user_confirmed
        result_config = StructuralQCConfig(
            check_walls=_is_checked(chk_walls),
            check_columns=_is_checked(chk_cols),
            check_comments=_is_checked(chk_comm),
            check_level=_is_checked(chk_lvl),
        )
        user_confirmed = True
        win.DialogResult = True  # cierra modal
        win.Close()

    def on_cancel(sender, args) -> None:
        nonlocal result_config, user_confirmed
        result_config = None
        user_confirmed = False
        win.DialogResult = False
        win.Close()

    # Wire events
    if btn_run:
        btn_run.Click += on_run
    if btn_cancel:
        btn_cancel.Click += on_cancel

    # Mostrar modal
    win.ShowDialog()

    return result_config if user_confirmed else None