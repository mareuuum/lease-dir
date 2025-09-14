import json, os, glob
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
tpl_listing = env.get_template("listing.html")
tpl_index   = env.get_template("index.html")
tpl_home    = env.get_template("home.html")

def build_category(cat):
    path = f"data/normalized/{cat}.json"
    if not os.path.exists(path): return
    data = json.load(open(path, encoding="utf-8"))
    os.makedirs(f"site/{cat}", exist_ok=True)
    for row in data:
        open(f"site/{cat}/{row['id']}.html","w",encoding="utf-8").write(tpl_listing.render(item=row))
    open(f"site/{cat}/index.html","w",encoding="utf-8").write(tpl_index.render(items=data, category=cat, title=f"{cat.title()} ディレクトリ"))

def build_home():
    cats = []
    for f in glob.glob("data/normalized/*.json"):
        cat = os.path.splitext(os.path.basename(f))[0]
        cnt = len(json.load(open(f, encoding="utf-8")))
        cats.append((cat, cnt))
    os.makedirs("site", exist_ok=True)
    open("site/index.html","w",encoding="utf-8").write(tpl_home.render(categories=cats, title="リース/レンタル ディレクトリ"))

if __name__=="__main__":
    os.makedirs("site", exist_ok=True)
    build_category("coworking")
    build_home()
