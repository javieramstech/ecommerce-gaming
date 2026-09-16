# Convenciones de Diseño y Código - JMSHOP

## 1. HTML5 Semántico
Se exige el uso estricto de etiquetas semánticas para garantizar estructura accesible y SEO limpio:
- `<header>` para la barra superior y navegación.
- `<nav>` para contenedores de enlaces de navegación.
- `<main>` como contenedor principal del contenido de la página.
- `<section>` para delimitar módulos (Hero, Catálogo, Contacto).
- `<article>` para cada tarjeta de producto o servicio individual.
- `<footer>` para el pie de página.
- `<button>` obligatoriamente para todos los elementos interactivos que disparen acciones JavaScript.

## 2. Paleta de Colores & Temas CSS
- **Modo Oscuro (Default):**
  - Fondo Principal: Slate 900 (`#0f172a` / `bg-slate-900`)
  - Contenedores/Tarjetas: Slate 800 (`#1e293b` / `bg-slate-800`)
  - Color Primario (Acento): Violeta Neón (`#8b5cf6` / `text-violet-500` / `bg-violet-600`)
  - Acento Secundario: Fucsia (`#ec4899` / `bg-pink-500`)
  - Texto Principal: Slate 50 (`#f8fafc` / `text-slate-50`)
  - Texto Secundario: Slate 400 (`#94a3b8` / `text-slate-400`)

- **Modo Claro (Toggle):**
  - Fondo Principal: Slate 50 (`#f8fafc` / `bg-slate-50`)
  - Contenedores/Tarjetas: Blanco (`#ffffff` / `bg-white`)
  - Color Primario (Acento): Esmeralda (`#10b981` / `bg-emerald-600`)
  - Acento Secundario: Azul Marino (`#1e3a8a` / `text-blue-900`)
  - Texto Principal: Slate 900 (`#0f172a` / `text-slate-900`)

## 3. Tipografía
Cargadas desde Google Fonts:
- **Títulos (`<h1>`, `<h2>`, `<h3>`):** `Playfair Display` (`font-serif`, `font-bold`).
- **Párrafos, Botones e Insumos de Formulario:** `Roboto` (`font-sans`, `font-normal`).

## 4. Diseño Responsive
- **Breakpoints Tailwind:**
  - Móvil (`< 768px`): Grilla de tarjetas en 1 columna (`grid-cols-1`). Menú hamburguesa desplegable.
  - Escritorio (`>= 768px`): Grilla de tarjetas en 3 columnas (`md:grid-cols-3`). Menú horizontal abierto.
- **Botones y Táctil:** Botones con padding amplio en pantallas móviles (`py-3 px-6`) para facilitar la pulsación táctil.

## 5. Micro-interacciones (Hover Effects)
- Transición suave de color y brillo en botones (`transition-all duration-300`).
- Elevación leve en tarjetas al pasar el cursor (`hover:-translate-y-1 hover:shadow-xl`).
- Ligero efecto de zoom fluido en la imagen de la tarjeta (`hover:scale-105 transition-transform duration-300`).
