# Brand kit de tami · Dirección Ritmo

Elegida por Valen entre las tres direcciones de `brand/tami/`.

## Logotipo

- `logo/tami-verde.svg`: principal, verde con punto coral, sobre blanco.
- `logo/tami-blanco-sobre-verde.svg`: blanco con punto coral, sobre verde.
- `logo/tami-verde-sobre-coral.svg`: todo verde sobre coral (nada blanco sobre coral).
- `logo/tami-monocromo.svg`: todo verde, para tamaños pequeños.
- `logo/tami-avatar.svg`: avatar "mi" blanco con punto coral en círculo verde (WhatsApp, redes, favicon).
- `logo.png`: lámina del logotipo.

Construcción (`scripts/dibujar_logo_tami.py`): trazo monolineal de 26 sobre altura x de 100, remates redondos. La a y los arcos de la m usan la misma curva (radio 37). "ami" es un solo trazo unido en la línea base, que expresa continuidad. El punto de la i es el único acento de color.

**Es un primer dibujo vectorial.** Antes de la entrega final necesita ajuste óptico de un diseñador: compensar grosor en las uniones de la línea base, sobreimpresión de curvas, peso del punto y espaciado entre t y a.

## Contraste del punto coral

El coral sobre blanco da 2,7:1. El punto es un acento gráfico del logotipo, no texto, así que:

- Sobre blanco, el punto va en coral solo cuando el logotipo mide 32 px de alto o más.
- Por debajo de 32 px (favicon, firmas, pies de documento), el logotipo va entero en verde.
- Sobre coral, el logotipo va entero en verde (verde sobre coral 4,7:1).
- Sobre verde, el punto coral funciona en cualquier tamaño (4,7:1).

## Paleta (`paleta.png`)

Verde `#173A2B`, Coral `#F27B75`, Blanco `#FFFFFF`. Nada más. Variables en `styles/tami.css`.

| Combinación | Contraste | Uso |
|---|---|---|
| Blanco sobre verde | 12,5:1 | Texto |
| Verde sobre coral | 4,7:1 | Texto |
| Coral sobre verde | 4,7:1 | Titulares grandes y punto |
| Blanco sobre coral | 2,7:1 | No usar |

Tipografía de apoyo: Outfit (OFL), semibold para titulares y regular para texto.

## Tablero y aplicaciones

`tablero.png` y `aplicaciones.png` se generaron con la API de imágenes de OpenAI (`scripts/generar_kit_tami.py`) usando `logo.png` como referencia. Son **propuestas conceptuales**: el logotipo dentro de ellas es una reproducción aproximada y las piezas finales deben montarse con los SVG.

A revisar en las imágenes:
- Las cifras son ficticias y no son coherentes con condiciones reales (en el tablero el total no cuadra con el valor del equipo; en el documento el total es igual al valor del equipo, como si no hubiera costo financiero).
- La tarjeta de presentación muestra un teléfono, correo y dominio (`tami.co`) inventados; no están verificados.
- La última cuota del tablero cae en 2028 (12 cuotas desde marzo de 2027).
- Las pantallas de WhatsApp e Instagram conservan colores propios de esas apps.
