# DealEngine Take Home Project: Scraping CWRU Google Groups for Mailing List

> This short script scraps CWRU Google Groups and collects a mailing list of exposed @case.edu accounts.
> This is [a take home project](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/instruction.md) of [DealEngine](https://dealengine.io) Summer Internship, issued by [Phil Hwang](phil@dealengine.io).

---
## Run
Run the following command first to avoid synchronizing the content within `my_cwru_token.py` to GitHub, for privacy concerns.
```
git update-index --assume-unchanged my_cwru_token.py
```

Fill in your credential in [`my_cwru_token.py`](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/my_cwru_token.py), then run the `google_group_scraper` (available in both [`.ipynb`](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/google_group_scraper.ipynb) and [`.py`](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/google_group_scraper.py)) however you'd like.

Note it take quite a while to complete the task, and you might need to adjust the `time.sleep()` wait time to accompany your internet environment. So for twerking around, maybe just try [google_group_scraper.ipynb](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/google_group_scraper.ipynb) in a cell-by-cell manner.

You may expect a mailing list output at [`CWRU_scrapped_mailing_list.txt`](https://github.com/choH/DealEngine_CWRU_mailing_hack/blob/master/CWRU_scrapped_mailing_list.txt)~~, for the default setting it has 1400+ `@case.edu` email account inside it, as the delivery of this take-home~~.   
(removed due to privacy concerns)

## Reflection

This script focuses on giving a clean and concise delivery, but not a perfect one. Several improvements I could think of include:

1. Identify private group at the `forumsearch` layer (probably not much performance gain since now the script does the check in `forum` layer with an exception handling, which is really fast).
2. Implement a counter on the number of non-private forums (or even number of posts available for scrape), so that we may scroll the `forumsearch` page more rationally — now we have 300 `Keys.END`, which is way too much.
3. Register the total number of post available of each forum, and implement dynamic `WAIT` time on `forum` layer incrementally, so that all posts are guaranteed to be scraped.
4. Implement a check on `forum` layer to skip posts from the same sender with no other reply (as such account is likely scrapped already).
5. Use RSS source link like [this](https://groups.google.com/a/case.edu/forum/feed/cwrumocktrial/msgs/rss_v2_0.xml?num=100) instead of [standard Google Group URL](https://groups.google.com/a/case.edu/forum/feed/cwrumocktrial/msgs/rss_v2_0.xml?num=100), as it will functionally skips all scrolling on the `forum` layer. I did not proceed on this route as I "magic-numbered" the `forumsearch` layer, I feel like if I shortcut the `forum` layer as well there will be no much learning. I also did not use anything like [gggd](https://github.com/henryk/gggd) for the same reason.



---

### Ref.

* [2018-Teatime-W4a-Web Scraping | SDLE Research Center](https://www.youtube.com/watch?v=XuTxkXW2lzw&app=desktop)
* [Scrape dynamic web page (Google Group forum) using Selenium (1) | Huidong Tian](https://withr.github.io/scrape-dynamic-web-page-using-selenium-1/)
* Acknowledgement to my friend [@Lynsens](https://github.com/Lynsens) for providing a helpful intro to web scraping.
