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
