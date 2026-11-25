# Arquitectura de shelf

`shelf` es una CLI en Python 3.10+, solo con la biblioteca estándar. Cada comando pasa por las mismas cinco capas:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Entrada | `shelf/__main__.py` | Ejecuta `main()` y convierte su resultado en el código de salida. |
| CLI | `shelf/cli.py` | Construye el parser, despacha al handler y traduce `ShelfError` a código 1. |
| Comandos | `shelf/commands/*.py` | Un módulo por comando; cada uno define `register` y `run`. |
| Persistencia | `shelf/store.py` | Lee y escribe el archivo JSON de la estantería. |
| Modelo | `shelf/models.py` | `Book`, los estados válidos y las marcas de tiempo en UTC. |

## De un comando al archivo

```mermaid
flowchart TD
    A["python -m shelf COMANDO args<br/>shelf/__main__.py:5"] --> B["main(argv)<br/>shelf/cli.py:25"]
    B --> C["build_parser()<br/>shelf/cli.py:12"]
    C --> D["commands.register_all(subparsers)<br/>shelf/cli.py:21"]
    D --> E["Descubre y ordena los módulos de shelf/commands/<br/>shelf/commands/__init__.py:19"]
    E --> F["module.register(subparsers): add_parser + set_defaults(handler=run)<br/>shelf/commands/__init__.py:21"]
    F --> G["parse_args(argv)<br/>shelf/cli.py:31"]
    G -->|"uso inválido"| X2["argparse: SystemExit(2)"]
    G --> H["Store(): ruta = $SHELF_PATH o ~/.shelf.json<br/>shelf/cli.py:33 · shelf/store.py:28-31, 35-36"]
    H --> I["args.handler(args, store)<br/>shelf/cli.py:33"]
    I --> J["Store.load()<br/>shelf/store.py:38-42"]
    J -->|"el archivo no existe"| J0["lista vacía<br/>shelf/store.py:39-40"]
    J -->|"existe"| J1["json.loads + Book.from_dict<br/>shelf/store.py:41-42 · shelf/models.py:33-35"]
    J0 --> K{"¿El comando modifica?"}
    J1 --> K
    K -->|"no: list, search"| P["print(...) y return 0"]
    K -->|"sí: add, start, finish"| L["Book.move_to(status)<br/>shelf/models.py:25-28"]
    L --> M["Store.save(books)<br/>shelf/store.py:44-50"]
    M --> N["Escribe .tmp y lo cambia por el archivo<br/>shelf/store.py:48-50"]
    N --> P
    I -->|"ShelfError, p. ej. BookNotFound"| X1["shelf: error: ... por stderr, return 1<br/>shelf/cli.py:34-36"]
    P --> Z["raise SystemExit(código)<br/>shelf/__main__.py:5"]
    X1 --> Z
```

Los comandos se descubren con `pkgutil.iter_modules`. Para añadir un comando basta con crear un archivo en `shelf/commands/`; no hay que editar ninguna lista compartida (`shelf/commands/__init__.py:7-9`).

## Secuencia de `shelf finish ID`

```mermaid
sequenceDiagram
    actor U as Usuario
    participant Main as __main__.py
    participant CLI as cli.py
    participant Cmds as commands/__init__.py
    participant Prog as commands/progress.py
    participant Store as store.py
    participant Book as models.py (Book)
    participant FS as Archivo JSON

    U->>Main: python -m shelf finish 1
    Main->>CLI: main() (__main__.py:5)
    CLI->>Cmds: register_all(subparsers) (cli.py:21)
    Cmds->>Prog: register(subparsers) (__init__.py:21)
    Note over Prog: Registra "start" y "finish" desde TRANSITIONS (progress.py:10-13, 16-20). finish: status="done", verb="Finished"
    CLI->>CLI: parse_args → id=1, status="done", handler=run (cli.py:31)
    CLI->>Store: Store() → default_path() (cli.py:33, store.py:28-31)
    CLI->>Prog: run(args, store) (cli.py:33, progress.py:23)
    Prog->>Store: move(1, "done") (progress.py:24)
    Store->>FS: load(): read_text (store.py:38-42)
    FS-->>Store: lista JSON
    Store->>Book: Book.from_dict(record) (models.py:33-35)
    Store->>Store: find(books, 1) (store.py:63, 69-73)
    alt No existe el id
        Store-->>CLI: raise BookNotFound (store.py:73)
        CLI-->>U: "shelf: error: no book with id 1" por stderr, código 1 (cli.py:34-36)
    else Existe
        Store->>Book: move_to("done") (store.py:64)
        Book->>Book: status="done", finished_at=now() en UTC (models.py:27-28, 11-13)
        Store->>FS: save(): escribe .tmp y lo cambia por el archivo (store.py:65, 44-50)
        Store-->>Prog: book
        Prog-->>U: "Finished #1 [done] Dune by Frank Herbert" (progress.py:25)
        Prog-->>CLI: 0 (progress.py:26)
        CLI-->>Main: 0
        Main-->>U: SystemExit(0) (__main__.py:5)
    end
```

Cada `finish` sobrescribe `finished_at` con la hora actual, aunque el libro ya estuviera en `done`. Pasar a otro estado lo deja en `None` (`shelf/models.py:28`).
