import requests
import time
import re
from datetime import datetime

SUBTITLE_URL = "https://livestreaming.b67.tweedekamer.nl/live/plenairezaal/subtitles/nl_Live.m3u8?sourcetimestamps=1"

REGEX_UUID4 = r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
REGEX_SUBTITLE_URL = f'https://amcpwetkms-euwe.streaming.media.azure.net\/{REGEX_UUID4}\/subtitles\/nl\/[0-9]+.vtt'

IDLE_TIME = 2
MAX_URL_LENGTH = 200


class SubtitleFunction:
    def __init__(self, stream):
        self.stream = stream
        self.urls_seen = []
    
    def run(self):
        urls = self._get_new_urls()
        urls = self._update_urls_seen(urls)
        subs = self._get_new_subs(urls)
        return subs
    
    def _get_new_urls(self):
        r = requests.get(SUBTITLE_URL)
        urls = re.findall(REGEX_SUBTITLE_URL, str(r.content))
        return urls
    
    def _get_new_subs(self, urls):
        subs = []
        for url in urls:
            sub = requests.get(url).content
            subs.append(sub)
        return subs
    
    def _update_urls_seen(self, urls):
        new_urls = []
        for url in urls:
            if url not in self.urls_seen:
                self.urls_seen.append(url)
                new_urls.append(url)
        
        if len(self.urls_seen) > MAX_URL_LENGTH:
            self.urls = self.urls_seen[-MAX_URL_LENGTH:]
        
        return new_urls

    def data_handler(self, sub):
        # write the subtitle to Quix
        self.stream.parameters.buffer.add_timestamp(datetime.utcnow()) \
            .add_value("sub", sub) \
            .write()
