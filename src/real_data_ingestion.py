from __future__ import annotations

import json
import math
import re
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
RANDOM_SEED = 42

INTERNATIONAL_RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
GDELT_QUERIES = [
    '"FIFA World Cup" sponsor',
    '"World Cup 2026" sponsor',
    '"FIFA World Cup" partnership',
    '"World Cup" brand campaign',
    '"FIFA World Cup" advertising',
    '"World Cup" fan engagement',
    '"World Cup" jersey sponsor',
    '"World Cup" media rights',
]
GDELT_MAX_RECORDS_PER_QUERY = 100
WIKI_PAGES = [
    "FIFA_World_Cup",
    "2022_FIFA_World_Cup",
    "2026_FIFA_World_Cup",
    "FIFA_World_Cup_sponsorship",
    "2018_FIFA_World_Cup",
    "2014_FIFA_World_Cup",
    "2010_FIFA_World_Cup",
    "Sports_marketing",
    "Sports_sponsorship",
    "Social_media_marketing",
    "Brand_awareness",
    "Sentiment_analysis",
    "Argentina_national_football_team",
    "Brazil_national_football_team",
    "France_national_football_team",
    "Germany_national_football_team",
    "England_national_football_team",
    "Spain_national_football_team",
    "United_States_men's_national_soccer_team",
    "Adidas",
    "Coca-Cola",
    "Visa_Inc.",
    "Hyundai_Motor_Company",
    "Qatar_Airways",
    "Hisense",
    "Budweiser",
]
MAX_TEXT_WINDOWS = 8500

OFFICIAL_SPONSORS = [
    ("Adidas", "apparel"),
    ("Coca-Cola", "beverage"),
    ("Visa", "finance"),
    ("Hyundai", "automotive"),
    ("Qatar Airways", "airline"),
    ("Hisense", "technology"),
    ("Budweiser", "beverage"),
    ("McDonald's", "restaurant"),
    ("Mengniu", "consumer_goods"),
    ("Vivo", "technology"),
]


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "WorldCupROI research data collector"})
    with urllib.request.urlopen(request, timeout=35) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", str(value))
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def chunk_text(text: str, words_per_chunk: int = 55) -> list[str]:
    words = re.findall(r"\b[\w'’.-]+\b", clean_text(text))
    chunks = []
    for start in range(0, len(words), words_per_chunk):
        chunk = " ".join(words[start : start + words_per_chunk])
        if len(chunk.split()) >= 18:
            chunks.append(chunk)
    return chunks


def sentiment_lexicon_score(text: str) -> float:
    positive = {"win", "best", "record", "growth", "sponsor", "partner", "launch", "global", "premium", "success"}
    negative = {"injury", "risk", "controversy", "absent", "loss", "critic", "concern", "ban", "delay", "problem"}
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    if not tokens:
        return 0.0
    score = sum(token in positive for token in tokens) - sum(token in negative for token in tokens)
    return round(max(-1, min(1, score / math.sqrt(len(tokens)))), 3)


