import json, os, re

OUT = "data/raw/coworking.json"

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9一-龥ぁ-んァ-ンー]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "item"

def run():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    data = []
    for name, url, addr, price, desc in [
        ("アルファワークス", "https://example.com/spaces/alpha", "愛知県名古屋市中区1-2-3", "¥500/時〜", "駅近・会議室あり"),
        ("ブラボーコワーキング", "https://example.com/spaces/bravo", "東京都渋谷区3-2-1", "¥800/時〜", "登記OK・ドロップイン"),
    ]:
        data.append({
            "id": slugify(f"{name}-{url}"),
            "source": "example.com",
            "name": name,
            "url": url,
            "category": "coworking",
            "address": addr,
            "price_text": price,
            "description_raw": desc
        })
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT} ({len(data)} records)")

if __name__ == "__main__":
    run()
