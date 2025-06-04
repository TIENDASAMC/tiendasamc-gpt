# tiendasamc-gpt
Repositorio para automatización de respuestas en Instagram con IA

## Obtener comentarios de Instagram

El script `get_instagram_comments.py` permite consultar los comentarios más recientes de una cuenta de Instagram mediante el Graph API de Meta.

Uso básico:

```bash
python get_instagram_comments.py PAGE_ID ACCESS_TOKEN
```

Donde:
- `PAGE_ID` es el identificador de la página de Facebook asociada a la cuenta de Instagram.
- `ACCESS_TOKEN` es un token de acceso con permisos para leer la información de la página y los comentarios de Instagram.

Opcionalmente se puede especificar `--limit` para indicar cuántas publicaciones recientes revisar (por defecto 25).

El script muestra los comentarios ordenados por fecha, indicando usuario, texto y el `media_id` de la publicación a la que pertenecen.
