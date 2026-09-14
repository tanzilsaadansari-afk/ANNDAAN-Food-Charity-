import os

base_dir = 'C:/Users/JOHN/Documents/andc2/templates'

# base.html
base_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Anndaan \u00b7 Share Food. Spread Hope.{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{{ url_for('home') }}">
      <span class="brand-name">Anndaan</span>
      <span class="brand-tagline">Share Food. Spread Hope.</span>
    </a>
    <nav class="desktop-nav">
      <a href="{{ url_for('home') }}">Home</a>
      <a href="{{ url_for('browse') }}">Discover</a>
      <a href="{{ url_for('about') }}">About</a>
      {% if current_user %}
        {% if current_user['role'] == 'donor' %}<a href="{{ url_for('donate') }}" class="nav-cta">Donate food</a>{% endif %}
        <span class="nav-user">{{ current_user['name'] }}</span>
        <a href="{{ url_for('logout') }}">Log out</a>
      {% else %}
        <a href="{{ url_for('login') }}">Log in</a>
        <a href="{{ url_for('register') }}" class="nav-cta">Join Anndaan</a>
      {% endif %}
    </nav>
  </header>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash-wrap">
        {% for category, message in messages %}
          <div class="flash flash-{{ category }}">{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  <main>
    {% block content %}{% endblock %}
  </main>

  <nav class="bottom-nav" aria-label="Main navigation">
    <a class="bottom-link active" href="{{ url_for('home') }}"><span class="nav-icon">\u2302</span><span>Home</span></a>
    <a class="bottom-link" href="{{ url_for('donate') if current_user and current_user['role'] == 'donor' else url_for('register') }}"><span class="nav-icon">\u221a</span><span>Donate</span></a>
    <a class="bottom-link" href="{{ url_for('browse') }}"><span class="nav-icon">\u2316</span><span>Nearby</span></a>
    <a class="bottom-link" href="{{ url_for('browse') }}"><span class="nav-icon">\u2661</span><span>Requests</span></a>
    <a class="bottom-link" href="{{ url_for('login') if not current_user else url_for('logout') }}"><span class="nav-icon">\u25cb</span><span>{{ 'Profile' if current_user else 'Sign in' }}</span></a>
  </nav>

  <footer class="footer">
    <span>Anndaan \u00b7 food shared is a meal saved</span>
  </footer>
</body>
</html>"""

# index.html
index_html = """{% extends "base.html" %}
{% block title %}Home \u00b7 Anndaan{% endblock %}
{% block content %}
<section class="dashboard-wrap">
  <div class="dashboard-heading">
    <div>
      <p class="eyebrow">Saturday, 22 August 2026</p>
      <h1>{% if current_user %}Good to see you, {{ current_user['name'].split(' ')[0] }}{% else %}Good food deserves a second chance{% endif %}</h1>
      <p class="hero-sub">Small acts, shared locally, make a real difference.</p>
    </div>
    <div class="profile-orb">{% if current_user %}{{ current_user['name'][0]|upper }}{% else %}A{% endif %}</div>
  </div>

  <div class="action-grid">
    <a class="action-card action-card-primary" href="{{ url_for('donate') if current_user and current_user['role'] == 'donor' else url_for('register') }}"><span class="action-symbol">\u221a</span><strong>Donate food</strong><small>Share surplus nearby</small></a>
    <a class="action-card" href="{{ url_for('browse') }}"><span class="action-symbol">\u2316</span><strong>Find a meal</strong><small>{{ stats['available'] or 0 }} available now</small></a>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Your community</p><h2>Impact at a glance</h2></div><span class="trend">This month \u2197</span></div>
  <div class="impact-grid">
    <div class="impact-card"><span class="impact-icon coral">\u2668</span><strong>{{ (stats['completed'] or 0) * 20 + 128 }}</strong><span>meals shared</span></div>
    <div class="impact-card"><span class="impact-icon green">\u2661</span><strong>{{ (stats['completed'] or 0) * 8 + 46 }}</strong><span>people helped</span></div>
    <div class="impact-card"><span class="impact-icon gold">\u2726</span><strong>{{ (stats['total'] or 0) * 3 + 18 }} kg</strong><span>food rescued</span></div>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Live in your area</p><h2>Nearby donations</h2></div><a class="text-link" href="{{ url_for('browse') }}">View all \u2192</a></div>
  <div class="map-panel"><div class="map-copy"><span class="map-badge">\u25cf LIVE</span><h3>Good food is close by</h3><p>Discover donations and pickup points around you.</p><a class="btn btn-dark" href="{{ url_for('browse') }}">Explore nearby</a></div><div class="map-art" aria-label="Map showing nearby donation activity"><span class="map-road road-one"></span><span class="map-road road-two"></span><span class="map-pin pin-one">\u2668</span><span class="map-pin pin-two">\u2668</span><span class="map-pin pin-three">\u25cf</span><span class="map-you">You</span></div></div>

  <div class="section-heading"><div><p class="eyebrow">Keep the loop moving</p><h2>Active donation</h2></div></div>
  <div class="status-card"><div class="status-top"><span class="status-dot"></span><div><strong>{% if stats['claimed'] %}Pickup in progress{% else %}Ready for a helping hand{% endif %}</strong><p>{% if stats['claimed'] %}A volunteer is on the way{% else %}Every donation starts with you{% endif %}</p></div><span class="status-arrow">\u2192</span></div><div class="timeline"><span class="done">Posted</span><span class="current">Matched</span><span class="picked up">Picked up</span><span class="delivered">Delivered</span></div></div>
</section>

{% if recent %}<section class="recent">
  <div class="section-heading"><div><p class="eyebrow">Fresh from the community</p><h2>Just posted</h2></div><a class="text-link" href="{{ url_for('browse') }}">See all \u2192</a></div>
  <div class="card-grid">
    {% for d in recent %}
    <a class="card" href="{{ url_for('donation_detail', donation_id=d['id']) }}">
      <span class="tag tag-{{ d['food_type'] }}">{{ d['food_type'] }}</span>
      <h3>{{ d['food_item'] }}</h3>
      <p class="card-meta">{{ d['quantity'] }} &middot; pickup by {{ d['expiry_time'] }}</p>
      <p class="card-loc">{{ d['pickup_address'] }}</p>
    </a>
    {% endfor %}
  </div>
</section>
{% endif %}
{% endblock %}"""

# browse.html
browse_html = """{% extends "base.html" %}
{% block title %}Find food \u2014 Anndaan{% endblock %}
{% block content %}
<section class="browse-page">
  <div class="browse-head">
    <h1>Available right now</h1>
    <div class="filters">
      <a class="filter-chip {% if not food_type %}active{% endif %}" href="{{ url_for('browse') }}">All</a>
      <a class="filter-chip {% if food_type=='veg' %}active{% endif %}" href="{{ url_for('browse', food_type='veg') }}">Veg</a>
      <a class="filter-chip {% if food_type=='non-veg' %}active{% endif %}" href="{{ url_for('browse', food_type='non-veg') }}">Non-veg</a>
    </div>
  </div>

  {% if donations %}
  <div class="card-grid">
    {% for d in donations %}
    <a class="card" href="{{ url_for('donation_detail', donation_id=d['id']) }}">
      <span class="tag tag-{{ d['food_type'] }}">{{ d['food_type'] }}</span>
      <h3>{{ d['food_item'] }}</h3>
      <p class="card-meta">{{ d['quantity'] }} &middot; pickup by {{ d['expiry_time'] }}</p>
      <p class="card-loc">{{ d['pickup_address'] }}</p>
      <p class="card-donor">from {{ d['donor_name'] }}</p>
    </a>
    {% endfor %}
  </div>
  {% else %}
  <div class="empty">
    <p>Nothing posted right now. Check back soon
      {% if current_user and current_user['role'] == 'donor' %}
        , or be the first to <a href="{{ url_for('donate') }}">post a donation</a>.
      {% else %}.{% endif %}
    </p>
  </div>
  {% endif %}
</section>
{% endblock %}"""

# donate.html
donate_html = """{% extends "base.html" %}
{% block title %}Donate food \u2014 Anndaan{% endblock %}
{% block content %}
<section class="form-page">
  <h1>Post a food donation</h1>
  <p class="form-sub">Posting as <strong>{{ current_user['name'] }}</strong> ({{ current_user['phone'] }}). Give NGOs enough detail to decide fast \u2014 what it is, how much, and how long it'll stay good.</p>
  <div class="map-container">
    <div id="map" style="height:300px;margin-bottom:10px;"></div>
    <input type="hidden" name="latitude" id="latitude" value="">
    <input type="hidden" name="longitude" id="longitude" value="">
  </div>

  <form method="post" class="form">
    <label>
      Food item(s)
      <input type="text" name="food_item" placeholder="e.g. Rice, dal, mixed vegetable curry" value="{{ form.get('food_item','') }}" required>
    </label>

    <div class="form-row">
      <label>
        Type
        <select name="food_type" required>
          <option value="">Select</option>
          <option value="veg" {% if form.get('food_type')=='veg' %}selected{% endif %}>Vegetarian</option>
          <option value="non-veg" {% if form.get('food_type')=='non-veg' %}selected{% endif %}>Non-vegetarian</option>
        </select>
      </label>

      <label>
        Quantity
        <input type="text" name="quantity" placeholder="e.g. serves 20 people" value="{{ form.get('quantity','') }}" required>
      </label>
    </div>

    <label>
      Pickup address
      <input type="text" name="pickup_address" placeholder="Full address or landmark" value="{{ form.get('pickup_address','') }}" required>
    </label>

    <label>
      Pick up by
      <input type="datetime-local" name="expiry_time" value="{{ form.get('expiry_time', default_expiry) }}" required>
    </label>

    <label>
      Notes (optional)
      <textarea name="notes" rows="3" placeholder="Packed in containers, ready from 7pm, ring the bell etc.">{{ form.get('notes','') }}</textarea>
    </label>

    <button type="submit" class="btn btn-primary">Post donation</button>
  </form>
</section>
{% endblock %}

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script>
  document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([20, 75], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    
    map.on('click', function(e) {
      const lat = e.latlng.lat.toFixed(6);
      const lng = e.latlng.lng.toFixed(6);
      document.getElementById('latitude').value = lat;
      document.getElementById('longitude').value = lng;
      L.marker([lat, lng]).addTo(map);
    });
  });
</script>"""

# detail.html
detail_html = """{% extends "base.html" %}
{% block title %}{{ d['food_item'] }} \u2014 Anndaan{% endblock %}
{% block content %}
<section class="detail-page">
  <span class="tag tag-{{ d['food_type'] }}">{{ d['food_type'] }}</span>
  <h1>{{ d['food_item'] }}</h1>
  <span class="status-pill status-{{ d['status'] }}">{{ d['status'] }}</span>

  <dl class="detail-list">
    <dt>Quantity</dt><dd>{{ d['quantity'] }}</dd>
    <dt>Pickup by</dt><dd>{{ d['expiry_time'] }}</dd>
    <dt>Pickup address</dt><dd>{{ d['pickup_address'] }}</dd>
    <dt>Donor</dt><dd>{{ d['donor_name'] }} \u00b7 {{ d['donor_phone'] }}</dd>
    {% if d['notes'] %}<dt>Notes</dt><dd>{{ d['notes'] }}</dd>{% endif %}
    <dt>Posted</dt><dd>{{ d['created_at'] }}</dd>
  </dl>

  {% if d['status'] == 'available' %}
    <div class="claim-box">
      {% if current_user and current_user['role'] == 'ngo' %}
        <h2>Claim this donation</h2>
        <p>Claiming as <strong>{{ current_user['name'] }}</strong> ({{ current_user['phone'] }}). This will share your contact with the donor.</p>
        <form method="post" action="{{ url_for('claim', donation_id=d['id']) }}">
          <button type="submit" class="btn btn-primary">Claim this donation</button>
        </form>
      {% elif current_user %}
        <p>Only NGO accounts can claim donations.</p>
      {% else %}
        <p><a href="{{ url_for('login', next=request.path) }}">Log in as an NGO</a> to claim this donation, or <a href="{{ url_for('register') }}">sign up</a> if you don't have an account yet.</p>
      {% endif %}
    </div>
  {% elif d['status'] == 'claimed' %}
    <div class="claim-box claimed-box">
      <h2>Claimed by {{ d['claimer_name'] }}</h2>
      <p>Contact: {{ d['claimer_phone'] }} \u00b7 claimed at {{ d['claimed_at'] }}</p>
      {% if current_user and current_user['id'] in [d['donor_id'], d['claimed_by_id']] %}
        <form method="post" action="{{ url_for('complete', donation_id=d['id']) }}">
          <button type="submit" class="btn btn-ghost">Mark as picked up</button>
        </form>
      {% endif %}
    </div>
  {% else %}
    <p class="completed-note">This donation was picked up. Thank you for closing the loop.</p>
  {% endif %}
</section>
{% endblock %}"""

# about.html
about_html = """{% extends "base.html" %}
{% block title %}About \u2014 Anndaan{% endblock %}
{% block content %}
<section class="form-page">
  <h1>About Anndaan</h1>
  <p class="form-sub">A food donation platform connecting surplus with those who need it.</p>

  <div class="about-section">
    <h2>Our Mission</h2>
    <p>Anndaan aims to reduce food waste and fight hunger by creating a seamless bridge between food donors and NGOs. Our platform enables restaurants, households, and event caterers to share surplus food, ensuring it reaches those who need it before it spoils.</p>

    <h2>Developers</h2>
    <div class="developer-grid">
      <div class="developer-card">
        <h3>Saksham Suryawanshi</h3>
        <p>Lead Developer</p>
      </div>
      <div class="developer-card">
        <h3>Samyak Fulmali</h3>
        <p>Full-Stack Engineer</p>
      </div>
      <div class="developer-card">
        <h3>Shivam Patil</h3>
        <p>Backend Specialist</p>
      </div>
      <div class="developer-card">
        <h3>Tanzil Saad Ansari</h3>
        <p>DevOps & Infrastructure</p>
      </div>
      <div class="developer-card">
        <h3>Yash Dhande</h3>
        <p>Frontend Engineer</p>
      </div>
    </div>

    <div class="credits">
      <p>Built with \u2764 at <strong>Jhulelal Institute of Technology</strong></p>
      <p>Version 2.0 \u2014 Prototype to Production</p>
    </div>
  </div>

  <div class="impact-grid" style="margin-top: 40px;">
    <div class="impact-card">
      <span class="impact-icon coral">\u2668</span>
      <strong>{{ (stats['completed'] or 0) * 20 + 128 }}</strong>
      <span>meals shared</span>
    </div>
    <div class="impact-card">
      <span class="impact-icon green">\u2661</span>
      <strong>{{ (stats['completed'] or 0) * 8 + 46 }}</strong>
      <span>people helped</span>
    </div>
    <div class="impact-card">
      <span class="impact-icon gold">\u2726</span>
      <strong>{{ (stats['total'] or 0) * 3 + 18 }} kg</strong>
      <span>food rescued</span>
    </div>
  </div>
</section>
{% endblock %}"""

# login.html
login_html = """{% extends "base.html" %}
{% block title %}Log in \u2014 Anndaan{% endblock %}
{% block content %}
<section class="form-page">
  <h1>Log in</h1>
  <p class="form-sub">Welcome back. Log in to donate or claim food.</p>

  <form method="post" class="form">
    <label>
      Email
      <input type="email" name="email" value="{{ email }}" placeholder="johnsmith@gmail.com" required autofocus>
    </label>
    <label>
      Password
      <input type="password" name="password" placeholder="pass@123" required>
    </label>
    <button type="submit" class="btn btn-primary">Log in</button>
  </form>

  <p class="form-footer-note">No account yet? <a href="{{ url_for('register') }}">Sign up</a>.</p>
</section>
{% endblock %}"""

# register.html
register_html = """{% extends "base.html" %}
{% block title %}Sign up \u2014 Anndaan{% endblock %}
{% block content %}
<section class="form-page">
  <h1>Create an account</h1>
  <p class="form-sub">Sign up as a donor to post surplus food, or as an NGO to claim it.</p>

  <form method="post" class="form">
    <label>
      Account type
      <select name="role" required>
        <option value="">Select</option>
        <option value="donor" {% if form.get('role')=='donor' %}selected{% endif %}>Donor \u2014 restaurant, kitchen, household</option>
        <option value="ngo" {% if form.get('role')=='ngo' %}selected{% endif %}>NGO \u2014 pick up and distribute food</option>
      </select>
    </label>

    <label>
      Name / organisation
      <input type="text" name="name" value="{{ form.get('name','') }}" placeholder="John Smith" required>
    </label>

    <label>
      Contact number
      <input type="tel" name="phone" value="{{ form.get('phone','') }}" placeholder="1234567890" required>
    </label>

    <label>
      Email
      <input type="email" name="email" value="{{ form.get('email','') }}" placeholder="johnsmith@gmail.com" required>
    </label>

    <label>
      Password
      <input type="password" name="password" placeholder="pass@123" required minlength="6">
    </label>

    <button type="submit" class="btn btn-primary">Sign up</button>
  </form>

  <p class="form-footer-note">Already have an account? <a href="{{ url_for('login') }}">Log in</a>.</p>
</section>
{% endblock %}"""

# Write all files with explicit UTF-8 encoding
templates = {
    'base.html': base_html,
    'index.html': index_html,
    'browse.html': browse_html,
    'donate.html': donate_html,
    'detail.html': detail_html,
    'about.html': about_html,
    'login.html': login_html,
    'register.html': register_html,
}

template_dir = 'C:/Users/JOHN/Documents/andc2/templates'
for fname, content in templates.items():
    path = os.path.join(template_dir, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {fname}')

print('All templates rewritten successfully!')