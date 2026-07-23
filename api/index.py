import os
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')

if os.environ.get('VERCEL'):
    # Vercel's deployment bundle is read-only at runtime, but SQLite needs a
    # writable path even for reads (lock/journal files). Copy the seeded,
    # read-only db into /tmp once per cold start and point Django at that.
    tmp_db = Path('/tmp/db.sqlite3')
    if not tmp_db.exists():
        shutil.copy(BASE_DIR / 'db.sqlite3', tmp_db)
    os.environ['DJANGO_DB_PATH'] = str(tmp_db)

from django.core.wsgi import get_wsgi_application  # noqa: E402
from whitenoise import WhiteNoise  # noqa: E402

django_app = get_wsgi_application()

app = WhiteNoise(django_app, root=str(BASE_DIR / 'staticfiles'), prefix='static/')
app.add_files(str(BASE_DIR / 'media'), prefix='media/')
