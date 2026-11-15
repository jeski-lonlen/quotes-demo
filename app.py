# -*- coding: utf-8 -*-
"""
名言数据看板 —— Streamlit 入门 demo

数据来源: quotes.toscrape.com（公开的爬虫练习站）
本地运行: streamlit run app.py
部署: 推到 GitHub 后，在 share.streamlit.io 选仓库 -> Deploy
"""
from pathlib import Path

import pandas as pd
import streamlit as st

CSV = Path(__file__).with_name("quotes.csv")


@st.cache_data
def load_data():
    """读 CSV。加缓存，页面重绘时不会重复读盘。"""
    return pd.read_csv(CSV)


def main():
    st.set_page_config(page_title="名言数据看板", page_icon="📊", layout="wide")
    st.title("📊 名言数据看板")
    st.caption("数据由 requests + BeautifulSoup 抓取自 quotes.toscrape.com，共 100 条")

    if not CSV.exists():
        st.error("找不到 quotes.csv —— 先在本地运行 `python scraper.py` 生成数据。")
        st.stop()

    df = load_data()

    # ---------- 侧边栏筛选 ----------
    st.sidebar.header("筛选")
    authors = sorted(df["author"].dropna().unique())
    picked = st.sidebar.multiselect("作者", authors, default=authors)
    keyword = st.sidebar.text_input("关键词（英文，如 life）", "")

    view = df[df["author"].isin(picked)] if picked else df.iloc[0:0]
    if keyword.strip():
        view = view[view["text"].str.contains(keyword.strip(), case=False, na=False)]

    # ---------- 指标 ----------
    tags = {t for row in view["tags"].dropna() for t in str(row).split(",") if t}
    c1, c2, c3 = st.columns(3)
    c1.metric("名言条数", len(view))
    c2.metric("作者数", view["author"].nunique())
    c3.metric("标签数", len(tags))

    # ---------- 正文 ----------
    left, right = st.columns([2, 1])
    with left:
        st.subheader("名言列表")
        st.dataframe(view[["text", "author", "tags"]],
                     width="stretch", height=420)
    with right:
        st.subheader("作者产量 Top 10")
        st.bar_chart(view["author"].value_counts().head(10))

    with st.expander("这个项目是怎么做的"):
        st.markdown(
            "- **采集**：`scraper.py` 用 requests 抓 10 页，BeautifulSoup 解析，存 CSV\n"
            "- **展示**：Streamlit 读 CSV，做筛选、统计和图表\n"
            "- **规模**：全部代码不到 200 行，适合当作第一个公开作品"
        )


main()
