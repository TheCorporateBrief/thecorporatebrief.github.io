from datetime import datetime
from zoneinfo import ZoneInfo
import re, textwrap, hashlib, html
import feedparser

LON = ZoneInfo("Europe/London")
today = datetime.now(LON)
year, week, _ = today.isocalendar()
week = int(week)

FEEDS = [
  ("Reuters Business","https://feeds.reuters.com/reuters/businessNews"),
  ("Reuters World","https://feeds.reuters.com/reuters/worldNews"),
  ("Reuters Markets","https://feeds.reuters.com/reuters/USmarketsNews"),
  ("Reuters Mergers","https://feeds.reuters.com/reuters/mergersNews"),
  ("CNBC Top","https://www.cnbc.com/id/100003114/device/rss/rss.html"),
  ("FT UK","https://www.ft.com/?format=rss"),
  ("SEC S-1","https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=S-1&count=100&output=atom"),
]

def clean(txt):
  if not txt: return ""
  txt = html.unescape(re.sub(r"<[^>]+>", " ", str(txt)))
  txt = re.sub(r"\s+"," ", txt).strip()
  return txt

def bucket(title, summary):
  t = f"{title} {summary}".lower()
  if any(k in t for k in ["s-1","ipo","initial public offering","lists","debut","prices ipo","priced its ipo"]): return "IPOs"
  if any(k in t for k in ["acquires","acquisition","merger","merges","takeover","to buy","buyout","stake","m&a","deal"]): return "Deals"
  if any(k in t for k in ["fed","ecb","bank of england","boe","interest rate","inflation","cpi","ppi","payrolls","gdp","fiscal","budget","tariff","rate cut","rate hike"]): return "Macro/Policy"
  if any(k in t for k in ["ukraine","russia","china","iran","gaza","israel","taiwan","nato","sanction","ceasefire","election","eu summit","opec"]): return "Geopolitics"
  return "Companies & Tech"

items = {k:[] for k in ["Macro/Policy","Geopolitics","Deals","IPOs","Companies & Tech"]}

seen = set()
for _,url in FEEDS:
  feed = feedparser.parse(url, request_headers={"User-Agent":"TCBBot/1.0 (+https://github.com/TheCorporateBrief/tcb-staging)"})
  for e in feed.get("entries", [])[:60]:
    title = clean(getattr(e, "title", ""))
    link  = getattr(e, "link", "")
    summ  = clean(getattr(e, "summary", getattr(e,"description","")))
    if not title or not link: continue
    h = hashlib.md5((title+link).encode()).hexdigest()
    if h in seen: continue
    seen.add(h)
    b = bucket(title, summ)
    sub = summ[:220]
    items[b].append({"title":title, "sub":sub, "link":link})

for k in items: items[k] = items[k][:5]

draft_path = f"_drafts/{year}-week-{week:02d}-the-corporate-brief.md"
fm = f"""---
title: "The Corporate Brief — Week {week:02d} {year}"
date: {today.strftime('%Y-%m-%d')}
week: {week:02d}
tags: [weekly, markets, macro, geopolitics, deals, ipos, companies]
---

# Markets snapshot
_(add S&P/Nasdaq/FTSE/crypto quick numbers)_

# Macro/Policy
"""
md = fm
for sec in ["Macro/Policy","Geopolitics","Deals","IPOs","Companies & Tech","On the Radar"]:
  if sec != "Macro/Policy": md += f"\n# {sec}\n"
  lst = items.get(sec, [])
  if not lst and sec != "On the Radar":
    md += "* _No major items auto-detected_\n"
  else:
    for it in lst:
      md += textwrap.dedent(f"""\
      - **{it['title']}** — *{it['sub']}*  
        - Why it matters: _(one-liner)_  
        - Source: [{it['link']}]({it['link']})  
        - TCB take: —
      """)
    if sec == "On the Radar":
      md += "- _Your quick notes for next week_\n"

with open(draft_path,"w",encoding="utf-8") as f:
  f.write(md)

top = [it["title"] for sec in ["Macro/Policy","Deals","IPOs","Companies & Tech","Geopolitics"] for it in items[sec]][:3]
snippet = " | ".join(top) if top else "Macro, deals, IPOs, geopolitics in one read."
li = f"TCB Week {week:02d}: {snippet} — concise weekly brief. #markets #macro #M&A #IPOs #geopolitics #TheCorporateBrief"
with open(f"notes/linkedin-week-{week:02d}.txt","w",encoding="utf-8") as f:
  f.write(li + "\n")
print(f"Draft written to {draft_path}")
