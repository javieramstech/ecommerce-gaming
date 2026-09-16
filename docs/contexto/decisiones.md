# Registro de Decisiones de Arquitectura (ADR) - JMSHOP

## Regla de Control de Guardas
⚠️ **Importante:** Cualquier alteración en reglas de negocio existentes, modelos de datos de productos/servicios o manejo de eventos requiere explicación previa de impacto y **autorización explícita del usuario**.

---

### [ADR-001] [2026-09-15 19:43] - Stack Frontend Simple y Ágil
- **Estado:** Aprobado.
- **Contexto:** Se requiere maquetar una tienda web sin la complejidad de compiladores pesados.
- **Decisión:** Adoptar HTML5 semántico, TailwindCSS v3 (CDN) y JavaScript Vanilla puro.
- **Consecuencias:** Desarrollo directo en el navegador, sin necesidad de instalación de npm ni bundlers.

---

### [ADR-002] [2026-09-15 19:43] - Catálogo Mixto de Productos y Servicios
- **Estado:** Aprobado.
- **Contexto:** JMSHOP no solo vende componentes físicos, sino también servicios técnicos.
- **Decisión:** Diseñar la grilla de catálogo con soporte para productos (hardware, notebooks, licencias) y servicios (armado de PC personalizado, mantenimiento).
- **Consecuencias:** Las tarjetas incorporan etiquetas de categoría distintivas ("Producto" vs "Servicio") y botones adaptados.

---

### [ADR-003] [2026-09-15 19:43] - Interfaz con Soporte Dual de Tema (Dark/Light)
- **Estado:** Aprobado.
- **Contexto:** La comunidad gamer prefiere temas oscuros, pero se requiere accesibilidad en entornos iluminados.
- **Decisión:** Iniciar la aplicación en Modo Oscuro por defecto e incluir un toggle interactivo en la Navbar para alternar dinámicamente a Modo Claro mediante clases de Tailwind.
- **Consecuencias:** Requiere un pequeño script JS para alternar la clase `dark` en la etiqueta `<html>`.

---

### [ADR-004] [2026-09-15 19:43] - Integración Directa con WhatsApp para Cotizaciones
- **Estado:** Aprobado.
- **Contexto:** Los usuarios requieren atención inmediata para la cotización de servicios de armado de PC.
- **Decisión:** Agregar en la sección de contacto un botón secundario directo a la API de WhatsApp (`https://wa.me/...`).
- **Consecuencias:** Facilita la conversión rápida sin depender de un backend de correo.

---

### [ADR-005] [2026-09-15 22:05] - Rediseño Gaming Obsidian Cyberpunk & Estructura Multi-página con Pasarela de Pago
- **Estado:** Aprobado.
- **Contexto:** El usuario solicitó un diseño gaming profesional, minimalista y de alto impacto, superando estética genérica de IA.
- **Decisión:** Estilo Obsidian Cyberpunk, arquitectura de dos páginas (`index.html` y `catalogo.html`), Carrito Drawer Lateral flotante y Checkout con Pasarela de Pago simulada.

---

### [ADR-006] [2026-09-15 22:46] - PC Builder Interactivo (builder.html) y Perfeccionamiento del Sistema de Diseño Dual
- **Estado:** Aprobado (vía feedback visual).
- **Contexto:** El usuario solicitó agregar la herramienta interactiva "Arma tu PC" (`builder.html`) al estilo CompraGamer/Maximus Gaming con verificación de compatibilidad, cálculo de watts y cotizador; corregir la navegación uniforme (`Inicio` | `Catálogo` | `Arma tu PC` | `Servicios` | `Contacto`); ajustar el Modo Claro a un tono blanco suave/apagadito; corregir los números superpuestos en las tarjetas de servicios reemplazándolos por iconos neón; cambiar el botón de contacto a "Enviar Consulta"; e inyectar los logotipos vectoriales idénticos de las marcas top (NVIDIA, ASUS, AMD, MSI, CORSAIR, REDRAGON, KINGSTON).
- **Decisión:**
  1. Crear `builder.html` y `assets/js/builder.js` con validador de sockets/RAM/fuente.
  2. Sincronizar el header en todas las páginas con los mismos 5 enlaces.
  3. Perfeccionar Modo Claro en `assets/css/styles.css` con fondos slate-100 suave (`#f1f5f9`), no deslumbrantes.
  4. Rediseñar tarjetas de servicio sin texto superpuesto, agregando badges con íconos vectoriales.
  5. Actualizar el botón del formulario de contacto a "Enviar Consulta".
  6. Utilizar logotipos SVGs oficiales idénticos a los del ejemplo de referencia en el marquee.
