# FCAAssets - Sistema de Gestión de Equipos y Mantenimiento

Sistema web basado en Django para gestionar equipos de laboratorio y registrar su historial de mantenimiento. Permite a los administradores monitorear el estado de los equipos, registrar mantenimientos y recibir notificaciones automáticas cuando el mantenimiento está próximo a vencer.

## 📋 Descripción General

FCAAssets es una aplicación web de gestión de activos diseñada para:

- **Inventariar equipos** de laboratorio con información detallada (número de serie, marca, tipo, ubicación)
- **Registrar mantenimientos** realizados con documentación fotográfica y archivos PDF
- **Monitorear el estado** de mantenimiento de cada equipo (Al día / Por vencer / Vencido)
- **Enviar notificaciones automáticas** por correo electrónico:
  - 30 días antes del vencimiento
  - 7 días antes del vencimiento
  - En la fecha de vencimiento
- **Generar reportes** del estado actual de todos los equipos

## 🛠️ Stack Tecnológico

- **Backend:** Django 5.2.8
- **Base de datos:** SQLite3
- **Servidor:** WSGI/ASGI compatible
- **Scheduler:** APScheduler 3.11.1 (tareas programadas)
- **Procesamiento de imágenes:** Pillow 12.0.0
- **Gestión de zonas horarias:** tzdata, tzlocal

### Dependencias principales

```
Django==5.2.8
APScheduler==3.11.1
django-crontab==0.7.1
Pillow==12.0.0
asgiref==3.10.0
sqlparse==0.5.3
```

## 📁 Estructura del Proyecto

```
FCAAssets/
├── FCAAssets/              # Configuración principal de Django
│   ├── settings.py         # Configuración de la aplicación
│   ├── urls.py             # Rutas principales
│   ├── wsgi.py             # Configuración WSGI
│   └── asgi.py             # Configuración ASGI
├── storage/                # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica de negocio
│   ├── forms.py            # Formularios
│   ├── urls.py             # Rutas de la aplicación
│   ├── admin.py            # Configuración del admin
│   ├── scheduler.py        # Tareas programadas
│   ├── utils/              # Utilidades
│   │   ├── email.py        # Envío de correos
│   │   ├── check_maintenance_necessary.py
│   │   ├── update_upcoming_maintenance.py
│   │   └── validation_file.py
│   ├── static/             # Archivos estáticos
│   ├── templates/          # Plantillas HTML
│   └── migrations/         # Migraciones de BD
├── templates/              # Plantillas globales
│   ├── base.html
│   ├── header.html
│   ├── footer.html
│   ├── registration/       # Plantillas de autenticación
│   └── storage/            # Plantillas específicas
├── static/                 # Archivos CSS y estáticos
├── uploads/                # Archivos subidos por usuarios
├── manage.py               # Herramienta de gestión de Django
├── db.sqlite3              # Base de datos
└── requirements.txt        # Dependencias del proyecto
```

## 🗄️ Modelos de Datos

### Labs
Representa los laboratorios disponibles en la instalación.
- `lab_name`: Nombre del laboratorio

### Storage
Equipos o maquinaria que necesita mantenimiento.
- `serial`: Número de serie del equipo
- `name`: Tipo de equipo (FK → Types)
- `brand`: Marca del equipo (FK → Brand)
- `lab_name`: Laboratorio donde se ubica (FK → Labs)
- `floor`: Piso donde está localizado
- `acquisition_date`: Fecha de adquisición
- `upcoming_maintenance`: Fecha programada para próximo mantenimiento
- `necessary_maintenance`: Estado (AL_DIA, POR_VENCER, VENCIDO)
- `image`: Foto del equipo
- **Flags de notificación:**
  - `email_sent_30_days`
  - `email_sent_7_days`
  - `email_sent_due`

### Maintenance
Registros de mantenimiento realizados.
- `machinary_maintenance`: Equipo mantenido (FK → Storage)
- `maintenance_date`: Fecha del mantenimiento
- `maintenance_provider`: Proveedor/técnico (FK → Supplier)
- `maintenance_image`: Foto del mantenimiento
- `maintenance_file`: Documento PDF adjunto
- `is_approved`: Estado de aprobación

### Types
Tipos o categorías de equipos (maquinaria, herramientas, etc.)

### Brand
Marcas/fabricantes de equipos

### Supplier
Proveedores de servicios de mantenimiento

## 🔐 Autenticación y Permisos

- **Login requerido:** Todas las vistas protegidas con `LoginRequiredMixin`
- **Roles:**
  - Superusuarios (is_superuser)
  - Grupo "admins": Acceso a funcionalidades administrativas
- **Flujo de autenticación:** Rutas bajo `/accounts/login/`

## 🌐 Rutas Principales

