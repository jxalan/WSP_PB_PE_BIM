# Configuración IDE – WSP_PB_PE_BIM

## ¿Por qué VS Code / Visual Studio muestra advertencias?

Los módulos `pyrevit`, `clr`, y `System.*` **solo existen dentro de Revit en runtime**.
El IDE intenta validarlos en tu máquina → advertencias falsas.

✅ **Es normal. El código funciona perfectamente en Revit.**

---

## Solución

**Archivo:** `pyrightconfig.json`
- Desactiva advertencias de imports faltantes
- Define Python 3.8 como versión objetivo

Los imports en el código tienen `# type: ignore[import]` para que el IDE no proteste.



---

## Cómo Abrir en el IDE

```bash
cd WSP_PB_PE_BIM
code .              # VS Code
# o
start .             # Visual Studio 2022+ (Open Folder)
```

---

## ¿Aún ves advertencias?

Es normal. Ignóralas con seguridad:
- Las advertencias no afectan la funcionalidad
- El código funciona correctamente en Revit
- Están configuradas para no bloquearte
