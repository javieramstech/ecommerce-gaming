# Flujo de Trabajo y Definition of Done - JMSHOP

## 1. Pasos de Maquetado SDD (Software Design Description)

### Paso 1: Estructura HTML5 Semántica
- Creación de `index.html`.
- Definición de etiquetas semánticas (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).
- Incorporación de metadatos UTF-8, viewport responsive y fuentes de Google Fonts.

### Paso 2: Diseño & Estilos con TailwindCSS v3 (CDN)
- Configuración del script CDN de TailwindCSS.
- Aplicación de clases utilitarias para maquetado de contenedores, grillas responsive (`grid-cols-1 md:grid-cols-3`) y tipografías.
- Implementación de estilos para Modo Oscuro y Modo Claro.

### Paso 3: Interactividad y Comportamiento con JavaScript Vanilla
- Creación de scripts para:
  - Apertura / Cierre del menú hamburguesa en móviles.
  - Conmutador de tema (Dark / Light mode).
  - Apertura de modal con información detallada de productos/servicios.
  - Validación del formulario de contacto y despliegue del mensaje de éxito.
  - Redirección del botón de WhatsApp con mensaje preformateado.

---

## 2. Definition of Done (DoD) - Criterios de Aceptación
Antes de dar por completado cualquier componente o avance en la página:

1. **Justificación Técnica:** Breve explicación técnica del cambio realizado.
2. **Validación HTML & JS:** Código HTML semántico válido, sin errores ni advertencias en la consola del navegador (`F12`).
3. **Verificación Visual de los 4 Estados UI:**
   - 🟢 **Success:** Estado normal con datos desplegados correctamente.
   - 🔄 **Loading:** Indicador visual mientras se simulan acciones o cargas.
   - ⚠️ **Empty:** Manejo visual si una sección o búsqueda no contiene datos.
   - ❌ **Error:** Feedback visual claro si el usuario comete un error en un formulario.
4. **Prueba Responsive:** Verificación en tamaños de escritorio (1280px) y móviles (375px/414px en Chrome DevTools).
5. **Código Limpio:** Cumplimiento de convenciones, código legible y organizado.
