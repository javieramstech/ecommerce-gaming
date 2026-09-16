import json
import sys
import os

# Asegurar importación del paquete app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select, delete
from app.db.database import engine, init_db
from app.models.user import User
from app.models.product import Product
from app.core.security import get_password_hash

INITIAL_PRODUCTS = [
    # ==========================================
    # HARDWARE & COMPONENTES (26 ÍTEMS)
    # ==========================================
    {
        "title": "Placa de Video ASUS ROG Strix RTX 4080 Super 16GB OC",
        "category": "hardware",
        "type": "producto",
        "price": 1450000.0,
        "badge": "Top Gamut",
        "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Máxima potencia gráfica Ada Lovelace con disipador térmico de 3.5 ranuras y ventiladores Axial-tech.",
        "full_desc": "La ASUS ROG Strix GeForce RTX 4080 SUPER 16GB ofrece rendimiento extremo para renderizado 3D y juegos en 4K nativo. Equipada con camara de vapor patentada, estructura exoesqueleto de aluminio fundido y fases de alimentación de grado militar.",
        "specs_json": json.dumps(["VRAM: 16GB GDDR6X", "Bus: 256-bit", "Reloj OC: 2580 MHz", "Recomendado: Fuente 750W+", "Garantía: 36 Meses"]),
        "stock": 8
    },
    {
        "title": "Placa de Video NVIDIA GeForce RTX 4070 Super 12GB",
        "category": "hardware",
        "type": "producto",
        "price": 789990.0,
        "badge": "Top Ventas",
        "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Potencia gráfica de última generación para juegos en 1440p y 4K con Ray Tracing y DLSS 3.5.",
        "full_desc": "La NVIDIA GeForce RTX 4070 Super ofrece el rendimiento equilibrado que los jugadores y creadores necesitan. Experimenta trazado de rayos ultrarrápido y aceleración por IA en tus juegos favoritos.",
        "specs_json": json.dumps(["VRAM: 12GB GDDR6X", "Bus: 192-bit", "Recomendado: Fuente 650W+", "Garantía: 24 Meses"]),
        "stock": 15
    },
    {
        "title": "Placa de Video Gigabyte Radeon RX 7900 XT Gaming OC 20GB",
        "category": "hardware",
        "type": "producto",
        "price": 1150000.0,
        "badge": "AMD Flagship",
        "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Arquitectura AMD RDNA 3 con 20GB GDDR6 para gaming extremo en alta resolución.",
        "full_desc": "Diseñada para creadores y entusiastas del gaming. La Gigabyte Radeon RX 7900 XT integra el sistema de refrigeración WINDFORCE 3X con ventiladores alternados y placa trasera metálica protectora.",
        "specs_json": json.dumps(["VRAM: 20GB GDDR6", "Bus: 320-bit", "DisplayPort 2.1 Supported", "Recomendado: Fuente 750W+", "Garantía: 36 Meses"]),
        "stock": 6
    },
    {
        "title": "Procesador AMD Ryzen 7 7800X3D 5.0GHz Turbo AM5",
        "category": "hardware",
        "type": "producto",
        "price": 549000.0,
        "badge": "El Rey del Gaming",
        "image": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=600&q=80",
        "short_desc": "El procesador de gaming más rápido del mundo gracias a la tecnología 3D V-Cache de 96MB.",
        "full_desc": "Construido en la arquitectura Zen 4 y socket AM5. El AMD Ryzen 7 7800X3D ofrece tasas de cuadros por segundo insuperables en eSports y títulos AAA sin elevar la temperatura del sistema.",
        "specs_json": json.dumps(["Núcleos: 8 (16 Threads)", "Frecuencia Turbo: 5.0 GHz", "Caché L3: 96MB 3D V-Cache", "Socket: AM5 (DDR5)", "TDP: 120W"]),
        "stock": 12
    },
    {
        "title": "Procesador Intel Core i7-14700K 20 Cores LGA1700",
        "category": "hardware",
        "type": "producto",
        "price": 519000.0,
        "badge": "High Performance",
        "image": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=600&q=80",
        "short_desc": "20 núcleos (8 P-Cores + 12 E-Cores) hasta 5.6 GHz para multitarea extrema y streaming.",
        "full_desc": "Procesador Intel Core i7 de 14a Generación desbloqueado para overclocking. Maximiza el rendimiento en edición de video 4K, producción musical y juegos multitarea sin cuellos de botella.",
        "specs_json": json.dumps(["Núcleos: 20 (28 Threads)", "Frecuencia Turbo: 5.6 GHz", "Socket: LGA1700", "Desbloqueado para Overclock"]),
        "stock": 18
    },
    {
        "title": "Procesador AMD Ryzen 5 7600X 6-Core 5.3GHz Turbo",
        "category": "hardware",
        "type": "producto",
        "price": 289000.0,
        "badge": "Excelente Calidad/Precio",
        "image": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=600&q=80",
        "short_desc": "6 núcleos y 12 hilos con arquitectura Zen 4 para dar el salto a la plataforma DDR5 AM5.",
        "full_desc": "El punto de partida ideal para una PC Gamer moderna. Ofrece un rendimiento mono-núcleo excepcional para juegos competitivos con soporte PCIe 5.0.",
        "specs_json": json.dumps(["Núcleos: 6 (12 Threads)", "Frecuencia Turbo: 5.3 GHz", "Caché Total: 38MB", "Socket: AM5"]),
        "stock": 25
    },
    {
        "title": "Motherboard ASUS ROG Maximus Z790 Hero WiFi LGA1700",
        "category": "hardware",
        "type": "producto",
        "price": 890000.0,
        "badge": "Premium Enthusiast",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Placa madre Z790 de nivel entusiasta con 20+1 fases de poder, PCIe 5.0 y Wi-Fi 6E integrados.",
        "full_desc": "Diseñada para llevar procesadores Intel Core i9 e i7 a su límite absoluto. Incluye pantalla Polymo Lighting, puertos Thunderbolt 4 y soporte para hasta 5 SSDs M.2 NVMe.",
        "specs_json": json.dumps(["Socket: LGA1700", "Memoria: DDR5 Dual Channel", "Puertos: Thunderbolt 4", "Red: 2.5G LAN + Wi-Fi 6E"]),
        "stock": 5
    },
    {
        "title": "Motherboard MSI MAG B650 Tomahawk WiFi AM5",
        "category": "hardware",
        "type": "producto",
        "price": 310000.0,
        "badge": "Recomendado AM5",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Construcción robusta para procesadores Ryzen Serie 7000/8000 con disipación extendida.",
        "full_desc": "La serie MAG lucha junto a los gamers por el honor. Con la incorporación de elementos de estilo militar, estas placas ofrecen durabilidad incondicional y estabilidad de voltajes.",
        "specs_json": json.dumps(["Socket: AM5", "Memoria: DDR5 6600+MHz (OC)", "M.2 Slots: 3x PCIe 4.0", "Wi-Fi: Wi-Fi 6E + Bluetooth 5.3"]),
        "stock": 14
    },
    {
        "title": "Memoria RAM Corsair Vengeance RGB DDR5 32GB (2x16GB) 6000MHz CL30",
        "category": "hardware",
        "type": "producto",
        "price": 195000.0,
        "badge": "RGB & Low Latency",
        "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Kit de memoria ultrarrápida optimizada con perfiles AMD EXPO e Intel XMP 3.0.",
        "full_desc": "Optimiza tu sistema con las memorias Corsair Vengeance RGB DDR5. Ofrece frecuencias altas y latencias bajísimas (CL30) acompañadas de iluminación RGB dinámica direccionable de 10 zonas.",
        "specs_json": json.dumps(["Capacidad: 32GB (2x16GB)", "Frecuencia: 6000 MHz", "Latencia: CL30-36-36-76", "Perfil: Intel XMP / AMD EXPO"]),
        "stock": 20
    },
    {
        "title": "Memoria RAM Kingston FURY Beast DDR4 16GB (2x8GB) 3200MHz",
        "category": "hardware",
        "type": "producto",
        "price": 62000.0,
        "badge": "Best Seller DDR4",
        "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Actualización automática de Plug N Play y perfil bajo para disipadores de CPU grandes.",
        "full_desc": "Kingston FURY Beast DDR4 proporciona un gran aumento de rendimiento para juegos, edición de video y renderizado con velocidades de hasta 3200MHz.",
        "specs_json": json.dumps(["Capacidad: 16GB (2x8GB)", "Velocidad: 3200 MHz", "Voltaje: 1.35V", "Garantía: De por vida"]),
        "stock": 40
    },
    {
        "title": "SSD NVMe M.2 Samsung 990 PRO 2TB PCIe 4.0",
        "category": "hardware",
        "type": "producto",
        "price": 275000.0,
        "badge": "Velocidad Extrema",
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Hasta 7.450 MB/s de lectura secuencial para tiempos de carga inexistentes.",
        "full_desc": "Logra el máximo rendimiento en lectura y escritura con la tecnología V-NAND de Samsung. Diseñado para gamers empedernidos, editores de video 8K y cargas de trabajo masivas.",
        "specs_json": json.dumps(["Capacidad: 2TB", "Lectura: 7.450 MB/s", "Escritura: 6.900 MB/s", "Factor de forma: M.2 2280 NVMe"]),
        "stock": 15
    },
    {
        "title": "SSD NVMe M.2 Kingston NV2 1TB PCIe 4.0",
        "category": "hardware",
        "type": "producto",
        "price": 84000.0,
        "badge": "Económico & Rápido",
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Solución de almacenamiento de última generación impulsada por un controlador NVMe Gen 4x4.",
        "full_desc": "Kingston NV2 es una solución eficiente que ofrece velocidades de lectura/escritura de hasta 3.500/2.100 MB/s con un consumo de energía significativamente menor.",
        "specs_json": json.dumps(["Capacidad: 1TB", "Interface: PCIe 4.0 x4", "Lectura: 3.500 MB/s", "Garantía: 3 Años"]),
        "stock": 35
    },
    {
        "title": "Fuente de Poder Corsair RM1000x 1000W 80 Plus Gold Modular",
        "category": "hardware",
        "type": "producto",
        "price": 289000.0,
        "badge": "Certificación 80+ Gold",
        "image": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Alimentación continua con eficiencia 80 PLUS Gold y cables totalmente modulares.",
        "full_desc": "Las fuentes de alimentación de la serie Corsair RMx están construidas con componentes de la más alta calidad, incluidos condensadores japoneses de 105°C para garantizar potencia limpia y estable.",
        "specs_json": json.dumps(["Potencia: 1000 Watts", "Certificación: 80 PLUS Gold", "Cableado: Full Modular", "Garantía: 10 Años"]),
        "stock": 10
    },
    {
        "title": "Fuente de Poder EVGA 750W 80 Plus Bronze Semi-Modular",
        "category": "hardware",
        "type": "producto",
        "price": 125000.0,
        "badge": "Confianza EVGA",
        "image": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Potencia robusta y confiable para placas de video de gama media-alta como RTX 4070.",
        "full_desc": "La fuente EVGA 750W Bronze ofrece un rendimiento constante y protecciones eléctricas avanzadas (OVP, UVP, OCP, OPP, SCP) para salvaguardar todos los componentes de tu setup.",
        "specs_json": json.dumps(["Potencia: 750 Watts", "Certificación: 80 PLUS Bronze", "Formato: ATX", "Protecciones: Completas"]),
        "stock": 22
    },
    {
        "title": "Gabinete Gamer NZXT H9 Flow RGB Dual-Chamber",
        "category": "hardware",
        "type": "producto",
        "price": 295000.0,
        "badge": "Diseño Panorámico",
        "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Diseño de doble cámara con cristal templado continuo panorámico y ventiladores RGB.",
        "full_desc": "El NZXT H9 Flow está diseñado para refrigerar GPUs de alta gama gracias a sus capacidades térmicas masivas y capacidad de alojamiento para radiadores de hasta 360mm.",
        "specs_json": json.dumps(["Paneles: Cristal Templado Frontal/Lateral", "Soporte Radiador: Hasta 360mm", "Ventiladores: 4x Fans RGB Incluidos"]),
        "stock": 7
    },
    {
        "title": "Gabinete Corsair 4000D Airflow Mid-Tower",
        "category": "hardware",
        "type": "producto",
        "price": 149000.0,
        "badge": "Flujo de Aire Óptimo",
        "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Panel frontal optimizado de alto flujo de aire y enrutamiento de cables RapidRoute.",
        "full_desc": "El Corsair 4000D Airflow combina canalización oculta de cables y un diseño frontal perforado para mantener tus temperaturas bajo control aun en sesiones de juego intensas.",
        "specs_json": json.dumps(["Factor de Forma: Mid-Tower ATX", "Panel Lateral: Cristal Templado", "Incluye: 2x Fans 120mm AirGuide"]),
        "stock": 16
    },
    {
        "title": "Watercooler Corsair iCUE H150i Elite LCD XT 360mm ARGB",
        "category": "hardware",
        "type": "producto",
        "price": 380000.0,
        "badge": "Pantalla IPS Personalizable",
        "image": "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Refrigeración líquida AIO de 360mm con pantalla LCD IPS personalizada de 2.1 pulgadas.",
        "full_desc": "Muestra las temperaturas de tu CPU en tiempo real, GIFs animados o logos de tu equipo con la pantalla LCD integrada de 480x480 píxeles y ventiladores AF RGB ELITE ultrasilenciosos.",
        "specs_json": json.dumps(["Radiador: 360mm", "Pantalla: LCD IPS 480x480 30FPS", "Fans: 3x Corsair AF120 RGB ELITE"]),
        "stock": 9
    },
    {
        "title": "Cooler CPU DeepCool AK620 Digital Dual-Tower",
        "category": "hardware",
        "type": "producto",
        "price": 110000.0,
        "badge": "Air Cooling Top Performance",
        "image": "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Disipador de doble torre de aire con pantalla digital de monitoreo de temperatura en tiempo real.",
        "full_desc": "Logra el máximo rendimiento de refrigeración por aire para CPUs Ryzen 7 e Intel i7. Equipado con 6 tubos de calor de cobre y ventiladores FDB silenciosos de alta presión estática.",
        "specs_json": json.dumps(["Disipación TDP: Hasta 260W", "Pantalla: Temperatura y Uso de CPU", "Compatibilidad: AM5 / LGA1700"]),
        "stock": 18
    },
    {
        "title": "Monitor Gamer ASUS ROG Swift 27\" 240Hz QHD OLED 0.03ms",
        "category": "hardware",
        "type": "producto",
        "price": 1690000.0,
        "badge": "Pantalla OLED 240Hz",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Panel OLED 1440p de 240Hz con tiempo de respuesta ultra-rápido de 0.03ms y contraste infinito.",
        "full_desc": "Experimenta la máxima inmersión visual. El monitor ROG Swift PG27AQDM incorpora tecnología OLED de tercera generación, recubrimiento antirreflejos y disipador térmico personalizado sin ventilador.",
        "specs_json": json.dumps(["Pantalla: 27 OLED QHD (2560x1440)", "Refresco: 240 Hz", "Respuesta: 0.03 ms GTG", "HDR: HDR10 / 1000 nits"]),
        "stock": 4
    },
    {
        "title": "Monitor Gamer Samsung Odyssey G5 27\" 165Hz QHD Curvo",
        "category": "hardware",
        "type": "producto",
        "price": 420000.0,
        "badge": "Curvatura 1000R",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Pantalla curva 1000R resolución WQHD con frecuencia de actualización de 165Hz y AMD FreeSync Premium.",
        "full_desc": "Llena tu visión periférica y sumérgete en el campo de batalla. La curvatura 1000R coincide exactamente con la curvatura del ojo humano para reducir la fatiga visual.",
        "specs_json": json.dumps(["Pantalla: 27 Curva VA WQHD", "Refresco: 165 Hz", "Respuesta: 1 ms MPTR", "Sincronización: AMD FreeSync Premium"]),
        "stock": 11
    },
    {
        "title": "Teclado Mecánico Custom Keychron Q1 Pro Wireless RGB Hot-Swap",
        "category": "hardware",
        "type": "producto",
        "price": 260000.0,
        "badge": "Aluminio CNC Custom",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Teclado mecánico inalambrico 75% construido en aluminio mecanizado CNC con diseño Gasket Mount.",
        "full_desc": "El Keychron Q1 Pro es un teclado mecánico premium personalizable. Compatible con VIA/QMK, interruptores intercambiables en caliente (Hot-Swap) y conexión Bluetooth 5.1 multidispositivo.",
        "specs_json": json.dumps(["Cuerpo: Aluminio Mecanizado CNC", "Formato: 75% Layout", "Conectividad: Bluetooth 5.1 / Cable USB-C", "Switches: Keychron K Pro Red"]),
        "stock": 10
    },
    {
        "title": "Mouse Gamer Inalámbrico Logitech G Pro X Superlight 2 (60g)",
        "category": "hardware",
        "type": "producto",
        "price": 185000.0,
        "badge": "eSports Choice",
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=600&q=80",
        "short_desc": "El ícono eSports evolucionado: 60g de peso ultra liviano, sensor HERO 2 e interruptores híbridos LIGHTFORCE.",
        "full_desc": "Diseñado en colaboración con los mejores jugadores profesionales de eSports del mundo. Equipado con tecnología inalámbrica LIGHTSPEED de grado de competición y hasta 95 horas de batería.",
        "specs_json": json.dumps(["Peso: 60 gramos", "Sensor: HERO 2 (32.000 DPI)", "Tasa de Sondeo: 2000Hz Polling Rate", "Carga: USB-C / POWERPLAY"]),
        "stock": 25
    },
    {
        "title": "Auriculares Gamer Inalámbricos HyperX Cloud III Wireless 7.1",
        "category": "hardware",
        "type": "producto",
        "price": 179000.0,
        "badge": "120h de Batería",
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Comodidad legendaria de HyperX con hasta 120 horas de batería y audio espacial DTS Headphone:X 3D.",
        "full_desc": "Escucha cada detalle de tus enemigos. Los Cloud III Wireless incorporan controladores angulados de 53mm sintonizados para una respuesta de graves enriquecida y micrófono con cancelación de ruido.",
        "specs_json": json.dumps(["Autonomía: Hasta 120 Horas", "Drivers: 53mm Neodimio", "Conexión: Inalámbrica 2.4 GHz", "Estructura: Aluminio Duradero"]),
        "stock": 14
    },
    {
        "title": "Notebook Gamer ASUS ROG Strix G16 (2024) i9 RTX 4070",
        "category": "notebooks",
        "type": "producto",
        "price": 2490000.0,
        "badge": "Pantalla ROG Nebula 240Hz",
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Pantalla 16 QHD+ 240Hz, Intel Core i9-13980HX de 24 Núcleos, 32GB DDR5 y RTX 4070 8GB.",
        "full_desc": "Laptop gamer de máxima categoría. Domina los torneos con refrigeración de metal líquido Tri-Fan ROG Intelligent Cooling y MUX Switch dedicado con NVIDIA Advanced Optimus.",
        "specs_json": json.dumps(["Procesador: Intel i9-13980HX (24 Cores)", "RAM: 32GB DDR5 4800MHz", "Almacenamiento: 1TB SSD NVMe PCIe 4.0", "GPU: RTX 4070 8GB (140W WGP)"]),
        "stock": 5
    },
    {
        "title": "Notebook Gamer Lenovo Legion Pro 5 Gen 8 Ryzen 7 RTX 4060",
        "category": "notebooks",
        "type": "producto",
        "price": 1890000.0,
        "badge": "Excelente Chasis & Pantalla",
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80",
        "short_desc": "AMD Ryzen 7 7745HX, 16GB RAM DDR5, SSD 1TB y pantalla PureSight 16 IPS 165Hz.",
        "full_desc": "Lenovo Legion Pro 5 te da la ventaja competitiva impulsada por el chip de IA Lenovo LA1. Disfruta de teclados TrueStrike táctiles precisos y refrigeración Legion ColdFront 5.0.",
        "specs_json": json.dumps(["CPU: AMD Ryzen 7 7745HX", "RAM: 16GB DDR5 5200MHz", "Pantalla: 16 WQXGA (2560x1600) 165Hz", "GPU: NVIDIA RTX 4060 8GB"]),
        "stock": 7
    },
    {
        "title": "Licencia Digital Microsoft Windows 11 Pro Vitalicia Retail",
        "category": "software",
        "type": "producto",
        "price": 24990.0,
        "badge": "Entrega Inmediata",
        "image": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Clave de activación digital oficial y vitalicia para 1 PC con soporte de actualizaciones oficiales.",
        "full_desc": "Licencia original Microsoft Windows 11 Professional. Válida para reactivaciones en el mismo equipo. Incluye encriptación BitLocker, escritorio remoto y características avanzadas de seguridad empresarial.",
        "specs_json": json.dumps(["Tipo: Clave Retail Vitalicia", "Envío: Correo Electrónico Inmediato", "Arquitectura: 64-bit", "Soporte Oficial Microsoft"]),
        "stock": 100
    },

    # ==========================================
    # SERVICIOS DIGITALES & TALLER (4 ÍTEMS)
    # ==========================================
    {
        "title": "Servicio de Armado Profesional y Testeo de PC Gamer a Medida",
        "category": "servicios",
        "type": "servicio",
        "price": 35000.0,
        "badge": "Servicio Técnico Oficial",
        "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Ensamble profesional, ordenamiento estético de cables (Cable Management) y pruebas de estabilidad Stress Test 2h.",
        "full_desc": "Deja el armado de tu nueva computadora en manos de expertos. Incluye montaje cuidadoso de componentes, canalización oculta de cables para óptimo flujo de aire, actualización de BIOS a la última versión y prueba de temperatura bajo carga extrema por 2 horas.",
        "specs_json": json.dumps(["Tiempo de Entrega: 24 a 48 hs", "Prueba de Estrés: FurMark + Cinebench", "Actualización de BIOS incluida", "Garantía de Ensamble: 6 Meses"]),
        "stock": 50
    },
    {
        "title": "Servicio de Mantenimiento Preventivo, Limpieza Ultrasónica y Pasta Térmica Premium",
        "category": "servicios",
        "type": "servicio",
        "price": 28000.0,
        "badge": "Mantenimiento Taller",
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Limpieza profunda de polvo, cambio de pasta térmica de alta conductividad (Arctic MX-4) y optimización de S.O.",
        "full_desc": "Servicio recomendado cada 6 a 12 meses para prevenir sobrecalentamientos y extender la vida útil de tus componentes gamer. Incluye desarme completo de placa de video y CPU, limpieza de disipadores, reemplazo de thermal pads desgastados e informe de temperaturas antes/después.",
        "specs_json": json.dumps(["Pasta Térmica: Arctic MX-4 / Thermal Grizzly", "Limpieza de Fans y Radiadores", "Optimización de Inicio de Windows", "Informe de Temperaturas Antes/Después"]),
        "stock": 50
    },
    {
        "title": "Servicio de Optimización Avanzada de S.O., Drivers, Overclock Seguro & Tuning BIOS",
        "category": "servicios",
        "type": "servicio",
        "price": 22000.0,
        "badge": "Tuning & FPS Boost",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Ajuste fino del sistema operativo para eliminar latencia de entrada (Input Lag) y exprimir máximos FPS.",
        "full_desc": "Optimización técnica especializada para jugadores competitivos de eSports. Configuración de latencias de memoria RAM XMP/EXPO, undervolting de procesador y placa de video para menores temperaturas y mayores frecuencias sostenidas.",
        "specs_json": json.dumps(["Inclusión: Calibración XMP / EXPO", "Undervolting Seguro GPU & CPU", "Desactivación de Telemetría Basura", "Reducción de Latencia de Entrada"]),
        "stock": 50
    },
    {
        "title": "Servicio de Diagnóstico Técnico de Hardware, Reparación & Banco de Pruebas",
        "category": "servicios",
        "type": "servicio",
        "price": 18000.0,
        "badge": "Diagnóstico de Taller",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80",
        "short_desc": "Detección exacta de fallas, pantallas azules (BSOD), reinicios inesperados y problemas de encendido.",
        "full_desc": "Testeo individual de componentes en banco de pruebas (Memtest86 para RAM, verificador de voltajes en fuentes, escaneo de sectores defectuosos en SSDs). El costo del diagnóstico se bonifica si se realiza la reparación en nuestro taller.",
        "specs_json": json.dumps(["Diagnóstico: 24 a 48 hs", "Pruebas: MemTest86 + Osciloscopio Fuente", "Bonificable con el costo de reparación", "Informe Escrito de Falla"]),
        "stock": 50
    }
]


