import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os

DB_PATH = Path(__file__).parent / "anndaan.db"
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")  # Use env var in production

# Language translations
translations = {
    'en': {
        'home': 'Home',
        'browse': 'Discover',
        'donate': 'Donate food',
        'login': 'Log in',
        'register': 'Join Anndaan',
        'logout': 'Log out',
        'hero_title': 'Good food deserves a second chance',
        'hero_subtitle': 'Small acts, shared locally, make a real difference.',
        'eyebrow_dashboard': 'Saturday, 22 August 2026',
        'action_donate': 'Donate food',
        'action_donate_desc': 'Share surplus nearby',
        'action_browse': 'Find a meal',
        'action_browse_desc': 'Available now',
        'impact_meals': 'meals shared',
        'impact_people': 'people helped',
        'impact_food': 'food rescued',
        'section_community': 'Your community',
        'section_impact': 'Impact at a glance',
        'section_nearby': 'Nearby donations',
        'section_active': 'Active donation',
        'section_recent': 'Fresh from the community',
        'header_recent': 'Just posted',
        'tag_veg': 'Veg',
        'tag_non_veg': 'Non-veg',
        'placeholder_food_item': 'e.g. Rice, dal, mixed vegetable curry',
        'placeholder_quantity': 'e.g. serves 20 people',
        'placeholder_address': 'Full address or landmark',
        'placeholder_notes': 'Packed in containers, ready from 7pm, ring the bell etc.',
        'button_post_donation': 'Post donation',
        'button_claim_donation': 'Claim this donation',
        'button_mark_picked_up': 'Mark as picked up',
        'label_food_item': 'Food item(s)',
        'label_food_type': 'Type',
        'label_quantity': 'Quantity',
        'label_pickup_address': 'Pickup address',
        'label_pickup_by': 'Pick up by',
        'label_notes': 'Notes (optional)',
        'title_home': 'Home · Anndaan',
        'title_browse': 'Find food — Anndaan',
        'title_donate': 'Donate food — Anndaan',
        'title_about': 'About — Anndaan',
        'title_login': 'Log in — Anndaan',
        'title_register': 'Sign up — Anndaan',
        'title_detail': ' — Anndaan',
        'footer_text': 'Anndaan · food shared is a meal saved',
        'about_mission': 'Our Mission',
        'about_mission_text': 'Anndaan aims to reduce food waste and fight hunger by creating a seamless bridge between food donors and NGOs. Our platform enables restaurants, households, and event caterers to share surplus food, ensuring it reaches those who need it before it spoils.',
        'about_developers': 'Developers',
        'about_credits': 'Built with ❤️ at Jhulelal Institute of Technology',
        'about_version': 'Version 2.0 — Prototype to Production',
        'nav_home': 'Home',
        'nav_browse': 'Discover',
        'nav_about': 'About',
        'nav_donate': 'Donate food',
        'nav_login': 'Log in',
        'nav_register': 'Join Anndaan',
        'nav_logout': 'Log out',
        'nav_profile': 'Profile',
        'nav_signin': 'Sign in',
        'bottom_nav_home': 'Home',
        'bottom_nav_donate': 'Donate',
        'bottom_nav_browse': 'Nearby',
        'bottom_nav_requests': 'Requests',
        'bottom_nav_profile': 'Profile',
        'bottom_nav_signin': 'Sign in',
        'flash_registered': 'Account created successfully! Welcome to Anndaan.',
        'flash_login': 'Welcome back, {name}.',
        'flash_logout': 'Logged out successfully.',
        'flash_donation_posted': 'Donation posted successfully! Thank you for sharing — an NGO can now claim it.',
        'flash_donation_claimed': 'Donation claimed successfully! Contact the donor to arrange pickup.',
        'flash_donation_completed': 'Donation marked as picked up successfully. Thanks for closing the loop!',
        'flash_please_login': 'Please log in to continue.',
        'flash_only_donors': 'That page is only for donors.',
        'flash_only_ngos': 'That page is only for NGOs.',
        'flash_account_exists': 'An account with that email already exists — try logging in.',
        'flash_invalid_email': 'Incorrect email or password.',
        'flash_select_role': 'Please choose an account type.',
        'flash_fill_form': 'Please fill in: {fields}',
        'flash_expiry_future': 'Expiry time must be in the future.',
        'flash_invalid_expiry': 'Invalid expiry time format.',
        'flash_quantity_required': 'Please enter a quantity.',
        'flash_phone_invalid': 'Please enter a valid 10-digit phone number.',
        'flash_donation_not_found': "That donation doesn't exist (maybe it was removed).",
        'flash_donation_expired': 'This donation has expired.',
        'flash_claim_only_ngo': 'Only NGO accounts can claim donations.',
        'flash_login_to_claim': 'Log in as an NGO to claim this donation, or sign up if you don\'t have an account yet.',
        'flash_claimer_contact': 'Claimed by {name} · Contact: {phone} · claimed at {time}',
        'flash_completed_note': 'This donation was picked up. Thank you for closing the loop.',
        'map_copy_text': 'Good food is close by',
        'map_copy_subtext': 'Discover donations and pickup points around you.',
        'map_explore_button': 'Explore nearby',
        'status_ready': 'Ready for a helping hand',
        'status_claimed': 'Pickup in progress',
        'status_dot_tooltip': 'Status indicator',
        'timeline_posted': 'Posted',
        'timeline_matched': 'Matched',
        'timeline_picked': 'Picked up',
        'timeline_delivered': 'Delivered',
        'language_english': 'English',
        'language_hindi': 'हिंदी',
        'language_toggle': 'Language',
    },
    'hi': {
        'home': 'होम',
        'browse': 'खोजें',
        'donate': 'दान दें',
        'login': 'लॉग इन करें',
        'register': 'पंजीकरण करें',
        'logout': 'लॉग आउट',
        'hero_title': 'अच्छा भोजन एक दूसरा मौका पाने का हकदार है',
        'hero_subtitle': 'स्थानीय स्तर पर साझा किए गए छोटे-छोटे कार्य वास्तविक अंतर ला सकते हैं।',
        'eyebrow_dashboard': 'शनिवार, 22 अगस्त 2026',
        'action_donate': 'दान दें',
        'action_donate_desc': 'निकटवर्ती अतिरिक्त साझा करें',
        'action_browse': 'एक भोजन खोजें',
        'action_browse_desc': 'अभी उपलब्ध',
        'impact_meals': 'भोजन साझा किए गए',
        'impact_people': 'लोगों की मदद की गई',
        'impact_food': 'भोजन बचाया गया',
        'section_community': 'आपका समुदाय',
        'section_impact': 'प्रभाव एक नज़र में',
        'section_nearby': 'निकटवर्ती दान',
        'section_active': 'सक्रिय दान',
        'section_recent': 'समुदाय से ताज़ा',
        'header_recent': 'ताज़ा पोस्ट किया गया',
        'tag_veg': 'शाकाहारी',
        'tag_non_veg': 'मांसाहारी',
        'placeholder_food_item': 'उदाहरण: चावल, दाल, मिश्रित सब्जी करी',
        'placeholder_quantity': 'उदाहरण: 20 लोगों के लिए पर्याप्त',
        'placeholder_address': 'पूरा पता या लैंडमार्क',
        'placeholder_notes': 'डब्बों में पैक किया हुआ, शाम 7 बजे से तैयार, घंटी बजाएं आदि।',
        'button_post_donation': 'दान पोस्ट करें',
        'button_claim_donation': 'इस दान का दावा करें',
        'button_mark_picked_up': 'ले लिया गया चिह्नित करें',
        'label_food_item': 'भोजन की वस्तु(यें)',
        'label_food_type': 'प्रकार',
        'label_quantity': 'मात्रा',
        'label_pickup_address': 'उठाने का पता',
        'label_pickup_by': 'उठाने का समय',
        'label_notes': 'टिप्पणी (वैकल्पिक)',
        'title_home': 'होम · अनндаान',
        'title_browse': 'भोजन खोजें — अनндаान',
        'title_donate': 'दान दें — अनндаान',
        'title_about': 'के बारे में — अनндаान',
        'title_login': 'लॉग इन करें — अनндаान',
        'title_register': 'साइन अप करें — अनндаान',
        'title_detail': ' — अनндаान',
        'footer_text': 'अनndaaan · साझा किया गया भोजन एक भोजन बचाता है',
        'about_mission': 'हमारा मिशन',
        'about_mission_text': 'अनndaaan का लक्ष्य खाद्य बर्बादी कम करना और भूख मिटाना है, खाद्य दाताओं और एनजीओ के बीच एक सहज सेतु बनाकर। हमारा प्लेटफ़ॉर्म रेस्तरां, घरों और इवेंट कैटरर्स को अतिरिक्त खाद्य साझा करने में सक्षम बनाता है, जिससे यह सुनिश्चित होता है कि यह बर्बाद होने से पहले ज़रूरतमंदों तक पहुँचे।',
        'about_developers': 'डेवलपर्स',
        'about_credits': 'झूलेल इंस्टीट्यूट ऑफ़ टेक्नोलॉजी में ❤️ से बनाया गया',
        'about_version': 'संस्करण 2.0 — प्रोटोटाइप से उत्पादन तक',
        'nav_home': 'होम',
        'nav_browse': 'खोजें',
        'nav_about': 'के बारे में',
        'nav_donate': 'दान दें',
        'nav_login': 'लॉग इन करें',
        'nav_register': 'पंजीकरण करें',
        'nav_logout': 'लॉग आउट',
        'nav_profile': 'प्रोफ़ाइल',
        'nav_signin': 'साइन इन करें',
        'bottom_nav_home': 'होम',
        'bottom_nav_donate': 'दान दें',
        'bottom_nav_browse': 'खोजें',
        'bottom_nav_requests': 'अनुरोध',
        'bottom_nav_profile': 'प्रोफ़ाइल',
        'bottom_nav_signin': 'साइन इन करें',
        'flash_registered': 'खाता सफलतापूर्वक बनाया गया! अनndaaan में आपका स्वागत है।',
        'flash_login': 'वापस आएँ पर स्वागत है, {name}।',
        'flash_logout': 'सफलतापूर्वक लॉग आउट हो गए।',
        'flash_donation_posted': 'दान सफलतापूर्वक पोस्ट किया गया! साझा करने के लिए धन्यवाद — अब एक एनजीओ इसे दावा कर सकता है।',
        'flash_donation_claimed': 'दान सफलतापूर्वक दावा कर लिया गया! दाता से संपर्क करके उठाने की व्यवस्था करें।',
        'flash_donation_completed': 'दान सफलतापूर्वक ले लिया गया चिह्नित कर दिया गया। लूप पूरा करने के लिए धन्यवाद!',
        'flash_please_login': 'कृपया जारी रखने के लिए लॉग इन करें।',
        'flash_only_donors': 'यह पृष्ठ केवल दाताओं के लिए है।',
        'flash_only_ngos': 'यह पृष्ठ केवल एनजीओ के लिए है।',
        'flash_account_exists': 'इस ईमेल से पहले से एक खाता मौजूद है — कृपया लॉग इन करके देखें।',
        'flash_invalid_email': 'गलत ईमेल या पासवर्ड।',
        'flash_select_role': 'कृपया एक खाता प्रकार चुनें।',
        'flash_fill_form': 'कृपया निम्नलिखित फ़ील्ड भरें: {fields}',
        'flash_expiry_future': 'समाप्ति समय भविष्य में होना चाहिए।',
        'flash_invalid_expiry': 'अमान्य समाप्ति समय प्रारूप।',
        'flash_quantity_required': 'कृपया मात्रा दर्ज करें।',
        'flash_phone_invalid': 'कृपया एक वैध 10-अंकीय फोन नंबर दर्ज करें।',
        'flash_donation_not_found': "वह दान मौजूद नहीं है (शायद इसे हटा दिया गया हो।)",
        'flash_donation_expired': 'यह दान समाप्त हो गया है।',
        'flash_claim_only_ngo': 'केवल एनजीओ खातों वाले दान का दावा कर सकते हैं।',
        'flash_login_to_claim': 'इस दान का दावा करने के लिए एनजीओ के रूप में लॉग इन करें, या यदि आपके पास खाता नहीं है तो साइन अप करें।',
        'flash_claimer_contact': '{name} द्वारा दावा किया गया · संपर्क: {phone} · {time} पर दावा किया गया',
        'flash_completed_note': 'यह दान उठा लिया गया है। लूप पूरा करने के लिए धन्यवाद।',
        'map_copy_text': 'अच्छा भोजन पास में है',
        'map_copy_subtext': 'पास के दान और उठाने के बिंदुओं की खोज करें।',
        'map_explore_button': 'पास की खोज करें',
        'status_ready': 'मदद के लिए तैयार',
        'status_claimed': 'उठाने की प्रक्रिया में',
        'status_dot_tooltip': 'स्थिति संकेतक',
        'timeline_posted': 'पोस्ट किया गया',
        'timeline_matched': 'मिलान किया गया',
        'timeline_picked': 'उठा लिया गया',
        'timeline_delivered': 'डिलीवर किया गया',
        'language_english': 'अंग्रेज़ी',
        'language_hindi': 'हिंदी',
        'language_toggle': 'भाषा',
    }
}

