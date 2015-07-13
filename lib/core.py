import apscheduler.schedulers.background
import datetime
import queue
import sys
from lib.utilities import url_to_json

config = {}


class Tokenizer():
    def __init__(self):
        tokens = config.get('options', {}).get('github_tokens', [])

        self.have_tokens = bool(tokens)
        self.available_tokens = queue.Queue()
        self.scheduler = apscheduler.schedulers.background.BackgroundScheduler(
            )
        self.scheduler.start()

        if not self.have_tokens:
            self.print_warning(
                'No GitHub OAuth tokens provided. Proceeding without '
                'authentication.'
            )

        for token in tokens:
            self.available_tokens.put(token)

    def tokenize(self, url):
        if url.startswith('https://api.github.com'):
            if self.have_tokens:
                token = self.get_token()
                if token is not None:
                    return '{0}?access_token={1}'.format(url, token)
                else:
                    return url
            else:
                return url
        else:
            raise ValueError('url must be for the GitHub API')

    def get_token(self):
        while True:
            if not self.scheduler.get_jobs() and self.available_tokens.empty():
                self.print_warning('No more valid OAuth tokens available.')
                return None

            token = self.available_tokens.get(block=True)

            rate_limit_url = (
                'https://api.github.com/rate_limit?access_token={0}'
            ).format(token)
            status = url_to_json(rate_limit_url)

            # Throw away bad OAuth keys.
            if 'resources' not in status:
                self.print_warning(
                    'Invalid OAuth token supplied. Trying again...'
                )
                continue

            if status['resources']['core']['remaining'] > 0:
                self.available_tokens.put_nowait(token)
                return token
            else:
                self.scheduler.add_job(
                    self.available_tokens.put_nowait,
                    'date',
                    args=[token],
                    run_date=datetime.datetime.fromtimestamp(
                        status['resources']['core']['reset']
                    )
                )

    def print_warning(self, message):
        formatted_message = '\033[91mWARNING\033[0m: {0}'.format(message)
        print(formatted_message)
