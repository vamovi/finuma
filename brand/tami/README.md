# Lettering de tami (exploración)

Tres direcciones de logotipo tipográfico en minúsculas para "tami" (contexto: Tamibrief.md, mismo negocio que Finuma). El gesto está en una o dos letras y no hay símbolo aparte ni dibujos añadidos.

| Dirección | Archivo | Gesto | A vigilar |
|---|---|---|---|
| 1 · Puente | `puente.png` | El travesaño de la t se prolonga y se convierte en el techo de la a: dos letras que se encuentran a mitad de camino. | La a con techo plano necesita ajuste óptico para que no pese más que la m. |
| 2 · Ritmo | `ritmo.png` | La a y los arcos de la m comparten la misma curva; el punto de la i es el único acento coral. | El punto de color es un recurso muy visto; coral sobre blanco tiene poco contraste (2,7:1) a tamaños pequeños. |
| 3 · Eco | `eco.png` | La t y la i terminan con el mismo gancho: la palabra empieza y acaba con el mismo gesto. | Muy legible, pero el avatar con la i sola dentro de un círculo se confunde con el icono universal de "información". |

## Paleta (solo estos tres colores)

- Verde oscuro `#173A2B`
- Coral `#F27B75`
- Blanco `#FFFFFF`

Contraste: blanco sobre verde 12,5:1; verde sobre coral 4,7:1; blanco sobre coral 2,7:1 (no usar para texto).
Variables en `styles/tami.css`.

## Importante

Las imágenes son **propuestas conceptuales** generadas con la API de imágenes de OpenAI (`scripts/generar_lettering_tami.py`). No son una fuente comercial. El logotipo elegido necesitará **dibujo vectorial y ajuste óptico** antes de su entrega final. El brand kit completo se desarrollará después de elegir dirección.

**Elegida: Ritmo.** El brand kit está en `kit/`.
