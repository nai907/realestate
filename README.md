# HomeComfy

A real estate listings website built with **Django** on the backend and **Vue 3 (via CDN)** for frontend interactivity — no separate frontend build, no npm. Templates are plain Django HTML, served from within the Django app itself.

## Features

- Property listings grid with pagination
- Property detail pages with a Vue-powered image gallery (thumbnail click / prev-next navigation)
- Featured listings section on the homepage
- Client-side "save to favorites" heart toggle (persisted in `localStorage`, no backend needed)
- Full CRUD for properties and their photos via the Django admin
- Sample data generator with procedurally drawn placeholder property photos

## Tech stack

- **Backend**: Django 6, SQLite
- **Frontend**: Django templates + Vue 3 loaded from a CDN, mounted inline per page
- **Images**: Pillow (for generated placeholder photos and real uploads via the admin)

## Project structure

```
realestate/          Django project config (settings, urls)
listings/            The single Django app
  models.py          Property, PropertyImage
  admin.py            Admin CRUD (with inline image uploads)
  views.py            HomeView, ListingListView, ListingDetailView
  templates/listings/ HTML templates (Vue mounted inline)
  static/listings/    CSS
  management/commands/seed_data.py   Demo data generator
```

## Getting started

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data       # populates ~9 sample properties with placeholder photos
python manage.py createsuperuser # for /admin/ access
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` — homepage with featured listings
- `http://127.0.0.1:8000/listings/` — full listings grid
- `http://127.0.0.1:8000/admin/` — manage properties and upload real photos

## Adding properties

- **One-off / real listings**: use the Django admin (`/admin/`) — add a Property, then upload photos in the inline images section.
- **Bulk / demo data**: add entries to `SAMPLE_PROPERTIES` in `listings/management/commands/seed_data.py` and re-run `python manage.py seed_data` (it skips titles that already exist, so it's safe to re-run).

## Configuration

`SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` in `realestate/settings.py` read from environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`) with safe local-dev defaults, so no setup is required to run locally.

## Deploying to Vercel (read-only demo)

Vercel's serverless filesystem is read-only at runtime, so this deploy is a **browsing demo only**: listings, detail pages, and the image gallery work normally, but admin logins/edits and new photo uploads won't persist between requests. For a real production deployment, swap SQLite for a hosted Postgres and move `MEDIA_ROOT` to cloud storage (e.g. S3, Cloudinary) first.

How it works:
- `api/index.py` is the WSGI entrypoint. On Vercel it copies the bundled, pre-seeded `db.sqlite3` into `/tmp` on cold start (SQLite needs a writable path even for reads), and wraps the Django app with [WhiteNoise](https://whitenoise.readthedocs.io/) to serve `staticfiles/` and `media/` directly.
- `vercel.json` routes all requests to that entrypoint.
- `db.sqlite3`, `media/`, and `staticfiles/` are committed to this repo (normally you wouldn't do this) specifically so the demo has data and photos to show without needing a database or storage service.

To deploy:
1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. On [vercel.com](https://vercel.com), click **Add New → Project**, import this repo, and deploy — `vercel.json` handles the rest.
3. In the Vercel project's **Settings → Environment Variables**, set `DJANGO_SECRET_KEY` to a random value (the repo's fallback key is public, since this repo is public — don't rely on it for anything beyond local dev).
4. `DJANGO_DEBUG` and `ALLOWED_HOSTS` are handled automatically when Vercel's `VERCEL` env var is present — no extra config needed.

To refresh the demo data shown on the deployed site, regenerate locally (`python manage.py seed_data --flush`, `python manage.py collectstatic --noinput`) and commit the updated `db.sqlite3` / `media/` / `staticfiles/`.
