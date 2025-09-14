import os, datetime
BASE = "https://example.pages.dev"
urls=[]
for r,_,fs in os.walk("site"):
    for f in fs:
        if f.endswith(".html"):
            path = os.path.join(r,f).replace("site","").replace("\\","/")
            if not path.startswith("/"):
                path = "/" + path
            urls.append(BASE + path)
today = datetime.date.today().isoformat()
out = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(set(urls)):
    out.append(f"<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq></url>")
out.append("</urlset>")
os.makedirs("site", exist_ok=True)
open("site/sitemap.xml","w",encoding="utf-8").write("\n".join(out))
print("sitemap built", len(urls))
