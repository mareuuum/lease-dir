import json, glob, os
BASE = "https://example.pages.dev"
items=[]
for f in glob.glob("data/normalized/*.json"):
    cat = os.path.splitext(os.path.basename(f))[0]
    data = json.load(open(f, encoding="utf-8"))
    for row in data[-10:]:
        items.append((cat,row))
rss = ["<?xml version='1.0' encoding='UTF-8'?>","<rss version='2.0'><channel>",
       f"<title>新着ディレクトリ</title>", f"<link>{BASE}</link>", "<description>自動生成フィード</description>"]
for cat,row in items[:20]:
    link = f"{BASE}/{cat}/{row['id']}.html"
    rss += [f"<item><title>{row.get('name','')}</title><link>{link}</link><description>{row.get('summary','')}</description></item>"]
rss.append("</channel></rss>")
os.makedirs("site", exist_ok=True)
open("site/feed.xml","w",encoding="utf-8").write("\n".join(rss))
print("rss built", len(items))