# ---------- DB helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    # Remove existing database to start fresh with seed data (for demo purposes)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,               -- donor / ngo
            verified INTEGER DEFAULT 0,       -- 0 = not verified, 1 = verified NGO
            created_at TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            food_item TEXT NOT NULL,
            food_type TEXT NOT NULL,          -- veg / non-veg
            quantity TEXT NOT NULL,           -- e.g. "serves 20"
            pickup_address TEXT NOT NULL,
            expiry_time TEXT NOT NULL,        -- pickup-by, ISO-ish string
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'available',  -- available / claimed / completed
            claimed_by_id INTEGER,
            created_at TEXT NOT NULL,
            claimed_at TEXT,
            expires_at TEXT,                  -- when donation expires
            latitude REAL,                    -- latitude coordinate
            longitude REAL,                   -- longitude coordinate
            FOREIGN KEY (donor_id) REFERENCES users (id),
            FOREIGN KEY (claimed_by_id) REFERENCES users (id)
        )
        """
    )
    db.commit()
    
    # Insert sample users (donors and NGOs)
    sample_users = [
        ("Fresh Foods Donor", "5551234567", "donor1@example.com", "donor", 0),
        ("Community Kitchen NGO", "5559876543", "ngo1@example.com", "ngo", 1),  # Verified NGO
        ("Green Market Donor", "5555555555", "donor2@example.com", "donor", 0),
        ("Helping Hands NGO", "5551112222", "ngo2@example.com", "ngo", 0),     # Not verified
        ("Sunny Farm Donor", "5553333333", "donor3@example.com", "donor", 0),
        ("City Food Bank NGO", "5554444444", "ngo3@example.com", "ngo", 1),    # Verified NGO
    ]
    
    for name, phone, email, role, verified in sample_users:
        db.execute(
            """
            INSERT INTO users (name, phone, email, password_hash, role, verified, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                email,
                generate_password_hash("password123"),  # Same password for all samples
                role,
                verified,
                datetime.now().isoformat(timespec="minutes"),
            ),
        )
    
    # Insert sample donations
    now = datetime.now()
    sample_donations = [
        # Donor 1 (Fresh Foods Donor)
        (1, "Cooked Rice and Dal", "veg", "serves 30 people", "123 Main Street, Downtown", (now + timedelta(hours=2)).isoformat(timespec="minutes"), "Freshly cooked, ready to serve", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=2)).isoformat(timespec="minutes"), None, None),
        (1, "Vegetable Curry", "veg", "serves 25 people", "456 Oak Avenue, Uptown", (now + timedelta(hours=4)).isoformat(timespec="minutes"), "Spicy vegetable curry in containers", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=4)).isoformat(timespec="minutes"), None, None),
        # Donor 3 (Green Market Donor)
        (3, "Fresh Fruits Basket", "veg", "serves 15 people", "789 Pine Road, Suburb", (now + timedelta(hours=1)).isoformat(timespec="minutes"), "Assorted fruits: apples, bananas, oranges", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=1)).isoformat(timespec="minutes"), None, None),
        # Donor 5 (Sunny Farm Donor)
        (5, "Grilled Chicken Platter", "non-veg", "serves 20 people", "321 Elm Street, West Side", (now + timedelta(hours=3)).isoformat(timespec="minutes"), "Grilled chicken with rice and vegetables", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=3)).isoformat(timespec="minutes"), None, None),
        # Add a few more with coordinates for map testing
        (1, "Fresh Salad Mix", "veg", "serves 10 people", "123 Main Street, Downtown", (now + timedelta(hours=6)).isoformat(timespec="minutes"), "Mixed greens with dressing", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=6)).isoformat(timespec="minutes"), 40.7128, -74.0060),  # NYC coordinates
        (3, "Bread Loaves", "veg", "serves 40 people", "789 Pine Road, Suburb", (now + timedelta(hours=5)).isoformat(timespec="minutes"), "Freshly baked whole wheat bread", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=5)).isoformat(timespec="minutes"), 34.0522, -118.2437),  # LA coordinates
        (5, "Chocolate Cake", "veg", "serves 8 people", "321 Elm Street, West Side", (now + timedelta(hours=2)).isoformat(timespec="minutes"), "Homemade chocolate cake", "available", now.isoformat(timespec="minutes"), (now + timedelta(hours=2)).isoformat(timespec="minutes"), 41.8781, -87.6298),  # Chicago coordinates
    ]
    
    for donation in sample_donations:
        db.execute(
            """
            INSERT INTO donations
                (donor_id, food_item, food_type, quantity,
                 pickup_address, expiry_time, notes, status, created_at, expires_at,
                 latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            donation,
        )
    
    db.commit()
    db.close()

# ---------- auth helpers ----------
def get_current_user():
    if "user_id" not in session:
        return None
    if "user" not in g:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
    return g.user

def get_current_user_by_id(user_id):
    return get_db().execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}

@app.before_request
def before_request():
    if 'language' not in session:
        session['language'] = 'en'

def t(key):
    lang = session.get('language', 'en')
    return translations.get(lang, translations['en']).get(key, key)

app.jinja_env.globals.update(t=t)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            flash(t('flash_please_login'), "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if user is None:
                flash(t('flash_please_login'), "error")
                return redirect(url_for("login", next=request.path))
            if user["role"] != role:
                who = "donors" if role == "donor" else "NGOs"
                flash(t('flash_only_donors') if role == "donor" else t('flash_only_ngos'), "error")
                return redirect(url_for("home"))
            return view(*args, **kwargs)
        return wrapped
    return decorator

# ---------- auth routes ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        required = ["name", "phone", "email", "password", "role"]
        missing = [f for f in required if not form.get(f, "").strip()]
        if missing:
            flash(t('flash_fill_form').format(fields=', '.join(missing)), "error")
            return render_template("register.html", form=form)
        if form["role"] not in ("donor", "ngo"):
            flash(t('flash_select_role'), "error")
            return render_template("register.html", form=form)

        # Validate phone number (basic validation)
        if not form["phone"].isdigit() or len(form["phone"]) != 10:
            flash(t('flash_phone_invalid'), "error")
            return render_template("register.html", form=form)

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (form["email"].strip().lower(),)
        ).fetchone()
        if existing:
            flash(t('flash_account_exists'), "error")
            return render_template("register.html", form=form)

        db.execute(
            """
            INSERT INTO users (name, phone, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                form["name"].strip(),
                form["phone"].strip(),
                form["email"].strip().lower(),
                generate_password_hash(form["password"]),
                form["role"],
                datetime.now().isoformat(timespec="minutes"),
            ),
        )
        db.commit()
        new_user = db.execute(
            "SELECT id FROM users WHERE email = ?", (form["email"].strip().lower(),)
        ).fetchone()
        session["user_id"] = new_user["id"]
        flash(t('flash_registered'), "success")
        return redirect(url_for("home"))

    return render_template("register.html", form={})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash(t('flash_invalid_email'), "error")
            return render_template("login.html", email=email)

        session["user_id"] = user["id"]
        flash(t('flash_login').format(name=user['name']), "success")
        next_url = request.args.get("next")
        return redirect(next_url or url_for("home"))

    return render_template("login.html", email="")

