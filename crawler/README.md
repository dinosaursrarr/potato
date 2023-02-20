# Crawler

A small and extensible web-crawling framework.

Created since I plan to crawl two different sites for my potato project and I didn't want to reimplement similar
functionality each time.

Supports interruption and graceful resume and relative URLs.

## Usage

Inject the required elements into [`Crawler`](crawler.py) then call `crawl(starting_url)`.

The required elements are:

- [`Fetcher`](fetcher.py): says how to download content. HTTP and HTTPS implementation provided.
- [`Handler`](handler.py): says what to do with page content. User-customizable.
- [`StateManager`](state_manager.py): maintains the queue. Single-machine, in-memory implementation provided. 
- [`ErrorHandler`](error_handler.py): says what to do with errors. Basic implementations provided.

## Limitations 

The current implementation is suitable for relatively small websites, which can easily be fit on a single machine.

The main limitations are:

- Single-threaded, limiting throughput. This wasn't a problem for me since I planned to respect sites' crawl-delay
  instructions.
- In-memory queue, limiting scale. The queue and list of all visited sites must fit into available memory.
- Does not read robots.txt. The sites I planned to crawl didn't say much that was relevant, so I deferred this.
- Users must configure output handling. I'm still not sure exactly what I want, so it's hard to codify a good default.

I haven't paid much attention to performance, since I'm adding a multi-second delay between fetches, to avoid annoying the sites. 

## Example

See [europotato/](../europotato/) for an example of how to use the crawler.

In particular,
 - [main.py](../europotato/main.py) is an example of constructing and starting the crawler.
 - [router.py](../europotato/router.py) is a top-level handler that determines what kind of page we have and dispatches the relevant handler.
 - [index.py](../europotato/index.py) handles index pages where we just need to extract and enqueue newly-discovered URLs.
 - [view.py](../europotato/view.py) scrapes data from index pages and writes it to json.
