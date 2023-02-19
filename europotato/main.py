import datetime
import pathlib
import queue

from absl import app
from absl import flags

from crawler import crawler, error_handler, http_fetcher
from europotato import router

FLAGS = flags.FLAGS

flags.DEFINE_string('root_url', 'https://www.europotato.org/varieties/index', 'Root URL.')
flags.DEFINE_string('output_root', '', 'Path to write output files under.')
flags.DEFINE_integer('crawl_delay_seconds', 60, 'How long to delay between pages, in seconds.', lower_bound=0)
flags.DEFINE_boolean('retry_failures', False, 'Retry .')


def main(argv):
    if not FLAGS.output_root:
        raise ValueError('Output root must be provided')
    if not FLAGS.root_url:
        raise ValueError('Root URL must be provided')
    f = http_fetcher.HttpFetcher()
    h = router.Handler(pathlib.Path(FLAGS.output_root))
    e = error_handler.LoggingHandler()
    crawl_delay = datetime.timedelta(seconds=FLAGS.crawl_delay_seconds)

    c = crawler.Crawler(f, h, e, queue.Queue, crawl_delay, FLAGS.retry_failures)
    c.crawl(FLAGS.root_url)


if __name__ == '__main__':
    app.run(main)
