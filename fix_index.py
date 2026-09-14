index_content = """{% extends "base.html" %}
{% block title %}Home · Anndaan{% endblock %}
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
    <a class="action-card action-card-primary" href="{{ url_for('donate') if current_user and current_user['role'] == 'donor' else url_for('register') }}"><span class="action-symbol">＋</span><strong>Donate food</strong><small>Share surplus nearby</small></a>
    <a class="action-card" href="{{ url_for('browse') }}"><span class="action-symbol">⌖</span><strong>Find a meal</strong><small>{{ stats['available'] or 0 }} available now</small></a>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Your community</p><h2>Impact at a glance</h2></div><span class="trend">This month ↗</span></div>
  <div class="impact-grid">
    <div class="impact-card"><span class="impact-icon coral">♨</span><strong>{{ (stats['completed'] or 0) * 20 + 128 }}</strong><span>meals shared</span></div>
    <div class="impact-card"><span class="impact-icon green">♡</span><strong>{{ (stats['completed'] or 0) * 8 + 46 }}</strong><span>people helped</span></div>
    <div class="impact-card"><span class="impact-icon gold">✦</span><strong>{{ (stats['total'] or 0) * 3 + 18 }} kg</strong><span>food rescued</span></div>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Live in your area</p><h2>Nearby donations</h2></div><a class="text-link" href="{{ url_for('browse') }}">View all →</a></div>
  <div class="map-panel"><div class="map-copy"><span class="map-badge">● LIVE</span><h3>Good food is close by</h3><p>Discover donations and pickup points around you.</p><a class="btn btn-dark" href="{{ url_for('browse') }}">Explore nearby</a></div><div class="map-art" aria-label="Map showing nearby donation activity"><span class="map-road road-one"></span><span class="map-road road-two"></span><span class="map-pin pin-one">♨</span><span class="map-pin pin-two">♨</span><span class="map-pin pin-three">●</span><span class="map-you">You</span></div></div>

  <div class="section-heading"><div><p class="eyebrow">Keep the loop moving</p><h2>Active donation</h2></div></div>
  <div class="status-card"><div class="status-top"><span class="status-dot"></span><div><strong>{% if stats['claimed'] %}Pickup in progress{% else %}Ready for a helping hand{% endif %}</strong><p>{% if stats['claimed'] %}A volunteer is on the way{% else %}Every donation starts with you{% endif %}</p></div><span class="status-arrow">→</span></div><div class="timeline"><span class="done">Posted</span><span class="current">Matched</span><span class="picked up">Picked up</span><span class="delivered">Delivered</span></div></div>
</section>

{% if recent %}<section class="recent">
  <div class="section-heading"><div><p class="eyebrow">Fresh from the community</p><h2>Just posted</h2></div><a class="text-link" href="{{ url_for('browse') }}">See all →</a></div>
  <div class="card-grid">
    {% for d in recent %}
    <a class="card" href="{{ url_for('donation_detail', donation_id=d['id']) }}">
      <span class="tag tag-{{ d['food_type'] }}">{{ d['food_type'] }}</span>
      <h3>{{ d['food_item'] }}</h3>
      <p class="card-meta">{{ d['quantity'] }} &middot; pickup by {{ d['expiry_time'] }}</p>
      <p class="card-loc">{{ d['pickup_address'] }}</p>
      <p class="card-donor">from {{ d['donor_name'] }}</p>
    </a>
    {% endfor %}
  </div>
</section>
{% endif %}
{% endblock %}
"""

with open('C:/Users/JOHN/Documents/andc2/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)
print('index.html written successfully')