def seed_database():
    """Puebla la base de datos con los 30 productos y servicios reales de JMSHOP."""
    init_db()
    with Session(engine) as session:
        # 1. Crear Usuario Admin
        admin = session.exec(select(User).where(User.email == "admin@jmshop.com")).first()
        if not admin:
            admin_user = User(
                email="admin@jmshop.com",
                full_name="JMSHOP Administrator",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_admin=True
            )
            session.add(admin_user)
            print("[INFO] Usuario Administrador creado: admin@jmshop.com / admin123")

        # 2. Crear Usuario Cliente de prueba
        client_user = session.exec(select(User).where(User.email == "cliente@jmshop.com")).first()
        if not client_user:
            demo_user = User(
                email="cliente@jmshop.com",
                full_name="Cliente JMSHOP",
                hashed_password=get_password_hash("cliente123"),
                is_active=True,
                is_admin=False
            )
            session.add(demo_user)
            print("[INFO] Usuario Cliente de prueba creado: cliente@jmshop.com / cliente123")

        # 3. Limpiar y re-sembrar los 30 productos para coherencia total
        session.exec(delete(Product))
        session.commit()

        for item in INITIAL_PRODUCTS:
            prod = Product(**item)
            session.add(prod)
        
        session.commit()
        print(f"[SUCCESS] Se han sembrado exitosamente {len(INITIAL_PRODUCTS)} productos y servicios en SQLite 3 (26 Hardware + 4 Servicios Digitales).")


if __name__ == "__main__":
    seed_database()
