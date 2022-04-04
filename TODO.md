# TODO

- frontend
    - page
        - navigation top bar 
        - set title
        - set favicon / logo
        - re-design page header
    - table of users
        - ranking
        - level / badge
        - number of attended
        - number of solved
        - sorting for any columns
    - scoreboard table
        - icon image for show-code button
        - fail-count: red-color or icon-display
        - columns width difference between tables
    - code box 
        - improve css: padding margin shadow 
        - customizable highlight color
    - others
        - show loading gif
        - filter of contests
            - by range of date
            - by contest numbers
        - link to leetcode question page
        - $.when(fetch1, fetch2, fetch3, ...)
        - fetch fail handle (404, 429...)
- backend
    - json record files
        - keep files in multiple servers
        - client reqeust priority
            1. raw.githubusercontent.com
            2. cs.nctu.edu.tw
            3. jasonisgod.xyz
    - handicap
        - setup rule
        - auto calculation
    - main.py crawling 
        - add sleep between requests
        - check before over-write existed json file
        - cmd parameter
            - contest name (list)
            - PAGE_RANGE
            - REPEATS
    - config files
        - username.json
        - contest.json
        - handicap.json