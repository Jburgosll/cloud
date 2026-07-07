# Netflix Clone (Django) — Segunda Entrega AWS

Sitio Django básico (HTML/CSS/JS) usado para la práctica de despliegue en AWS:
EC2 Linux (Apache/Nginx), EC2 Windows (IIS), RDS (MySQL) y S3 (servicio adicional).

## Estructura

- `catalog/models.py` — modelos `Catalog` (categorías/filas del inicio) y `Movie` (título, descripción, catálogo, poster, si es el "hero").
- `catalog/views.py` — home dinámico + panel de administración propio (`/panel/`) para crear catálogos y películas; si no hay datos usa ejemplos hardcodeados (para que el sitio nunca se vea roto).
- `catalog/forms.py` — formularios de catálogos y películas.
- `netflixclone/settings.py` — toda la configuración de RDS y S3 se activa/desactiva con variables de entorno del archivo `.env`.

## 1. Instalación local

```bash
pip install -r requirements.txt
copy .env.example .env      # (ya viene creado un .env de ejemplo con todo en False)
python manage.py migrate
python manage.py runserver
```

### Panel de administración (`/panel/`)

Se entra directo con el enlace **"Administrar"** del navbar (sin usuarios ni login:
es una simulación de la herramienta que se implementará más adelante).

- **Nuevo catálogo** — crea las filas del inicio (ej. "Populares en Netflix") con su orden.
- **Nueva película** — título, sinopsis, catálogo, poster (esa imagen va a S3 cuando `USE_S3=True`), opción de mostrarla en el banner principal y orden.
- Listados con opción de eliminar catálogos (con sus películas) y películas.

El `/admin/` clásico de Django sigue disponible como alternativa (requiere
`python manage.py createsuperuser`). Con `USE_S3=False` y `USE_RDS=False` todo
funciona 100% local (SQLite + archivos en `media/`), ideal para desarrollar antes
de tocar AWS.

## 2. Servicio adicional: Amazon S3

Esto es lo que conecta el `Storage` de Django con S3 para guardar y servir
**solo las imágenes** (`media/posters/`, los posters que subes desde el panel).
El CSS y el JS se sirven siempre en local.

### Pasos en la consola de AWS

1. **S3 → Crear bucket**
   - Nombre único, ej. `netflix-clone-<tu-nombre>`.
   - Región, ej. `us-east-1`.
   - Puedes dejar "Block all public access" activado si vas a usar URLs firmadas,
     pero para que las imágenes se vean directo en el navegador lo más simple
     para la demo es **desactivar el bloqueo público** y agregar esta Bucket Policy
     (Permissions → Bucket Policy):

     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Sid": "PublicReadGetObject",
           "Effect": "Allow",
           "Principal": "*",
           "Action": "s3:GetObject",
           "Resource": "arn:aws:s3:::NOMBRE_DE_TU_BUCKET/*"
         }
       ]
     }
     ```

2. **IAM → Crear usuario** (acceso programático) o mejor, un **rol IAM** adjunto a
   la instancia EC2 si el sitio corre ahí (evita guardar claves en el servidor).
   - Política: `AmazonS3FullAccess` (para la práctica) o una política restringida
     al bucket específico.
   - Si usas un usuario IAM, genera un **Access Key ID** y **Secret Access Key**.

3. Completa en tu `.env`:

   ```
   USE_S3=True
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   AWS_STORAGE_BUCKET_NAME=netflix-clone-tu-nombre
   AWS_S3_REGION_NAME=us-east-1
   ```

4. Reinicia el sitio:

   ```bash
   python manage.py runserver
   ```

   Al subir un poster desde el panel (`/panel/`), el archivo se guarda directo en
   `s3://tu-bucket/media/posters/...` y la página lo muestra como imagen de fondo
   de la card (en vez del gradiente de color de respaldo).

### Qué mostrar en la sustentación

- Consola S3 → el bucket con la carpeta `media/posters/` (las imágenes subidas desde el panel).
- El sitio funcionando con esas imágenes cargando desde la URL de S3 (puedes verlo en
  el inspector del navegador → pestaña Network → la URL de la imagen apunta a
  `https://tu-bucket.s3.us-east-1.amazonaws.com/media/posters/...`).
- Explicar que Django usa `django-storages` + `boto3` como backend de almacenamiento
  (`STORAGES["default"]` en `settings.py`), así que el código de la app no cambia:
  solo cambia dónde se guardan las imágenes.

## 3. RDS (MySQL)

1. RDS → Crear base de datos → MySQL → plantilla "Free tier".
2. Anota el **endpoint**, usuario y contraseña maestra.
3. En el Security Group de la instancia RDS, habilita el puerto 3306 desde tu IP
   (para conectarte con un cliente externo) y/o desde el Security Group de tu EC2.
4. Completa en `.env`:

   ```
   USE_RDS=True
   RDS_DB_NAME=netflixdb
   RDS_DB_USER=admin
   RDS_DB_PASSWORD=...
   RDS_DB_HOST=tu-instancia.xxxxx.us-east-1.rds.amazonaws.com
   RDS_DB_PORT=3306
   ```

5. Crea la base y corre migraciones:

   ```bash
   python manage.py migrate
   ```

6. Para "conexión desde cliente externo" (requisito de la entrega), conéctate con
   MySQL Workbench o `mysql -h <endpoint> -u admin -p` usando esas mismas credenciales.

## 4. EC2 Linux (Apache/Nginx)

- Instancia Amazon Linux, Security Group con puertos 22 (SSH) y 80 (HTTP) abiertos.
- Conéctate por SSH, instala Python, git, `pip install -r requirements.txt`.
- Copia el proyecto (git clone o `scp`), crea el `.env` con `USE_S3`/`USE_RDS` en `True`
  apuntando a los recursos ya creados.
- Sirve la app con Gunicorn detrás de Nginx (o `mod_wsgi` con Apache) — Nginx/Apache
  hace de proxy reverso hacia Gunicorn en `127.0.0.1:8000`.
- Agrega la IP pública/DNS de la instancia a `DJANGO_ALLOWED_HOSTS` en el `.env`.

## 5. EC2 Windows (IIS)

- Instancia Windows Server, conéctate por RDP.
- Instala IIS + el módulo `wfastcgi` (o usa IIS solo como proxy hacia Waitress/Gunicorn
  corriendo el sitio Django en `127.0.0.1:8000`, similar al esquema de Nginx).
- Publica el sitio en IIS Manager apuntando al proyecto, agrega el binding en el
  puerto 80 y abre el puerto en el Security Group de la instancia.
