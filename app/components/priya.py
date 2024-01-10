import streamlit as st
import requests
import re


class Priya:
    def make_query(self, query):
        data = requests.get(
            st.secrets["API_URL"],
            params={"q": query, "api_key": st.secrets["API_KEY"]},
            timeout=10000,
        ).json()

        citations = []
        for citation in re.findall(r"\[[\d\s,]+\]", data["response"]):
            numbers = citation[1:-1]
            linked_citations = []
            for number in numbers.split(","):
                number = int(number.strip())
                source_link = data["sources"][number - 1]["link"]
                linked_citations.append(f"[{number}]({source_link})")
            citations.append("[" + ", ".join(linked_citations) + "]")

        output = ""
        for idx, text in enumerate(re.split(r"\[[\d\s,]+\]", data["response"])):
            output += text
            if idx != len(citations):
                output += citations[idx]

        if len(data["sources"]) > 0:
            links = [
                f"[{source['page']}]({source['link']})" for source in data["sources"]
            ]
            output += "\n\nSources: " + ", ".join(links)

        return output