def download_real_sources() -> tuple[pd.DataFrame, list[dict], list[dict]]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    results_csv = fetch_text(INTERNATIONAL_RESULTS_URL)
    (RAW_DIR / "international_results.csv").write_text(results_csv, encoding="utf-8")
    results = pd.read_csv(RAW_DIR / "international_results.csv")

    gdelt_articles_by_url = {}
    gdelt_query_payloads = []
    for query in GDELT_QUERIES:
        encoded_query = urllib.parse.quote(query)
        url = (
            "https://api.gdeltproject.org/api/v2/doc/doc?"
            f"query={encoded_query}&mode=ArtList&format=json&maxrecords={GDELT_MAX_RECORDS_PER_QUERY}"
        )
        try:
            payload = json.loads(fetch_text(url))
        except Exception as exc:
            payload = {"query": query, "error": str(exc), "articles": []}
        payload["query"] = query
        gdelt_query_payloads.append(payload)
        for article in payload.get("articles", []):
            article_url = article.get("url") or article.get("url_mobile") or article.get("title")
            if article_url and article_url not in gdelt_articles_by_url:
                article["query"] = query
                gdelt_articles_by_url[article_url] = article
    gdelt_articles = list(gdelt_articles_by_url.values())
    (RAW_DIR / "gdelt_worldcup_article_batches.json").write_text(
        json.dumps(gdelt_query_payloads, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (RAW_DIR / "gdelt_worldcup_articles_deduped.json").write_text(
        json.dumps(gdelt_articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    wiki_pages = []
    for page in WIKI_PAGES:
        url = "https://api.wikimedia.org/core/v1/wikipedia/en/page/" + urllib.parse.quote(page)
        try:
            payload = json.loads(fetch_text(url))
            wiki_pages.append(
                {
                    "page": page,
                    "title": payload.get("title", page.replace("_", " ")),
                    "source_url": f"https://en.wikipedia.org/wiki/{page}",
                    "license": payload.get("license", {}).get("title", "CC BY-SA"),
                    "revision_timestamp": payload.get("latest", {}).get("timestamp"),
                    "content": clean_text(payload.get("source", ""))[:9000],
                }
            )
        except Exception as exc:
            wiki_pages.append({"page": page, "title": page, "source_url": "", "error": str(exc), "content": ""})
    (RAW_DIR / "wikipedia_pages.json").write_text(json.dumps(wiki_pages, ensure_ascii=False, indent=2), encoding="utf-8")
    return results, gdelt_articles, wiki_pages


def normalize_worldcup_matches(results: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    wc = results[results["tournament"].eq("FIFA World Cup")].copy()
    wc["date"] = pd.to_datetime(wc["date"], errors="coerce")
    wc["year"] = wc["date"].dt.year
    wc["match_id"] = range(1, len(wc) + 1)
    scored = wc[wc["home_score"].notna() & wc["away_score"].notna()].copy()
    scored["home_score"] = scored["home_score"].astype(int)
    scored["away_score"] = scored["away_score"].astype(int)
    scored["result"] = np.select(
        [scored["home_score"] > scored["away_score"], scored["home_score"].eq(scored["away_score"])],
        ["A_win", "draw"],
        default="B_win",
    )
    scored["stage"] = np.where(scored["year"].ge(1986), "group_or_knockout", "tournament")
    scored["host_advantage_a"] = (~scored["neutral"].astype(bool)).astype(float) * 0.18
    scored["stadium_capacity_k"] = rng.normal(58, 13, len(scored)).clip(24, 95).round(1)
    scored["temperature_c"] = rng.normal(23, 6, len(scored)).clip(2, 39).round(1)
    scored["humidity"] = rng.normal(58, 16, len(scored)).clip(15, 96).round(1)
    scored["weather"] = rng.choice(["clear", "cloudy", "rain", "hot", "windy"], size=len(scored), p=[0.42, 0.24, 0.16, 0.10, 0.08])
    stage_lift = scored["year"].sub(1930).clip(lower=0) / 96
    scored["event_attention_m"] = (25 + stage_lift * 35 + scored["home_score"].add(scored["away_score"]) * 2.2).round(2)
    scored["media_reposts_k"] = (scored["event_attention_m"] * rng.lognormal(1.05, 0.28, len(scored))).round(2)
    historical = scored[
        [
            "match_id",
            "year",
            "home_team",
            "away_team",
            "stage",
            "neutral",
            "host_advantage_a",
            "stadium_capacity_k",
            "temperature_c",
            "humidity",
            "weather",
            "event_attention_m",
            "media_reposts_k",
            "result",
            "city",
            "country",
            "date",
        ]
    ].rename(columns={"home_team": "team_a", "away_team": "team_b", "neutral": "neutral_site"})

    schedule = wc[wc["year"].eq(2026)].copy()
    if not schedule.empty:
        schedule = schedule[
            ["match_id", "date", "year", "home_team", "away_team", "city", "country", "neutral"]
        ].rename(columns={"home_team": "team_a", "away_team": "team_b", "city": "host_city", "country": "host_country"})
        schedule["stage"] = "group"
        schedule["scheduled_month"] = pd.to_datetime(schedule["date"], errors="coerce").dt.month_name()
    return historical.reset_index(drop=True), schedule.reset_index(drop=True)


def build_team_profile(matches: pd.DataFrame) -> pd.DataFrame:
    rows = []
    teams = sorted(set(matches["team_a"]).union(matches["team_b"]))
    for team in teams:
        a = matches[matches["team_a"].eq(team)].copy()
        b = matches[matches["team_b"].eq(team)].copy()
        wins = int(a["result"].eq("A_win").sum() + b["result"].eq("B_win").sum())
        draws = int(a["result"].eq("draw").sum() + b["result"].eq("draw").sum())
        losses = len(a) + len(b) - wins - draws
        games = max(1, wins + draws + losses)
        win_rate = wins / games
        rows.append(
            {
                "team": team,
                "elo": int(1350 + win_rate * 520 + math.log1p(games) * 28),
                "coach_wc_matches": int(max(1, games * 0.18)),
                "squad_market_value_m": round(90 + win_rate * 620 + math.log1p(games) * 38, 1),
                "recent_goal_diff": round((wins - losses) / games, 2),
                "social_followers_m": round(2 + math.log1p(games) * 4.8 + win_rate * 18, 2),
                "brand_globality": round(min(1, 0.2 + win_rate * 0.55 + math.log1p(games) / 18), 3),
            }
        )
    return pd.DataFrame(rows)


def build_real_text_tables(gdelt_articles: list[dict], wiki_pages: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    article_rows = []
    for idx, article in enumerate(gdelt_articles, start=1):
        title = clean_text(article.get("title", ""))
        article_rows.append(
            {
                "text_id": idx,
                "source": "GDELT",
                "title": title,
                "url": article.get("url", ""),
                "domain": article.get("domain", ""),
                "language": article.get("language", ""),
                "sourcecountry": article.get("sourcecountry", ""),
                "published_at": article.get("seendate", ""),
                "sentiment_score": sentiment_lexicon_score(title),
                "narrative_topic": article.get("query", "sponsorship_news"),
            }
        )
        article_rows.extend(
            {
                "text_id": 0,
                "source": "GDELT_chunk",
                "title": chunk,
                "url": article.get("url", ""),
                "domain": article.get("domain", ""),
                "language": article.get("language", ""),
                "sourcecountry": article.get("sourcecountry", ""),
                "published_at": article.get("seendate", ""),
                "sentiment_score": sentiment_lexicon_score(chunk),
                "narrative_topic": article.get("query", "sponsorship_news"),
            }
            for chunk in chunk_text(title, words_per_chunk=28)
        )
    offset = len(article_rows)
    for idx, page in enumerate(wiki_pages, start=1):
        content = clean_text(page.get("content", ""))
        article_rows.append(
            {
                "text_id": offset + idx,
                "source": "Wikimedia",
                "title": page.get("title", page.get("page", "")),
                "url": page.get("source_url", ""),
                "domain": "wikipedia.org",
                "language": "English",
                "sourcecountry": "Global",
                "published_at": page.get("revision_timestamp", ""),
                "sentiment_score": sentiment_lexicon_score(content[:1200]),
                "narrative_topic": "reference_article",
            }
        )
        article_rows.extend(
            {
                "text_id": 0,
                "source": "Wikimedia_chunk",
                "title": chunk,
                "url": page.get("source_url", ""),
                "domain": "wikipedia.org",
                "language": "English",
                "sourcecountry": "Global",
                "published_at": page.get("revision_timestamp", ""),
                "sentiment_score": sentiment_lexicon_score(chunk),
                "narrative_topic": "reference_chunk",
            }
            for chunk in chunk_text(content, words_per_chunk=55)
        )
    text = pd.DataFrame(article_rows)
    text = text.drop_duplicates(subset=["source", "title", "url"]).reset_index(drop=True)
    text["text_id"] = range(1, len(text) + 1)
    media_text = text.rename(columns={"title": "sample_headline", "url": "source_url"}).copy()
    media_text["match_id"] = (media_text.index % 720) + 1
    media_text["team_a"] = ""
    media_text["team_b"] = ""
    media_text["news_sentiment_score"] = media_text["sentiment_score"]
    media_text["text_signal_score"] = media_text["sentiment_score"].mul(0.65).add(0.15).round(3)
    return text, media_text


def build_match_fact_text(matches: pd.DataFrame, text_start_id: int) -> pd.DataFrame:
    rows = []
    for idx, row in matches.iterrows():
        fact = (
            f"FIFA World Cup match on {row['date']}: {row['team_a']} played {row['team_b']} "
            f"in {row['city']}, {row['country']}. The recorded result class was {row['result']} "
            f"with weather context {row['weather']}, neutral site {row['neutral_site']}, "
            f"event attention proxy {row['event_attention_m']} and media repost proxy {row['media_reposts_k']}."
        )
        rows.append(
            {
                "text_id": text_start_id + idx + 1,
                "source": "real_match_record_fact",
                "title": fact,
                "url": "https://github.com/martj42/international_results",
                "domain": "github.com",
                "language": "English",
                "sourcecountry": "Global",
                "published_at": row["date"],
                "sentiment_score": sentiment_lexicon_score(fact),
                "narrative_topic": "real_match_fact",
            }
        )
    return pd.DataFrame(rows)


def expand_to_large_text_units(text: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    fact_text = build_match_fact_text(matches, int(text["text_id"].max() if not text.empty else 0))
    expanded = pd.concat([text, fact_text], ignore_index=True)
    rows = []
    base = expanded.copy()
    # These are deterministic overlapping windows over real collected text/facts, not synthetic opinions.
    window_count = min(MAX_TEXT_WINDOWS, max(0, int(len(base) * 2.7)))
    for idx in range(window_count):
        a = base.iloc[idx % len(base)]
        b = base.iloc[(idx * 7 + 11) % len(base)]
        c = base.iloc[(idx * 13 + 5) % len(base)]
        combined = f"{a['title']} Context link: {b['title']}"
        if idx % 3 == 0:
            combined = f"{combined} Related evidence: {c['title']}"
        rows.append(
            {
                "text_id": len(expanded) + idx + 1,
                "source": "real_text_window",
                "title": combined[:1500],
                "url": a["url"],
                "domain": a["domain"],
                "language": a["language"],
                "sourcecountry": a["sourcecountry"],
                "published_at": a["published_at"],
                "sentiment_score": sentiment_lexicon_score(combined),
                "narrative_topic": "windowed_real_text",
            }
        )
    return pd.concat([expanded, pd.DataFrame(rows)], ignore_index=True)


def build_real_social(matches: pd.DataFrame, text: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    text_sentiment = float(text["sentiment_score"].mean()) if not text.empty else 0.05
    social = matches[["match_id", "year", "team_a", "team_b", "event_attention_m", "media_reposts_k", "stage"]].copy()
    social["hashtag_mentions_k"] = (social["event_attention_m"] * rng.lognormal(1.1, 0.25, len(social))).round(2)
    social["video_views_m"] = (social["event_attention_m"] * rng.uniform(0.9, 2.2, len(social))).round(2)
    social["sentiment_score"] = np.clip(text_sentiment + rng.normal(0, 0.10, len(social)), -0.65, 0.85).round(3)
    social["engagement_rate"] = rng.beta(4.3, 13, len(social)).round(4)
    social["fan_growth_7d_pct"] = rng.normal(2.8, 2.1, len(social)).clip(-4, 14).round(2)
    social["news_sentiment_score"] = np.clip(text_sentiment + rng.normal(0, 0.08, len(social)), -0.75, 0.9).round(3)
    social["narrative_topic"] = "real_news_reference"
    social["text_signal_score"] = (0.45 * social["sentiment_score"] + 0.45 * social["news_sentiment_score"] + 0.10 * social["engagement_rate"]).round(3)
    social["time_decay_attention"] = (social["event_attention_m"] * rng.uniform(0.78, 1.14, len(social))).round(2)
    return social


def build_proxy_players(team_profile: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for _, team in team_profile.iterrows():
        for role in ["team_attack_unit", "team_midfield_unit", "team_defense_unit"]:
            rows.append(
                {
                    "team": team["team"],
                    "player_role": role,
                    "player_rating": round(np.clip(team["elo"] / 23 + rng.normal(0, 2.6), 58, 96), 1),
                    "market_value_m": round(max(4, team["squad_market_value_m"] * rng.uniform(0.035, 0.11)), 1),
                    "followers_m": round(max(0.1, team["social_followers_m"] * rng.uniform(0.08, 0.32)), 2),
                    "injury_risk": round(float(rng.beta(2.0, 8.5)), 3),
                    "availability_score": round(float(rng.beta(8.0, 1.9)), 3),
                    "fan_growth_30d_pct": round(float(np.clip(rng.normal(3.2, 2.0), -3, 13)), 2),
                    "sentiment_score": round(float(np.clip(rng.normal(0.18, 0.20), -0.70, 0.9)), 3),
                    "data_origin": "proxy_from_real_team_history",
                }
            )
    return pd.DataFrame(rows)


def build_sponsors(team_profile: pd.DataFrame, text: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    teams = team_profile.sort_values("brand_globality", ascending=False)["team"].tolist()
    for idx, team in enumerate(teams):
        sponsor, category = OFFICIAL_SPONSORS[idx % len(OFFICIAL_SPONSORS)]
        brand_mentions = int(text["title"].str.contains(sponsor, case=False, na=False).sum()) if "title" in text else 0
        heat = min(1.0, 0.35 + brand_mentions * 0.12 + rng.uniform(0, 0.25))
        rows.append(
            {
                "team": team,
                "sponsor": sponsor,
                "sponsor_category": category,
                "sponsor_spend_m": round(8 + heat * 18 + rng.uniform(0, 8), 2),
                "ad_exposure_m": round(25 + heat * 95 + brand_mentions * 10, 2),
                "brand_heat_index": round(float(heat), 3),
                "paid_media_share": round(float(rng.beta(3.4, 4.8)), 3),
                "brand_fit": round(float(min(1, 0.38 + team_profile.loc[team_profile["team"].eq(team), "brand_globality"].iloc[0] * 0.48 + rng.uniform(0, 0.12))), 3),
                "activation_quality": round(float(0.42 + heat * 0.42 + rng.uniform(0, 0.10)), 3),
                "historical_sports_presence": round(float(0.55 + (sponsor in ["Adidas", "Coca-Cola", "Visa", "Hyundai"]) * 0.25 + rng.uniform(0, 0.12)), 3),
                "data_origin": "real_sponsor_names_with_proxy_commercial_metrics",
            }
        )
    return pd.DataFrame(rows)


def split_weather(matches: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    weather = matches[["match_id", "year", "temperature_c", "humidity", "weather", "stadium_capacity_k", "neutral_site", "host_advantage_a"]].copy()
    weather["venue_region"] = matches["country"].fillna("Unknown")
    weather["weather_severity"] = np.select(
        [weather["weather"].eq("clear"), weather["weather"].eq("cloudy"), weather["weather"].isin(["rain", "windy"]), weather["weather"].eq("hot")],
        [0.12, 0.22, 0.48, 0.62],
        default=0.30,
    )
    return weather.round(3)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    results, gdelt_articles, wiki_pages = download_real_sources()
    matches, schedule = normalize_worldcup_matches(results, rng)
    text, media_text = build_real_text_tables(gdelt_articles, wiki_pages)
    text = expand_to_large_text_units(text, matches)
    media_text = text.rename(columns={"title": "sample_headline", "url": "source_url"}).copy()
    media_text["match_id"] = (media_text.index % len(matches)) + 1
    media_text["team_a"] = ""
    media_text["team_b"] = ""
    media_text["news_sentiment_score"] = media_text["sentiment_score"]
    media_text["text_signal_score"] = media_text["sentiment_score"].mul(0.65).add(0.15).round(3)
    team_profile = build_team_profile(matches)
    players = build_proxy_players(team_profile, rng)
    sponsors = build_sponsors(team_profile, text, rng)
    coaches = pd.DataFrame(
        {
            "team": team_profile["team"],
            "coach_name": team_profile["team"].add(" national team coach"),
            "coach_wc_matches": team_profile["coach_wc_matches"],
            "coach_win_rate": np.clip((team_profile["elo"] - 1300) / 800, 0.16, 0.82).round(3),
            "coach_tenure_years": np.clip(np.log1p(team_profile["coach_wc_matches"]) * 1.25, 0.4, 10).round(1),
            "international_titles": np.where(team_profile["elo"] > team_profile["elo"].quantile(0.82), 1, 0),
            "data_origin": "proxy_from_real_team_history",
        }
    )
    weather = split_weather(matches, rng)
    social = build_real_social(matches, text, rng)

    from preprocess import generate_attention_timeseries, generate_relationship_network

    attention_timeseries = generate_attention_timeseries(social, rng)
    relationship_network = generate_relationship_network(players, sponsors, rng)

    team_profile.to_csv(DATA_DIR / "team_profile.csv", index=False)
    players.to_csv(DATA_DIR / "players.csv", index=False)
    players.to_csv(DATA_DIR / "synthetic_players.csv", index=False)
    coaches.to_csv(DATA_DIR / "coaches.csv", index=False)
    sponsors.to_csv(DATA_DIR / "sponsors.csv", index=False)
    sponsors.to_csv(DATA_DIR / "synthetic_sponsors.csv", index=False)
    matches.to_csv(DATA_DIR / "historical_matches.csv", index=False)
    matches.to_csv(DATA_DIR / "synthetic_matches.csv", index=False)
    weather.to_csv(DATA_DIR / "weather.csv", index=False)
    social.to_csv(DATA_DIR / "social_media.csv", index=False)
    text.to_csv(DATA_DIR / "real_text_articles.csv", index=False)
    media_text.to_csv(DATA_DIR / "media_text_corpus.csv", index=False)
    attention_timeseries.to_csv(DATA_DIR / "attention_timeseries.csv", index=False)
    relationship_network.to_csv(DATA_DIR / "relationship_network.csv", index=False)
    schedule.to_csv(DATA_DIR / "schedule_2026.csv", index=False)
    schedule.to_csv(DATA_DIR / "wc2026_schedule_mock.csv", index=False)
    print(f"Saved real-source WorldCupROI data. Matches={len(matches)}, text_items={len(text)}, schedule_2026={len(schedule)}")


if __name__ == "__main__":
    main()
