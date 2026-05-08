# 📝 Guía: Personalizar Tool1 y Tool2

**Objetivo:** Convertir los templates genéricos en herramientas funcionales específicas.

---

## 🔧 Estructura Actual de Templates

```
Tool1.pushbutton/
├── script.py                    ← Código principal (copiar de Structural QC)
├── wpf_dialog.py                ← Dialog WPF (copiar de Structural QC)
├── bundle.yaml                  ← Metadatos (actualizar)
└── ui/
    └── StructuralQC_Dialog.xaml ← Interfaz (copiar de Structural QC)

Tool2.pushbutton/               ← Mismo formato
└── ...
```

Actualmente son **copias exactas de Structural QC**.

---

## 📋 Pasos para Personalizar

### PASO 1: Renombrar la Carpeta

```bash
# Opción A: Renombrar Tool1 a algo descriptivo
# Ej: "Walls QC" para revisión de muros
mv "Tool1.pushbutton" "Walls QC.pushbutton"

# Opción B: Renombrar Tool2
# Ej: "Columns QC" para revisión de columnas
mv "Tool2.pushbutton" "Columns QC.pushbutton"
```

### PASO 2: Actualizar bundle.yaml

Archivo original (Tool1/bundle.yaml):
```yaml
<metadata>
  <Name>Tool1</Name>
  <Text>Tool1</Text>
  <Description></Description>
  <Image></Image>
  <Assembly></Assembly>
  <Class></Class>
  <Owner></Owner>
</metadata>
```

**Editar a:**
```yaml
<metadata>
  <Name>Walls QC</Name>
  <Text>Walls QC</Text>
  <Description>Verificación de muros: parámetros, niveles, conectividad</Description>
  <Image></Image>
  <Assembly></Assembly>
  <Class></Class>
  <Owner>WSP BIM Peru</Owner>
</metadata>
```

### PASO 3: Renombrar el XAML

```bash
# En Tool1/ui/
mv StructuralQC_Dialog.xaml WallsQC_Dialog.xaml

# Actualizar el path en wpf_dialog.py:
# Cambiar: xaml_path = os.path.join(base_dir, "ui", "StructuralQC_Dialog.xaml")
# A:       xaml_path = os.path.join(base_dir, "ui", "WallsQC_Dialog.xaml")
```

### PASO 4: Personalizar wpf_dialog.py

#### Cambiar el nombre de la clase Dataclass:
```python
# Antes
@dataclass(frozen=True)
class StructuralQCConfig:
    check_walls: bool
    check_columns: bool
    check_comments: bool
    check_level: bool

# Después (Tool1 - Walls QC)
@dataclass(frozen=True)
class WallsQCConfig:
    check_connectivity: bool
    check_height: bool
    check_thickness: bool
    check_constraints: bool
```

#### Cambiar el nombre de la función:
```python
# Antes
def show_structuralqc_dialog() -> Optional[StructuralQCConfig]:

# Después
def show_wallsqc_dialog() -> Optional[WallsQCConfig]:
```

### PASO 5: Personalizar script.py

#### Actualizar imports:
```python
# Cambiar
from wpf_dialog import show_structuralqc_dialog

# A
from wpf_dialog import show_wallsqc_dialog
```

#### Cambiar el dialog y la lógica:
```python
def run() -> None:
    # ... [import código igual] ...

    cfg = show_wallsqc_dialog()  # ← Cambiar
    if cfg is None:
        return None

    # Cambiar la lógica de elementos
    elements = []

    if cfg.check_connectivity:
        # Implementar lógica de conectividad
        elements.extend(get_walls_with_issues(doc, "connectivity"))

    if cfg.check_height:
        # Implementar lógica de altura
        elements.extend(get_walls_with_issues(doc, "height"))

    # ... [resto del código] ...
```

### PASO 6: Personalizar XAML (WallsQC_Dialog.xaml)

Cambiar los nombres de los controles y labels:

```xml
<!-- Antes (CheckBox para Walls) -->
<CheckBox x:Name="chkWalls" Content="Muros estructurales"/>

<!-- Después (CheckBox para Conectividad) -->
<CheckBox x:Name="chkConnectivity" Content="Verificar conectividad de muros"/>

<!-- Cambiar los demás según funcionalidad -->
<CheckBox x:Name="chkHeight" Content="Verificar altura"/>
<CheckBox x:Name="chkThickness" Content="Verificar espesor"/>
<CheckBox x:Name="chkConstraints" Content="Verificar restricciones"/>
```

### PASO 7: Actualizar wsp_utils.py (si es necesario)

Si necesitas funciones nuevas, añadir en `lib/wsp_utils.py`:

```python
def get_walls_with_issues(doc: Any, check_type: str) -> list[Any]:
    """
    Retorna muros que fallan ciertos checks.
    check_type: "connectivity", "height", "thickness", "constraints"
    """
    from pyrevit import DB

    walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
    issues = []

    for wall in walls:
        if check_type == "connectivity":
            # Implementar lógica
            pass
        elif check_type == "height":
            # Implementar lógica
            pass

    return issues
```

---

## 📌 Ejemplo Completo: Tool1 → Walls QC

### Archivos a Cambiar

1. **bundle.yaml**
   - Name: "Walls QC"
   - Text: "Walls QC"
   - Description: "Revisión de muros estructurales"

2. **wpf_dialog.py**
   - Rename class: `StructuralQCConfig` → `WallsQCConfig`
   - Rename function: `show_structuralqc_dialog()` → `show_wallsqc_dialog()`
   - Update dataclass fields to: `check_connectivity`, `check_height`, etc.

3. **script.py**
   - Change import: `from wpf_dialog import show_wallsqc_dialog`
   - Change call: `cfg = show_wallsqc_dialog()`
   - Update elements collection logic
   - Change output messages

4. **ui/WallsQC_Dialog.xaml** (renombrar desde StructuralQC_Dialog.xaml)
   - Update checkbox x:Name attributes
   - Update Content labels
   - Update Title y descriptions

5. **lib/wsp_utils.py** (si necesitas funciones nuevas)
   - Add `get_walls_with_connectivity_issues()`
   - Add `get_walls_height_issues()`
   - etc.

---

## ✅ Checklist Final

- [ ] Carpeta renombrada (Tool1 → nombre descriptivo)
- [ ] bundle.yaml actualizado
- [ ] XAML renombrado y contenido actualizado
- [ ] wpf_dialog.py: Classes y funciones renombradas
- [ ] script.py: Imports y lógica actualizados
- [ ] wsp_utils.py: Funciones nuevas si necesarias
- [ ] Testear en Revit
- [ ] Verificar que aparece en Ribbon
- [ ] Dialog modal funciona
- [ ] Output en consola y TaskDialog

---

## 💡 Tips

- Mantener la estructura de carpetas igual
- No cambiar `bundle.yaml` del parent (`QA_QC.panel/bundle.yaml`)
- Probar cambios después de cada paso principal
- Usar `pyrevit revit logs show` si hay errores

