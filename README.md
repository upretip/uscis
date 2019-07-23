# USCIS 
### How to use
```
from uscis.USCIS import retrieve

print(retrieve("YSC1891500001"))

>>> 
```
The module depends on `requests` and `bs4`


This project scrapes the uscis [site](egov.uscis.gov/casestatus) by posting some random receipt number and extracts the case status for those receipt number.

I have downloaded about 5000 entries (before my IP was temporarily blocked by the server) and will be using those for some  analysis.

In this [example](exmaple_analysis.ipynb) I try to combine a few tools to get some insights from the data scraped. In particular,

1. SQLite - to create and store data in local database (doesn't create a database, just a .db file)
2. Pandas - read data from sqlite, and do data manupulation
3. Matplotlib - to create simple visualizations, bargraph, pie chart, etc


This document will be improved once the project materializes