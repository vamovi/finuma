# Finuma

Financiación de máquinas de ordeño para productores lecheros en Colombia.

## Marca

- `styles/finuma.css`: colores de marca como variables CSS.
- `brand/paleta.svg`: paleta de colores.
- `brand/board.png`: tablero de marca.
- `brand/logo.png`: logo y variantes.
- `brand/aplicaciones.png`: aplicaciones (web, WhatsApp, volante, tarjetas, gorra, sticker).
- `scripts/generar_marca.py`: genera el tablero de marca, el logo y las aplicaciones con la API de imágenes de OpenAI. Lee `OPENAI_API_KEY` del entorno y guarda las imágenes en `brand/`.

```bash
export OPENAI_API_KEY=...   # o cárgala desde tu .env
python3 scripts/generar_marca.py            # board, logo y aplicaciones
python3 scripts/generar_marca.py logo       # solo uno
```

| Color | Hex | Uso |
|---|---|---|
| Verde | `#173A2B` | Titulares, botones, pie |
| Tinta | `#14281F` | Texto |
| Coral | `#F27B75` | Banda de acento |
| Coral intenso | `#EA6662` | Punto, barras de requisitos |
| Crema | `#F9F9F7` | Fondo |
| Línea | `#D9DBD6` | Separadores |

Tipografía: sans geométrica tipo Outfit (por confirmar).
