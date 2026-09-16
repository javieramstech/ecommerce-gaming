# Arquitectura del Sistema - JMSHOP

## 1. Visión General
**JMSHOP** es una aplicación web de comercio electrónico (Ecommerce) Single-Page desarrollada sobre estándares web modernos. Está diseñada para la exhibición y comercialización de **productos tecnológicos** (hardware, notebooks, periféricos, licencias de software) y **servicios especializados** (armado de PC personalizado, mantenimiento y soporte).

## 2. Stack Tecnológico
- **Maquetado:** HTML5 Semántico (estándar W3C).
- **Estilos & Diseño Responsive:** TailwindCSS v3 inyectado vía CDN (`https://cdn.tailwindcss.com`).
- **Tipografía:** Google Fonts (`Playfair Display` para títulos y `Roboto` para textos de cuerpo).
- **Lógica e Interactividad:** JavaScript Vanilla (ES6+) ejecutable en el cliente (DOM Manipulation, Event Listeners).

## 3. Mapa de Módulos y Estructura Visual
De arriba hacia abajo en `index.html`:
1. **Header / Navbar:**
   - Logotipo de la marca (`JMSHOP`).
   - Navegación de secciones (Inicio, Catálogo, Contacto).
   - Botón interactivo de Alternador de Tema (Modo Oscuro / Modo Claro).
   - Menú hamburguesa desplegable para dispositivos móviles.
2. **Hero Section (Portada):**
   - Encabezado principal de alto impacto visual.
   - Subtítulo descriptivo de productos y servicios.
   - Botón de llamada a la acción (Call To Action).
3. **Sección Catálogo (Productos & Servicios):**
   - Grilla dinámica de 6 tarjetas de muestra (Hardware, Notebooks, Licencias y Servicio de Armado de PC).
   - Componentes modal / detalle para ampliar información al hacer clic.
4. **Sección Contacto & Asesoramiento:**
   - Formulario interactivo con validación visual (Nombre, Email, Mensaje).
   - Botón de confirmación con alerta de éxito.
   - Botón secundario con enlace directo a WhatsApp.
5. **Footer (Pie de Página):**
   - Información de copyright, canales de comunicación y redes sociales.

## 4. Tecnologías Prohibidas (Límites Estrictos)
Para garantizar la simplicidad del código y alinearse al estándar del curso, **queda estrictamente prohibido**:
- ⛔ Frameworks SPA pesados: React, Angular, Vue, Svelte.
- ⛔ Entornos Backend: Node.js, Express, Python, PHP.
- ⛔ Bases de datos: SQL (PostgreSQL, MySQL) o NoSQL (MongoDB, Firebase).
- ⛔ Estilos en línea: Prohibido usar atributos `style="..."` dentro de etiquetas HTML.