@app.route("/logout")
def logout():
    session.clear()
    flash(t('flash_logout'), "success")
    return redirect(url_for("home"))

# ---------- cleanup helper ----------
def cleanup_expired_donations():
    """Remove donations that have expired"""
    db = get_db()
    current_time = datetime.now().isoformat(timespec="minutes")
    db.execute(
        "UPDATE donations SET status='expired' WHERE expiry_time < ? AND status='available'",
        (current_time,)
    )
    db.commit()

# ---------- error handlers ----------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db = get_db()
    db.rollback()
    return render_template('500.html'), 500

# ---------- language toggle route ----------
@app.route('/toggle-language')
def toggle_language():
    current = session.get('language', 'en')
    session['language'] = 'hi' if current == 'en' else 'en'
    # Redirect back to the referring page or home if not available
    return redirect(request.referrer or url_for('home'))

# ---------- app routes ----------
@app.route("/")
def home():
    db = get_db()
    stats = db.execute(
        """
        SELECT
          SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) AS available,
          SUM(CASE WHEN status='claimed' THEN 1 ELSE 0 END) AS claimed,
          SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) AS completed,
          SUM(CASE WHEN status='expired' THEN 1 ELSE 0 END) AS expired,
          COUNT(*) AS total
        FROM donations
        """
    ).fetchone()
    recent = db.execute(
        """
        SELECT donations.*, users.name AS donor_name
        FROM donations JOIN users ON users.id = donations.donor_id
        WHERE status='available' ORDER BY created_at DESC LIMIT 3
        """
    ).fetchall()
    return render_template("index.html", stats=stats, recent=recent)

