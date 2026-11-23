# Issues de práctica: ID del catálogo → número en GitHub

Las issues de práctica usan IDs de catálogo (S1–S7, C1, C2) que **no coinciden** con el número de la issue en GitHub. Los números #3, #4 y #5 son pull requests, no issues.

Por ejemplo, **S3 es la issue #6, no la #3**. Cuando alguien mencione una issue por su ID (por ejemplo «implementa S3»), busca su número en esta tabla antes de usar `gh issue view`, ramas o `Closes #N`.

Repositorio: [`PabloMonzonToca/shelf`](https://github.com/PabloMonzonToca/shelf)

| ID | Issue en GitHub | Título | Estado (2026-11-23) |
| --- | --- | --- | --- |
| S1 | [#1](https://github.com/PabloMonzonToca/shelf/issues/1) | S1: Filtrar shelf list por estado | Cerrada |
| S2 | [#2](https://github.com/PabloMonzonToca/shelf/issues/2) | S2: Buscar libros por título o autor | Cerrada |
| S3 | [#6](https://github.com/PabloMonzonToca/shelf/issues/6) | S3: Mostrar estadísticas de lectura | Abierta |
| S4 | [#7](https://github.com/PabloMonzonToca/shelf/issues/7) | S4: Exportar la estantería a CSV o Markdown | Abierta |
| S5 | [#8](https://github.com/PabloMonzonToca/shelf/issues/8) | S5: Eliminar un libro, con confirmación | Abierta |
| S6 | [#9](https://github.com/PabloMonzonToca/shelf/issues/9) | S6: Rechazar títulos vacíos y estados desconocidos | Abierta |
| C1 | [#10](https://github.com/PabloMonzonToca/shelf/issues/10) | C1: Etiquetar libros | Abierta |
| C2 | [#11](https://github.com/PabloMonzonToca/shelf/issues/11) | C2: Versionar el formato del archivo de la estantería | Abierta |
| S7 | [#12](https://github.com/PabloMonzonToca/shelf/issues/12) | S7: Hacer shelf más útil para clubes de lectura | Abierta |

El estado es el del día en que se escribió esta tabla. Para ver el estado actual, ejecuta:

```bash
gh issue list --state all
```

Cada título empieza por su ID, así que también puedes buscar una issue con `gh issue list --search "S3 in:title"`.
