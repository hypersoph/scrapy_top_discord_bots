# Project: Top.gg, Custom ItemLoader

In this project we are going to scrape the top bots on Top.gg to create a dataset of all bots listed on the site.

Example

https://top.gg/list/top?page=3

## Targets

From each page we will scrape:

- Bot name
- Bot description
- Bot image url
- Number of servers
- Number of votes
- Its rank
- URL for the bot's page on top.gg
- Tags

From each bot's page:

- Bot's Website URL
- Invite link
- Support server
- Creator
- Long description
- Prefix

## Primary Concerns

This website uses Cloudflare DDoS protection. We must bypass this in order to scrape anything.

We are using cfscrape

https://github.com/Anorov/cloudflare-scrape

As of July 2020 this pull request works:

https://github.com/Anorov/cloudflare-scrape/pull/373

```cmd
pip install https://github.com/Sraq-Zit/cloudflare-scrape/archive/master.zip
```



# Silly Mistakes

- forgetting the text argument in

  ```python
  selector_obj = Selector(text=html)
  ```

## Forgot to do:

- Process numerical fields to numbers (eg. remove commas, make int)

- Save the top.gg bot ID's

# Things Learned

https://stackoverflow.com/questions/54102498/load-item-fileds-with-itemloader-across-multiple-responses

I learned how to carry over items between requests using the meta tag and a custom item loader class. Without it, our spider only yielded the items from `parse_summary` method but not the items from `parse` method.

Create loader.py in the top_gg folder

```python
from scrapy.loader import ItemLoader as ScrapyItemLoader

class ItemLoader(ScrapyItemLoader):
    """ Extended Loader
        for Selector resetting.
        """

    def reset(self, selector=None, response=None):
        if response is not None:
            if selector is None:
                selector = self.default_selector_class(response)
            self.selector = selector
            self.context.update(selector=selector, response=response)
        elif selector is not None:
            self.selector = selector
            self.context.update(selector=selector)
```

Import it into your spider

```python
from ..loader import ItemLoader

class TheLoader(ItemLoader):
    pass
```

Make the loader object using the custom class

```python
loader = TheLoader(item=TopGgItem(), selector=listing, response=response)
```

Pass it on in the response meta

```python
            yield scrapy.Request(
                url = abs_url,
                cookies = token[0],
                headers = {
                    'User-Agent':token[1]
                },
                callback = self.parse_bot_page,
                meta = {
                    'loader':loader
                }
            )
```

And finally reset the loader.

```python
    def parse_bot_page(self, response):
        loader = response.meta['loader']
        # rebind ItemLoader to new Selector instance
        #loader.reset(selector=response.selector, response=response)
        # skipping the selector will default to response.selector, like ItemLoader
        loader.reset(response=response)
```



# Cloudflare scrape

Many websites are difficult to scrape because of this Cloudflare challenge.

A package for solving cloudflare challenges is called cloudflare-scrape.

[https://github.com/Anorov/cloudflare-scrape](https://github.com/Anorov/cloudflare-scrape?fbclid=IwAR3QW9abf7efoUardIA_8fWxXCcK9wFevzn37yRjJcmnX8WAged4BTQde6g)

However, the master branch is outdated. This did not work for my project. Our savior is one of the pull requests by Sraq-Zit

https://github.com/Anorov/cloudflare-scrape/pull/373

To install his fixed cloudflare-scrape just install the package this way:

```
pip install https://github.com/Sraq-Zit/cloudflare-scrape/archive/master.zip
```

Now just import cfscrape into your spider, and follow the example:

```python
    def start_requests(self):
        url = 'https://your-website-here.com'
        scraper = cfscrape.create_scraper()
        token = scraper.get_tokens(url)
        
        yield scrapy.Request(
            url=url,
            cookies=token[0],
            headers={
                'User-Agent':token[1]
            },
            callback = self.parse,
            meta= {
                'currentPage': 1,
                'token':token
            }
            )
```

get_tokens returns a tuple with 2 elements: a dictionary (the cookies) and the user agent used. The user agent must match with all the requests.

I also pass on the token within the request meta to carry the cookies and user agent to next requests.



# Incorporating cloudflare scrape into middleware

https://github.com/clemfromspace/scrapy-cloudflare-middleware

Rather than writing cfscrape into the spider, we can also use middleware instead.

# Rotating proxies

https://github.com/TeamHG-Memex/scrapy-rotating-proxies



## Custom proxy direct in spider

Simply add to the meta of a request to make it use a proxy.

Eg.

```python
        yield scrapy.Request(
            url=url,
            callback = self.parse,
            meta= {
                'currentPage':current_page,
                'proxy':'192.178.1.1.:8080'
            }
            )
```

