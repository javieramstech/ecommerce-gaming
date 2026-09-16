# Errores Conocidos y Gotchas de Maquetado - JMSHOP

## 1. Prevención de Scroll Horizontal Roto
- **Síntoma:** Aparece una barra de desplazamiento horizontal no deseada en celulares debido a elementos o imágenes que sobrepasan el ancho de la pantalla (`vw`).
- **Solución:**
  - Agregar la clase `overflow-x-hidden` en la etiqueta `<body>` o contenedor principal.
  - Asegurar que las imágenes contengan `w-full h-auto` y `max-w-full`.

## 2. Accesibilidad y Atributo `alt` en Imágenes
- **Síntoma:** Lectores de pantalla y validadores HTML fallan por imágenes sin descripción.
- **Solución:**
  - Todas las fotos de tarjetas de productos y servicios deben incluir obligatoriamente el atributo `alt="..."` especificando el nombre del ítem (ej: `alt="Notebook Gamer i7 RTX 4060"`).

## 3. Uso Semántico de Etiquetas Cliqueables
- **Síntoma:** Asignar eventos de clic a contenedores `<div>` o `<span>`, lo que rompe la navegación por teclado (Tab) y accesibilidad.
- **Solución:**
  - Todo elemento cliqueable debe ser una etiqueta `<button>` o un enlace `<a>`.

## 4. Contraste de Texto sobre Fondos Dinámicos (Dark/Light)
- **Síntoma:** Textos ilegibles o grises oscuros sobre fondos oscuros al alternar temas.
- **Solución:**
  - Usar clases de contraste Tailwind vinculadas al tema: `text-slate-50 dark:text-slate-50` para textos claros en modo oscuro y `text-slate-900` para modo claro.

## 5. Prevención de IDs Duplicados
- **Síntoma:** Múltiples botones o modales comparten el mismo atributo `id`, haciendo que JavaScript solo seleccione el primer elemento.
- **Solución:**
  - Usar clases para seleccionar grupos de elementos o generar atributos de datos únicos (ej: `data-product-id="1"`).
