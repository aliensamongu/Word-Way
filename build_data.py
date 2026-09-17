{\rtf1\ansi\ansicpg1252\cocoartf2907
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww28260\viewh15680\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import json\
import urllib.request\
\
# The 27 New Testament books matching your app's key structure\
BOOKS = [\
    "matthew", "mark", "luke", "john", "acts", "romans",\
    "1corinthians", "2corinthians", "galatians", "ephesians",\
    "philippians", "colossians", "1thessalonians", "2thessalonians",\
    "1timothy", "2timothy", "titus", "philemon", "hebrews",\
    "james", "1peter", "2peter", "1john", "2john", "3john",\
    "jude", "revelation"\
]\
\
# Source repository for open-domain Greek New Testament text\
BASE_URL = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/greek_ugnt.json"\
\
def fetch_and_build():\
    print("Fetching full Greek New Testament dataset...")\
    try:\
        req = urllib.request.Request(BASE_URL, headers=\{'User-Agent': 'Mozilla/5.0'\})\
        with urllib.request.urlopen(req) as response:\
            raw_data = json.loads(response.read().decode('utf-8'))\
    except Exception as e:\
        print(f"Error fetching remote dataset: \{e\}")\
        return\
\
    print("Processing verses and assembling data.json structure...")\
    \
    # Initialize dictionary structure\
    db = \{\}\
    for book in BOOKS:\
        db[book] = \{\
            "na28": \{"greek": "", "gloss": ""\},\
            "aleph": \{"greek": "", "gloss": ""\}\
        \}\
\
    # Populate Greek text from dataset\
    # Grouping verses under each book\
    for verse in raw_data.get("verses", []):\
        book_id = verse.get("book_name", "").lower().replace(" ", "")\
        if book_id in db:\
            text = verse.get("text", "").strip()\
            if text:\
                if db[book_id]["na28"]["greek"]:\
                    db[book_id]["na28"]["greek"] += " " + text\
                else:\
                    db[book_id]["na28"]["greek"] = text\
                \
                # Duplicate base text into aleph fallback\
                db[book_id]["aleph"]["greek"] = db[book_id]["na28"]["greek"]\
\
    # Write out to data.json\
    output_filename = "data.json"\
    with open(output_filename, "w", encoding="utf-8") as f:\
        json.dump(db, f, ensure_ascii=False, indent=2)\
\
    print(f"Success! \{output_filename\} has been updated with all 27 New Testament books.")\
\
if __name__ == "__main__":\
    fetch_and_build()}