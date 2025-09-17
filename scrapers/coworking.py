import json, os, re, time, requests

OUT = "data/raw/coworking.json"

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
# 例：東京都（boundary ISOコードでも可）。全国にするなら area フィルタを外す。
# エリアIDの簡便指定: area["ISO3166-2"="JP-13"];  # 東京都
QUERY = r"""
[out:json][timeout:60];
area["ISO3166-2"="JP-13"]->.searchArea;
(
  node["amenity"="co-working_space"](area.searchArea);
  way["amenity"="co-working_space"](area.searchArea);
  relation["amenity"="co-working_space"](area.searchArea);

  node["office"="coworking"](area.searchArea);
  way["office"="coworking"](area.searchArea);
  relation["office"="coworking"](area.searchArea);
);
out tags center;
"""

UA = "lease-dir-bot/0.1 (+https://github.com/mareuuum/lease-dir) contact: mare_uuum@example.com"

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9一-龥ぁ-んァ-ンー]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "item"

def norm_addr(tags):
    parts = [tags.get(k,"") for k in ("addr:province","addr:city","addr:suburb","addr:quarter","addr:neighbourhood","addr:district","addr:town","addr:village","addr:hamlet","addr:street","addr:housenumber")]
    s = "".join([p for p in parts if p])
    return s or tags.get("addr:full","")

def run():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    # Overpass 叩く
    res = requests.post(OVERPASS_URL, data=QUERY.encode("utf-8"), headers={"User-Agent": UA})
    res.raise_for_status()
    j = res.json()

    data = []
    for el in j.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:ja") or tags.get("alt_name") or "名称不明"
        url  = tags.get("website") or tags.get("contact:website") or tags.get("url") or ""
        addr = norm_addr(tags)
        price = tags.get("fee") or tags.get("charge") or ""
        desc  = tags.get("description") or ""

        # 緯度経度（node は lat/lon、way/relation は center）
        if "lat" in el and "lon" in el:
            lat, lon = el["lat"], el["lon"]
        else:
            c = el.get("center") or {}
            lat, lon = c.get("lat"), c.get("lon")

        item = {
            "id": slugify(f"{name}-{url or el.get('id')}"),
            "source": "OpenStreetMap (Overpass)",
            "name": name,
            "url": url,
            "category": "coworking",
            "address": addr,
            "price_text": price,
            "description_raw": desc,
            "lat": lat,
            "lon": lon,
        }
        data.append(item)

    # 保存
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote {OUT} ({len(data)} records)")

if __name__ == "__main__":
    # API優先度の都合で軽く待機（礼儀）
    time.sleep(1.0)
    run()
