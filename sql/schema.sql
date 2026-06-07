CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    year INTEGER,
    team_a TEXT,
    team_b TEXT,
    stage TEXT,
    result TEXT
);

CREATE TABLE sponsors (
    team TEXT,
    sponsor TEXT,
    sponsor_category TEXT,
    sponsor_spend_m REAL,
    ad_exposure_m REAL,
    brand_heat_index REAL,
    brand_fit REAL,
    activation_quality REAL
);

CREATE TABLE social_media (
    match_id INTEGER,
    hashtag_mentions_k REAL,
    video_views_m REAL,
    engagement_rate REAL,
    fan_growth_7d_pct REAL,
    news_sentiment_score REAL,
    text_signal_score REAL
);

CREATE TABLE roi_predictions (
    match_id INTEGER,
    predicted_roi REAL,
    roi_lift_vs_spend REAL,
    media_exposure_index REAL,
    commercial_momentum_score REAL,
    injury_risk_score REAL,
    sponsor_team_fit_score REAL
);