| Ruta | Descripción | Permisos |
|------|-------------|----------|
| `/` | Dashboard principal con resumen de equipos | Admin |
| `/search/` | Búsqueda y filtrado de equipos | Admin |
| `/machinary-detail/<serial>` | Detalle de un equipo específico | Admin |
| `/maintenance-detail/<id>` | Detalle de un mantenimiento | Admin |
| `/create-maintenance/` | Formulario para crear mantenimiento | Admin |
| `/create-machinary/` | Formulario para crear equipo | Admin |
| `/edit-machinary/<serial>/` | Editar información de equipo | Admin |
| `/maintenance-file/<id>` | Descargar archivo de mantenimiento | Admin |
| `/api/create-lab/` | API para crear laboratorio | Admin |
| `/api/create-brand/` | API para crear marca | Admin |
| `/api/create-type/` | API para crear tipo | Admin |

## ⏰ Scheduler (Tareas Programadas)

El sistema ejecuta tareas automáticas **diariamente a las 7:00 AM**:

### 1. **Envío de correos de mantenimiento** (`job_send_maintenance_emails`)
   - Envía recordatorio 30 días antes del vencimiento
   - Envía recordatorio 7 días antes del vencimiento
   - Envía recordatorio en la fecha de vencimiento
   - Evita duplicados con flags de control

### 2. **Actualización de mantenimiento próximo** (`update_upcoming_maintenance`)
   - Recalcula la próxima fecha de mantenimiento basada en registros aprobados

### 3. **Verificación de estado** (`check_maintenance_necessary`)
   - Actualiza el estado del mantenimiento (AL_DIA/POR_VENCER/VENCIDO)
   - Se basa en la diferencia entre hoy y la fecha próxima

## 📧 Sistema de Notificaciones

El sistema envía correos automáticos en tres momentos:

1. **30 días antes:** Notificación inicial de acción próxima
2. **7 días antes:** Recordatorio urgente
3. **Día del vencimiento:** Alertamiento de vencimiento

Cada notificación se controla con un flag en el modelo Storage para evitar envíos duplicados.

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.8 o superior
- pip
- SQLite3

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   cd FCAAssets
   ```

2. **Crear entorno virtual** (si no existe)
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   # o
   source venv/bin/activate      # En Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   IS_DEVELOPMENT=True
   APP_HOST=localhost:8000
   EMAIL_HOST=smtp.tuproveedor.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=tu-email@example.com
   EMAIL_HOST_PASSWORD=tu-contraseña
   EMAIL_USE_TLS=True
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Crear grupo de administradores** (opcional)
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import Group
   Group.objects.create(name='admins')
   ```

8. **Recolectar archivos estáticos** (para producción)
   ```bash
   python manage.py collectstatic
   ```

## 🏃 Ejecución

### Desarrollo
```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000`

### Producción
```bash
gunicorn FCAAssets.wsgi
```

## 📝 Formularios

### MaintenanceForm
Formulario para registrar un nuevo mantenimiento:
- Equipo (dropdown con serial y detalles)
- Fecha de mantenimiento
- Proveedor
- Imagen del mantenimiento
- Archivo PDF (validado)

### StorageForm
Formulario para crear/editar un equipo:
- Número de serie
- Imagen
- Fecha de adquisición
- Tipo de maquinaria
- Marca
- Laboratorio
- Piso
- Próxima fecha de mantenimiento

## 🔧 Utilities

### `email.py`
- `send_maintenance_email()`: Envía correos de notificación
- `job_send_maintenance_emails()`: Función ejecutada por el scheduler

### `check_maintenance_necessary.py`
- Verifica y actualiza el estado de mantenimiento de todos los equipos
- Calcula diferencia entre hoy y próximo mantenimiento

### `update_upcoming_maintenance.py`
- Actualiza la próxima fecha de mantenimiento
- Se basa en el último mantenimiento aprobado

### `validation_file.py`
- Validador personalizado para archivos PDF
- Aseguran que solo se suban documentos en formato PDF

## 📊 Flujo de Trabajo Típico

1. **Administrador crea equipo** → `/create-machinary/`
   - Completa formulario con datos del equipo
   - Se asigna fecha de próximo mantenimiento automáticamente (1 año)

2. **Se monitora estado automáticamente**
   - Sistema calcula estado según fechas
   - Scheduler envía correos en fechas programadas

3. **Técnico registra mantenimiento** → `/create-maintenance/`
   - Selecciona equipo
   - Carga documentación (fotos y PDF)
   - Proporciona detalles del proveedor

4. **Administrador aprueba mantenimiento**
   - Revisa detalles
   - Aprueba registro

5. **Sistema actualiza próximo mantenimiento**
   - Calcula nueva fecha (usualmente +1 año)
   - Reinicia ciclo de notificaciones

## 🐛 Troubleshooting

### El scheduler no se ejecuta
- Verificar que `DEBUG=True` en settings
- Revisar logs del servidor
- Confirmar que APScheduler esté instalado

### Correos no se envían
- Validar credenciales SMTP en `.env`
- Verificar que el servidor SMTP está disponible
- Revisar logs: `logger.getLogger("maintenance_scheduler")`

### Archivos no se cargan
- Verificar permisos de carpeta `uploads/`
- Confirmar que Pillow está instalado correctamente
- Revisar validadores de archivo

## 📄 Licencia

Este proyecto es propiedad de FCAAssets.

## 👥 Contacto

Para preguntas o reportar problemas, contactar al equipo de desarrollo.

---

**Última actualización:** Febrero 2026
