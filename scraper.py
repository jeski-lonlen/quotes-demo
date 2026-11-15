# -*- coding: utf-8 -*-
"""
抓取 quotes.toscrape.com 的名言，存成 quotes.csv

四步：请求 -> 解析 -> 翻页 -> 保存
运行：python scraper.py
"""
import csv
import random
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com/page/{}/"
HEADERS = {"User-Agent": "quotes-demo/1.0 (learning project; local)"}
OUT = Path(__file__).with_name("quotes.csv")


def fetch(page, retries=3):
    """带重试和指数退避的请求；失败返回 None，不抛异常。"""
    url = BASE.format(page)
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                return r.text
            print(f"  状态码 {r.status_code}: {url}")
        except requests.RequestException as e:
            print(f"  第 {i + 1} 次失败: {type(e).__name__}")
        time.sleep(2 ** i)          # 1s -> 2s -> 4s
    return None


def parse(html):
    """解析一页，返回 (数据行, 是否有下一页)。"""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for box in soup.select("div.quote"):
        text = box.select_one("span.text")
        author = box.select_one("small.author")
        if text is None or author is None:
            continue
        rows.append({
            "text": text.get_text(strip=True).strip("“”"),
            "author": author.get_text(strip=True),
            "tags": ",".join(t.get_text(strip=True) for t in box.select("a.tag")),
        })
    return rows, soup.select_one("li.next > a") is not None


def main():
    all_rows, page = [], 1
    while True:
        html = fetch(page)
        if html is None:
            print(f"第 {page} 页取不到，停止")
            break
        rows, has_next = parse(html)
        all_rows.extend(rows)
        print(f"第 {page} 页: {len(rows)} 条, 累计 {len(all_rows)}")
        if not has_next:
            break
        page += 1
        time.sleep(random.uniform(1.0, 2.0))   # 限速，别把站点压垮

    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"完成: {len(all_rows)} 条 -> {OUT.name}")


if __name__ == "__main__":
    main()
