# Configuración IDE para WSP_PB_PE_BIM – Advertencias de Pylance/Pyright

## Contexto

WSP_PB_PE_BIM es una **extensión pyRevit**, que significa:

1. **Entorno de ejecución:** CPython 3.8+ dentro de Revit (proporcionado por pyRevit)
2. **Módulos especiales disponibles SOLO en runtime:**
   - `pyrevit` (wrapper de pyRevit)
   - `Autodesk.Revit.DB` / `Revit API`
   - `clr` (pythonnet / IronPython)
   - `System.*` (módulos .NET: IO, Windows, etc.)

3. **En el IDE (VS Code/VS):** Estos módulos **no están instalados**, por lo que Pylance/Pyright generan advertencias.

---

## Advertencias Comunes (y por qué son esperadas)

```
reportMissingImports: Import "pyrevit" could not be resolved
reportMissingImports: Import "clr" could not be resolved
reportMissingImports: Import "System.IO" could not be resolved
reportUndefinedVariable: "DB" is not defined
```

**Son normales y esperadas.** El código funciona correctamente dentro de Revit.

---

## Solución: Archivos de Configuración

Se han creado 3 archivos para suprimir estas advertencias:

### 1. `pyrightconfig.json` (Pylance/Pyright)
- Desactiva `reportMissingImports` y `reportUndefinedVariable`
- Define versión Python: `3.8` (estándar en pyRevit)

**Localización:**
```
WSP_PB_PE_BIM.extension/pyrightconfig.json
```

### 2. `.vscode/settings.json` (VS Code)
- Configura el workspace para usar Pyright
- Desactiva type checking mode para evitar ruido

**Localización:**
```
WSP_PB_PE_BIM.extension/.vscode/settings.json
```

### 3. `stubs/` (Type hints para IDE)
Stubs (.pyi) para módulos que solo existen en runtime:

```
WSP_PB_PE_BIM.extension/
├── stubs/
│   ├── pyrevit.pyi        # Stubs para pyRevit
│   └── system.pyi         # Stubs para System.* modules
```

Estos archivos ayudan a que el IDE **reconozca las signaturas** sin requerir los módulos.

---

## Cómo Usar (VS Code)

### Opción A: Abrir la carpeta de la extensión (recomendado)
```bash
cd WSP_PB_PE_BIM.extension
code .
```

VS Code automáticamente leerá `pyrightconfig.json` y `.vscode/settings.json`.

### Opción B: Abrir desde la raíz
```bash
cd WSP_PB_PE_BIM
code .
```

Asegúrate de que VS Code reconoce la carpeta `WSP_PB_PE_BIM.extension/` como workspace.

---

## Cómo Verificar

1. Abre VS Code
2. Abre la paleta de comandos: `Ctrl+Shift+P`
3. Busca: "Python: Show Pythonpath" o "Pyright: Status"
4. Verifica que Pyright está activo y `pyrightconfig.json` es reconocido

---

## Si Siguen Apareciendo Advertencias

### En script.py y wpf_dialog.py:
- Se ha añadido `# type: ignore[import]` en imports problemáticos
- Estos comentarios le dicen a Pylance: "Confía en mí, esto funciona en runtime"

### En wsp_utils.py:
- Se ha cambiado `elem: DB.Element` a `elem: Any` para evitar "DB is not defined"
- El código sigue siendo correcto y funciona en Revit

---

## Desarrollo Local (sin Revit)

Si quieres ejecutar tests o verificaciones sin Revit:

```bash
# Crea un venv
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Instala pytest (opcional)
pip install pytest

# Ejecuta tests (sin Revit API)
pytest tests/
```

Los tests en `tests/` están diseñados para **no depender de Revit API**.

---

## Referencias

- [pyRevit Docs – Extensions](https://docs.pyrevitlabs.io/reference/pyrevit/extensions/)
- [Pyright Configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
- [Type Hints for Python 3.8](https://docs.python.org/3.8/library/typing.html)

---

## Resumen

✅ **Las advertencias son normales y se han configurado para no interferir.**
✅ **El código funciona correctamente dentro de Revit.**
✅ **Use `# type: ignore` solo cuando sea necesario.**

Si necesitas más detalles, revisa `pyrightconfig.json` y `.vscode/settings.json`.
