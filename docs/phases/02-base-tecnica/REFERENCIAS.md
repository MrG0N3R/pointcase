# Referencias técnicas de la Fase 02

Consultadas el 28 de octubre de 2026. Las versiones instaladas están fijadas en los archivos de dependencias; las páginas de documentación pueden actualizarse.

- La construcción web usa el flujo de desarrollo/compilación descrito por [Vite](https://vite.dev/guide/). Versiones exactas de React, TypeScript, Vite y su plugin en `package-lock.json`.
- La API libera su pool al finalizar mediante lifespan, según [FastAPI](https://fastapi.tiangolo.com/advanced/events/). Su contenedor usa la forma exec para el arranque, siguiendo [FastAPI en Docker](https://fastapi.tiangolo.com/deployment/docker/).
- Las conexiones usan el dialecto [PostgreSQL/psycopg de SQLAlchemy](https://docs.sqlalchemy.org/en/21/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg). Las migraciones siguen el [entorno de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html).
- Compose declara salud y dependencias de migración según [el orden de arranque de Docker](https://docs.docker.com/compose/how-tos/startup-order/). El archivo está preparado; el arranque con Docker no se ha ejecutado localmente.
- Los respaldos usan pg_dump/pg_restore conforme a [PostgreSQL 18](https://www.postgresql.org/docs/18/backup-dump.html); la inicialización de contenedor obtiene la contraseña desde el entorno mediante [psql getenv](https://www.postgresql.org/docs/18/app-psql.html).

Verificación de versiones: metadatos de los registros oficiales npm y PyPI, resolución/instalación y posterior instalación limpia de los requisitos fijados. No se instalaron dependencias globales ni proveedores de pago/facturación.
