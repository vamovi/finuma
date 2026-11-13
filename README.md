# Finuma

Financiación de inversiones productivas a partir del conocimiento de cada negocio. Primer producto: máquinas de ordeño.

## Marca

- `styles/finuma.css`: colores de marca como variables CSS.
- `brand/paleta.svg`: paleta de colores.
- `brand/board.png`: tablero de marca.
- `brand/logo/*.svg`: símbolo vectorial (coral, verde y línea). Dos ganchos iguales que se sostienen entre sí: confianza en doble vía.
- `brand/logo.png`: logo y variantes.
- `brand/aplicaciones.png`: aplicaciones (web, WhatsApp, volante, tarjetas, gorra, sticker).
- `scripts/generar_marca.py`: genera el tablero de marca y las aplicaciones a partir del logo con la API de imágenes de OpenAI. Lee `OPENAI_API_KEY` del entorno y guarda las imágenes en `brand/`.

```bash
export OPENAI_API_KEY=...   # o cárgala desde tu .env
python3 scripts/generar_marca.py            # tablero y aplicaciones
python3 scripts/generar_marca.py board      # solo uno
```

| Color | Hex | Uso |
|---|---|---|
| Verde | `#173A2B` | Titulares, botones, pie |
| Tinta | `#14281F` | Texto |
| Coral | `#F27B75` | Banda de acento |
| Coral intenso | `#EA6662` | Punto, barras de requisitos |
| Crema | `#F9F9F7` | Fondo |
| Línea | `#D9DBD6` | Separadores |

Tipografía: Outfit (Google Fonts, licencia OFL). Titulares 700, texto 400.
