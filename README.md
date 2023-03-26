# LeetQuery
Query Leetcode Contest Ranking Data

keywords: leetcode contest weekly biweekly history rank ranking query crawl user username code score scoreboard submission

## Backend
- `python3 server.py {PORT}`
  - run http server
- `python3 crawl.py`
  - query leetcode contest and output results as JSON files
- `config/*.json`
  - config files of users, contests, ...
- `files/{CONTEST}-{USER}.json`
  - submissions of USER in CONTEST

## Frontend
- `index.html`
  - main page
- `js/script.js`
  - set DOMAIN and PORT of server
