# LeetQuery 

## TODO

- frontend
    - functional
        - filter/tabs of contests
        - fold/unfold tables
        - $.when(fetch1, fetch2, fetch3, ...)
        - fetch fail handle (404, 429...)
        - link to questions
    - UI
        - page
            - navigation bar/tabs, top of page
            - set page title
        - scoreboard table
            - icon image for show-code button
            - fail-count: red-color or icon-display
            - columns width difference between tables
        - code box 
            - BUG: py3 language bug
            - highlight color (customizable)
            - popup box, not buttom of page
        - responsive design 
            - check for all 16:9, 9:16, 22:9, 4:3, ...
- backend
    - add handicap time
        - seperated file record
        - list of user+handicap
    - add sleep between requests
    - check before over-write existed json file
    - input by cmd parameter
        - contest name (list)
        - PAGE_RANGE
        - REPEATS