@app.route("/donate", methods=["GET", "POST"])
@role_required("donor")
def donate():
    if request.method == "POST":
        form = request.form
        required = ["food_item", "food_type", "quantity", "pickup_address", "expiry_time"]
        missing = [f for f in required if not form.get(f, "").strip()]
        if missing:
            flash(t('flash_fill_form').format(fields=', '.join(missing)), "error")
            return render_template("donate.html", form=form)

        # Validate expiry time is in the future
        try:
            expiry_time = datetime.fromisoformat(form["expiry_time"].strip())
            if expiry_time <= datetime.now():
                flash(t('flash_expiry_future'), "error")
                return render_template("donate.html", form=form)
        except ValueError:
            flash(t('flash_invalid_expiry'), "error")
            return render_template("donate.html", form=form)

        # Validate quantity
        if not form["quantity"].strip():
            flash(t('flash_quantity_required'), "error")
            return render_template("donate.html", form=form)

        db = get_db()
        db.execute(
            """
            INSERT INTO donations
              (donor_id, food_item, food_type, quantity,
               pickup_address, expiry_time, notes, status, created_at, expires_at,
               latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'available', ?, ?, ?, ?)
            """,
            (
                get_current_user()["id"],
                form["food_item"].strip(),
                form["food_type"],
                form["quantity"].strip(),
                form["pickup_address"].strip(),
                form["expiry_time"].strip(),
                form.get("notes", "").strip(),
                datetime.now().isoformat(timespec="minutes"),
                datetime.now().isoformat(timespec="minutes"),
                None,  # latitude will be set via JS
                None   # longitude will be set via JS
            ),
        )
        db.commit()
        flash(t('flash_donation_posted'), "success")
        return redirect(url_for("browse"))

    default_expiry = (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M")
    return render_template("donate.html", form={}, default_expiry=default_expiry)


@app.route("/browse")
def browse():
    db = get_db()
    food_type = request.args.get("food_type", "")
    query = """
        SELECT donations.*, users.name AS donor_name
        FROM donations JOIN users ON users.id = donations.donor_id
        WHERE status='available'
    """
    params = []
    if food_type in ("veg", "non-veg"):
        query += " AND food_type = ?"
        params.append(food_type)
    query += " ORDER BY donations.created_at DESC"
    donations = db.execute(query, params).fetchall()
    return render_template("browse.html", donations=donations, food_type=food_type)


@app.route("/donation/<int:donation_id>")
def donation_detail(donation_id):
    db = get_db()
    d = db.execute(
        """
        SELECT donations.*,
               donor.name AS donor_name, donor.phone AS donor_phone,
               claimer.name AS claimer_name, claimer.phone AS claimer_phone
        FROM donations
        JOIN users AS donor ON donor.id = donations.donor_id
        LEFT JOIN users AS claimer ON claimer.id = donations.claimed_by_id
        WHERE donations.id = ?
        """,
        (donation_id,),
    ).fetchone()
    if d is None:
        flash(t('flash_donation_not_found'), "error")
        return redirect(url_for("browse"))
    
    # Check if donation has expired
    if d["expires_at"]:
        expiry_time = datetime.fromisoformat(d["expires_at"].strip())
        if expiry_time <= datetime.now():
            flash(t('flash_donation_expired'), "error")
            return redirect(url_for("browse"))

    return render_template("detail.html", d=d)


@app.route("/claim/<int:donation_id>", methods=["POST"])
@role_required("ngo")
def claim(donation_id):
    db = get_db()
    d = db.execute(
        "SELECT * FROM donations WHERE id=? AND status='available'",
        (donation_id,),
    ).fetchone()
    if d is None:
        flash(t('flash_donation_not_found'), "error")
        return redirect(url_for("browse"))

    db.execute(
        """
        UPDATE donations
        SET status='claimed', claimed_by_id=?, claimed_at=?
        WHERE id=? AND status='available'
        """,
        (get_current_user()["id"], datetime.now().isoformat(timespec="minutes"), donation_id),
    )
    db.commit()
    flash(t('flash_donation_claimed'), "success")
    return redirect(url_for("donation_detail", donation_id=donation_id))


@app.route("/complete/<int:donation_id>", methods=["POST"])
@login_required
def complete(donation_id):
    db = get_db()
    d = db.execute("SELECT * FROM donations WHERE id=?", (donation_id,)).fetchone()
    user = get_current_user()
    if d is None:
        flash(t('flash_donation_not_found'), "error")
        return redirect(url_for("browse"))
    if user["id"] not in (d["donor_id"], d["claimed_by_id"]):
        flash(t('flash_only_donor_or_ngo'), "error")
        return redirect(url_for("donation_detail", donation_id=donation_id))

    db.execute("UPDATE donations SET status='completed' WHERE id=?", (donation_id,))
    db.commit()
    flash(t('flash_donation_completed'), "success")
    return redirect(url_for("donation_detail", donation_id=donation_id))


@app.route("/about")
def about():
    db = get_db()
    stats = db.execute(
        """
        SELECT
          SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) AS available,
          SUM(CASE WHEN status='claimed' THEN 1 ELSE 0 END) AS claimed,
          SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) AS completed,
          SUM(CASE WHEN status='expired' THEN 1 ELSE 0 END) AS expired,
          COUNT(*) AS total
        FROM donations
        """
    ).fetchone()
    recent = db.execute(
        """
        SELECT donations.*, users.name AS donor_name
        FROM donations JOIN users ON users.id = donations.donor_id
        WHERE status='available' ORDER BY created_at DESC LIMIT 3
        """
    ).fetchall()
    return render_template("about.html", stats=stats, recent=recent)


@app.route('/api/donations')
def api_donations():
    return jsonify([dict(id=r['id'], food_type=r['food_type'], latitude=r['latitude'], longitude=r['longitude'], status=r['status']) for r in get_db().execute("SELECT id,food_type,latitude,longitude,status FROM donations WHERE status='available' AND latitude IS NOT NULL AND longitude IS NOT NULL").fetchall()])


if __name__ == "__main__":
    init_db()
    # Run cleanup first to remove expired donations
    with app.app_context():
        cleanup_expired_donations()
    app.run(debug=True, port=5050)