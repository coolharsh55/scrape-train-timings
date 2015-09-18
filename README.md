# scrape-train-timings
scrape local train timings for `pune to lonavala` trains and calculate the `timing differences` between various stations

[![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/coolharsh55/harshp.com/blob/master/LICENSE)

requirement came from my other project: 
[PNL2LNL](http://brainbank.harshp.com/pnl2lnl/)

## what does it do?
It scrapes information from online sources ( currently punediary) to retrieve local train information and calculates the time taken to go from each station to the next. It also calculates the average time difference for each train stop.

### why is this information needed?
Initially, the requirement is to check if the time difference between stations is the same for every train (along the same direction and route).

## what does it use?
`scrapy` to scrape the information
and `python 2.7` for a script to parse the `json` and print pretty output containing the timing information

## how to use the information?
There are two files called `up.json` and `down.json` containing scraped, cleaned, and corrected data for up/down local train timings respectively. The format is:

```
[
    {
        'station': 'station_name',
        'stops'  : ['HH.MM', ...]
    }
]
```

### using with `scrapy`

the repo is a `scrapy` project called learn-scrapy (because I'm learning `scrapy`) and as such can be used like any other scrapy project.

```
# install scrapy first
$:> pip install scrapy

# at project root
$:> scrapy crawl up_spider -o up.json
$:> scrapy crawl down_spider -o down.json
$:> python diff.py > op.txt
```

> __note__: the scraped information contains incorrect information about the timings which must be corrected manually