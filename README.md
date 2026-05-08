# WSP_PB_PE_BIM – pyRevit Extension

Extensión corporativa pyRevit para **WSP Perú**, con herramientas BIM internas de **QA/QC, modelado, documentación y coordinación** en Revit.

---

## ✅ Requisitos

- Autodesk Revit **2024 / 2025 / 2026** (inglés)
- **pyRevit ≥ 6.1.x** instalado y adjunto a Revit
- Git y Visual Studio o VS Code (recomendado)

---

## 📦 Instalación (usuarios)

Instalar la extensión directamente desde GitHub:

```sh
pyrevit extend extension https://github.com/jxalan/WSP_PB_PE_BIM.git WSP_PB_PE_BIM
```

Reinicia Revit después de la instalación.

### 🔄 Actualización

Para traer la última versión del repositorio:

```sh
pyrevit extensions update WSP_PB_PE_BIM
```

### 🧭 Ubicación en Revit

En el Ribbon aparecerá:
- **Tab:** WSP BIM Peru
- **Panels:**
  - QA / QC
  - Modeling
  - Docs
  - Coordination


## 🧪 Herramientas Disponibles

### Structural QC (QA / QC)
Herramienta de revisión rápida para elementos estructurales.

**Elementos verificados:**
- Muros estructurales
- Columnas estructurales

**Validaciones:**
- Parámetro `Comments` no vacío
- `Level` asignado correctamente

**Salida:**
- Detalle clickable en consola pyRevit (IDs de elementos)
- Resumen en diálogo con estadísticas
- Información de elementos que no cumplen

**Próximas herramientas:**
- QA/QC: Vigas, losas, muros arquitectónicos
- Modeling: Validación de familias y parámetros
- Docs: Exportación de vistas y planos
- Coordination: Revisión interdisciplinaria


## 🧱 Estructura del Proyecto

```
WSP_PB_PE_BIM/
├── README.md                                    # Documentación principal
├── WSP_PB_PE_BIM.extension/
│   ├── bundle.yaml                              # Manifiesto extensión
│   ├── pyrightconfig.json                       # Configuración Pyright
│   ├── pyproject.toml                           # Dependencias Python
│   ├── CONFIGURACION_IDE.md                     # Guía IDE y troubleshooting
│   ├── lib/
│   │   └── wsp_utils.py                         # Utilidades compartidas
│   ├── stubs/                                   # Type hints para módulos externos
│   │   ├── pyrevit.pyi
│   │   └── system.pyi
│   └── WSP BIM Peru.tab/                        # Estructura pyRevit
│       ├── QA_QC.panel/
│       │   └── Structural QC.pushbutton/
│       │       ├── script.py                    # Lógica principal
│       │       ├── wpf_dialog.py                # UI WPF
│       │       ├── bundle.yaml                  # Configuración botón
│       │       └── ui/
│       │           └── StructuralQC_Dialog.xaml # Diálogo WPF
│       ├── Modeling.panel/
│       ├── Docs.panel/
│       └── Coordination.panel/
```

**Convención pyRevit:** La estructura de carpetas define automáticamente Tabs, Panels y Buttons en Revit.


## 🛠 Desarrollo (equipo BIM)

### Stack Técnico
- **Python:** CPython 3.8+ (proporcionado por pyRevit)
- **UI:** WPF con XAML (XamlReader + IronPython)
- **API:** Revit API 2024+ (pyRevit wrapper)
- **No requiere:** Proyecto .NET, compilación C#

### Setup IDE

1. **Clonar repositorio:**
   ```sh
   git clone https://github.com/jxalan/WSP_PB_PE_BIM.git
   cd WSP_PB_PE_BIM
   ```

2. **Abrir en Visual Studio / VS Code:**
   - Visual Studio 2022+: `File → Open Folder`
   - VS Code: Abrir carpeta del proyecto

3. **Instalar en Revit (desarrollo):**
   ```sh
   pyrevit extend source --force "C:\Dev\WSP_PB_PE_BIM\WSP_PB_PE_BIM.extension"
   ```
   Esto vincula el repositorio local directamente a Revit.

### Advertencias de IDE Esperadas

Los módulos `pyrevit`, `clr`, y `System.*` solo existen **dentro de Revit en runtime**.
- ⚠️ Pylance/Pyright en el IDE mostrará advertencias → **es normal**
- ✅ El código funciona perfectamente en Revit

**Solución:** Lee [CONFIGURACION_IDE.md](./WSP_PB_PE_BIM.extension/CONFIGURACION_IDE.md) para activar type stubs y desactivar warnings.


## 🤖 Uso de GitHub Copilot Pro

Copilot es **apoyo para desarrollo**, no reemplaza criterio BIM/Revit API:

- ✅ Refinar scripts pyRevit existentes
- ✅ Mejorar diálogos WPF (XAML)
- ✅ Crear nuevas herramientas QA/QC
- ✅ Documentar estándares WSP
- ❌ **Nunca** confiar ciegamente en sugerencias sin validar en Revit


## 📄 Licencia y Distribución

Extensión de uso interno **WSP Perú**.
- ✅ Distribución interna dentro de WSP
- ❌ Distribución externa solo con autorización del equipo BIM

---

## 🤝 Contribuciones

Este repositorio es **para desarrollo interno del equipo BIM**.

**Estándares:**
- Usar branches `feature/*` para nuevas herramientas
- Enviar Pull Requests a `main` para review
- Mantener compatibilidad: **Revit 2024-2026** + **pyRevit 6.x+**
- Añadir tests para lógica no dependiente de API Revit

---

## 📞 Soporte

**Equipo BIM:** bim@wsp.pe

**Bugs / Requests:** Abrir issues en GitHub o contactar al equipo
