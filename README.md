# 名言数据看板 ✨

一个不到 200 行的爬虫 + 数据展示小项目：抓取公开练习站 `quotes.toscrape.com` 的 100 条名言，做成可筛选、可统计的看板。

**在线试用**：👉 部署后把这里换成你的 `https://xxx.streamlit.app` 链接

> 截图：部署完截一张图存成 `screenshot.png` 放到根目录，再把下面这行的注释去掉，README 顶部就有效果图了。
>
> `<!-- ![效果图](screenshot.png) -->`

## 功能

- 爬取 10 页名言 → 存成 `quotes.csv`（带限速和重试）
- 按作者多选、按关键词搜索
- 实时统计条数 / 作者数 / 标签数
- 作者产量 Top 10 柱状图

## 怎么跑

```bash
pip install -r requirements.txt
python scraper.py          # 生成 quotes.csv
streamlit run app.py       # 浏览器打开 http://localhost:8501
```

## 部署成能点开的链接

1. 把整个目录推到 GitHub（Public 仓库）
2. 打开 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 账号登录
3. New app → 选仓库 → Main file 填 `app.py` → Deploy
4. 拿到 `https://xxx.streamlit.app`，复制到本文顶部的「在线试用」

## 技术栈

Python / requests / BeautifulSoup / pandas / Streamlit

## 数据来源

[quotes.toscrape.com](https://quotes.toscrape.com) —— 专门供爬虫练习的公开沙盒站点，允许自由抓取。

## 说明

- 代码里的请求带了 `User-Agent`、`timeout`，页间 `sleep` 1–2 秒，属于基本礼貌
- 不采集个人隐私、不绕过任何登录或验证码
