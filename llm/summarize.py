import json, sys, os
def run(src, dst):
    data = json.load(open(src, encoding="utf-8"))
    for row in data:
        row["summary"] = " / ".join(filter(None, [
            f"料金目安: {row.get('price_text','')}".strip(),
            f"所在地: {row.get('address','')}".strip(),
            f"特徴: {row.get('description_raw','')}".strip()
        ]))[:120]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    json.dump(data, open(dst,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Wrote", dst, len(data))
if __name__=="__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    run(src, dst)
