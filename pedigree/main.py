import datetime
import pathlib
import queue

from absl import app
from absl import flags

from crawler.crawler import Crawler
from crawler.error_handler import LoggingHandler, RetryingHandler
from crawler.sqlite_state_manager import SqlStateManager
from crawler.http_fetcher import HttpFetcher
from pedigree.router import Handler

FLAGS = flags.FLAGS

flags.DEFINE_string('root_url', 'https://www.plantbreeding.wur.nl/PotatoPedigree/multilookup.php', 'URL to begin the '
                                                                                                   'crawl at.')
flags.DEFINE_string('state_root', '', 'Path to directory used to manage queue state.')
flags.DEFINE_string('output_root', '', 'Path to write output files under.')
flags.DEFINE_string('user_agent', 'http://github.com/dinosaursrarr/potato/pedigree', 'User agent to report when '
                                                                                     'fetching pages.')
flags.DEFINE_integer('crawl_delay_seconds', 10, 'How long to delay between pages, in seconds.', lower_bound=0)
flags.DEFINE_integer('max_failures_per_url', 3, 'How many times to try crawling a single URL before giving up.',
                     lower_bound=0)


def main(argv):
    if not FLAGS.state_root:
        raise ValueError('State root must be provided')
    if not FLAGS.output_root:
        raise ValueError('Output root must be provided')
    if not FLAGS.root_url:
        raise ValueError('Root URL must be provided')
    state_root = pathlib.Path(FLAGS.state_root)

    handler = Handler(pathlib.Path(FLAGS.output_root))
    state_manager = SqlStateManager(state_root / 'pedigree.db',
                                    max_failures_per_url=FLAGS.max_failures_per_url)
    crawl_delay = datetime.timedelta(seconds=FLAGS.crawl_delay_seconds)

    c = Crawler(HttpFetcher(FLAGS.user_agent), handler, state_manager,
                RetryingHandler(LoggingHandler()), crawl_delay)
    c.crawl([FLAGS.root_url])


if __name__ == '__main__':
    app.run(main)
