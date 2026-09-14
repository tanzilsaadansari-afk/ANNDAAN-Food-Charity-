# Anndaan — food donation prototype

A working prototype connecting food **donors** (restaurants, households, event
caterers) with **recipients** (NGOs, volunteers) who can pick up surplus food
before it spoils.

## Stack

- **Flask** (Python) — server, routing, form handling
- **SQLite** — single-file database, zero setup
- **Jinja2 templates + plain CSS** — no build step, no JS framework

Chosen for a prototype because it's one process, one file DB, and runs with
no npm/build tooling — you can be looking at the app in under a minute.

## How to run it

```bash
cd anndaan
python3 -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python3 app.py
```

Open **http://localhost:5050**. The SQLite database (`anndaan.db`) is created
automatically on first run in the same folder.

## What's in the prototype

- **Home** — live counts (available / claimed / completed) and the most
  recent postings.
- **Donate food** (`/donate`) — a donor posts what food, how much, where to
  pick up, and by when.
- **Find food** (`/browse`) — recipients browse available donations, with a
  veg / non-veg filter.
- **Donation detail** (`/donation/<id>`) — full details; a recipient claims
  it by leaving their name and contact (which reveals the donor's contact);
  the claimant later marks it picked up.

Donation status moves `available → claimed → completed`. Everything is
stored in one `donations` table — see `app.py::init_db` for the schema.

## What I'd extend first

Roughly in priority order for turning this into something real:

1. **Accounts & auth** — right now anyone can post or claim anything with no
   login. Add donor/NGO accounts (Flask-Login + password hashing, or magic
   links) so donation history and trust build up per user.
2. **Location-aware matching** — store lat/lng on donations (geocode the
   pickup address) and show/sort `/browse` by distance from the recipient,
   or push notifications to nearby NGOs when something new is posted.
3. **Expiry handling** — a background job (APScheduler or a cron hitting a
   `/cleanup` route) that auto-expires donations past their pickup-by time
   and surfaces "expiring soon" badges.
4. **Notifications** — SMS/WhatsApp (Twilio) to the donor when claimed, and
   to nearby NGOs when a new donation is posted — this is the feature that
   actually makes the loop fast in the real world.
5. **Photos** — let donors attach a photo of the food; recipients decide
   faster with a picture than with text alone.
6. **Move off SQLite** — once there's real concurrent traffic, move to
   Postgres (SQLite's fine solo, but will lock up under concurrent writes).
7. **Admin/NGO dashboard** — a view scoped to "my organisation's claimed
   donations" with pickup logistics, instead of everything being anonymous.

## Known shortcuts (it's a prototype)

- No authentication — anyone can post/claim.
- No input sanitisation beyond "required" — don't expose this to the
  internet as-is.
- `app.secret_key` is hardcoded — replace before any real deployment.
- Times are plain strings, not timezone-aware.
