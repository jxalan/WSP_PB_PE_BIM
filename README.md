# WSP_PB_PE_BIM – pyRevit Extension

Extensión corporativa pyRevit para **WSP Perú**, orientada a herramientas BIM internas de **QA/QC, modelado, documentación y coordinación** en Revit.

---

## ✅ Requisitos

- Autodesk Revit **2024 / 2025 / 2026** (inglés)
- **pyRevit ≥ 6.1.x** instalado y adjunto a Revit
- Git y Visual Studio (recomendado, no obligatorio)

---

## 📦 Instalación (usuarios)

Instalar la extensión directamente desde GitHub:

```sh
pyrevit extend extension https://github.com/TU_USUARIO/WSP_PB_PE_BIM.git WSP_PB_PE_BIM
```

Reinicia Revit después de la instalación.

🔄 Actualización
Para traer la última versión del repositorio:

```sh
pyrevit extensions update WSP_PB_PE_BIM
```

🧭 Ubicación en Revit
En el Ribbon aparecerá:
Tab: WSP BIM Peru
Panels:

- QA / QC
- Modelado
- Documentación
- Coordinación


🧪 Primer comando disponible
**Structural QC (QA / QC)**
Herramienta de revisión rápida para elementos estructurales:

Tipos:

- Muros estructurales
- Columnas estructurales

Checks:

- Parámetro Comments no vacío
- Level asignado

Los resultados se muestran:

- En la consola de pyRevit (detalle)
- En un resumen final (TaskDialog)


🧱 Estructura base de la extensión

WSP_PB_PE_BIM.extension/
├─ lib/                    # Utilidades compartidas
├─ WSP BIM Peru.tab/
│  ├─ QA_QC.panel/
│  │  └─ Structural QC.pushbutton/
│  │     ├─ script.py
│  │     └─ ui/StructuralQC_Dialog.xaml
│  ├─ Modeling.panel/
│  ├─ Docs.panel/
│  └─ Coordination.panel/

La estructura de carpetas define automáticamente Tabs, Panels y Buttons en Revit (convención pyRevit).


🛠 Desarrollo (equipo BIM)

- Motor Python: CPython 3 (#! python3)
- UI: WPF (.xaml) cargado con XamlReader
- No se requiere proyecto .NET ni compilación

Se recomienda trabajar en Visual Studio – Open Folder.


🤖 Uso de GitHub Copilot Pro
Copilot Pro puede usarse para:

- Refinar scripts pyRevit
- Mejorar diálogos WPF (XAML)
- Crear nuevas herramientas QA/QC
- Documentar estándares WSP

Copilot es apoyo, no reemplaza el criterio BIM / Revit API.


📄 Licencia / Uso
Extensión de uso interno WSP Perú.
Distribución externa solo con autorización del equipo BIM.

---

Contribuciones
--------------

Este repositorio está pensado para uso interno. Para contribuciones internas:

- Forzar uso de branch feature/* y enviar Pull Requests a main.
- Mantener la compatibilidad con Revit 2024-2026 y pyRevit 6.x.
- Añadir tests para la lógica que no dependa de la API de Revit.

Soporte
-------

Equipo BIM — bim@wsp.pe
