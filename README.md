# AI Digital Office

Plataforma institucional de inteligencia artificial,
automatización de procesos, gestión de conocimiento,
soporte tecnológico y análisis empresarial.

## Objetivos

- Centralizar conocimiento institucional.
- Implementar asistentes de IA.
- Implementar agentes inteligentes.
- Automatizar procesos.
- Gestionar tickets de soporte TI.
- Crear dashboards empresariales.
- Generar reportes automáticos.
- Implementar control de acceso.
- Auditar el uso de IA.
- Aplicar principios de seguridad y gobierno de IA.

## Stack

- React
- FastAPI
- Python
- PostgreSQL
- pgvector
- OpenAI API
- n8n
- Firebase
- AWS
- Power BI
- Docker
- GitHub
- PyTorch (módulo ML opcional)

## Pasos para levantar entorno virtual (venv)

- cd backend
- python3 -m venv .venv
- source .venv/bin/activate

## Iniciar backend
- uvicorn app.main:app --reload

## Levantar docker

- cd ~/AI-Digital-Office
- touch docker-compose.yml
- configurar manifiesto del archivo
- docker compose up -d
- docker compose ps 

## Probar PostgreSQL de docker
- docker exec -it ai-digital-office-postgres psql -U ai_admin -d ai_digital_office
- SELECT version();


## alembic migracion
- alembic revision --autogenerate -m "add created_by to tickets"
- alembic upgrade head
- alembic check
- Si dice que no hay operaciones nuevas, la migración está sincronizada.

## roles
- employee
 ├── crear tickets
 ├── ver sus tickets
 └── modificar/eliminar sus tickets

- support
 ├── ver tickets
 ├── modificar tickets
 └── atender tickets

- admin
 └── acceso completo

 ## FRONTEND ARQUITECTURA
 frontend/
    ├── lib/
    │   ├── core/
    │   │   ├── api/
    │   │   ├── storage/
    │   │   └── constants/
    │   │
    │   ├── features/
    │   │   ├── auth/
    │   │   ├── dashboard/
    │   │   ├── tickets/
    │   │   ├── comments/
    │   │   └── notifications/
    │   │
    │   └── main.dart

## ROLES 
    employee
    ├── crear ticket
    ├── ver sus tickets
    ├── comentar
    └── ver notificaciones

    support
    ├── ver tickets
    ├── asignar
    ├── cambiar estado
    ├── comentar
    └── dashboard

    admin
    └── todo lo anterior

## TanStack Query
    Para manejar correctamente las peticiones, caché, loading, errores y actualización de datos:

## Comprueba que TypeScript no tenga errores
 - npm run build


 ## IA para clasificación automática de tickets
 Empleado
   │
   ▼
Crear ticket
   │
   ▼
FastAPI
   │
   ├── Guarda Ticket
   │
   ├── TicketHistory → "created"
   │
   └── IA
        │
        ├── Clasifica prioridad
        ├── Detecta categoría
        ├── Resume problema
        └── Sugiere respuesta