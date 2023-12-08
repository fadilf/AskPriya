import feedparser
import os.path
import pickle
from datetime import datetime, timedelta
import streamlit as st
from include import include

include()

cache_file = "./feed_cache.pkl"
feed_link = "https://www.uscis.gov/news/rss-feed/22984"

def get_timestamped_feed(url):
    return {
        "time": datetime.now(),
        "feed": feedparser.parse(url).entries
    }

def write_new_timestamped_feed(url, path):
    timestamped_feed = get_timestamped_feed(url)
    with open(path, "wb+") as f:
        pickle.dump(timestamped_feed, f)
    return timestamped_feed

if os.path.isfile(cache_file):
    with open(cache_file, "rb") as pickle_file:
        parsed_feed = pickle.load(pickle_file)
        if (datetime.now() - parsed_feed["time"]) > timedelta(days=1):
            write_new_timestamped_feed(feed_link, cache_file)
else:
    parsed_feed = write_new_timestamped_feed(feed_link, cache_file)

for entry in parsed_feed["feed"][:10]:
    title = entry.title
    link = entry.link
    summary = entry.summary
    md = f"### {title}\n{summary}\n[Read more]({link})"
    st.markdown(md)
    st.write("\n\n")
