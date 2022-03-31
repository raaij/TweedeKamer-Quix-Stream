"""
Much of this is based on 
https://github.com/quixai/quix-library/blob/main/python/sources/Twitter-Stream/main.py
"""

import os
import json
import time
from threading import Thread
from requests.exceptions import ChunkedEncodingError

from quixstreaming import QuixStreamingClient, StreamReader
from quixstreaming.app import App

from stream.constants import PATH_SETTINGS
from stream.source.subtitle_function import SubtitleFunction


with open(PATH_SETTINGS, 'r') as fp:
    settings = json.load(fp)

try:
    # should the main loop run?
    run = True
    client = QuixStreamingClient(settings['QUIX_SDK_TOKEN'])
    output_topic = client.open_output_topic(settings["QUIX_TOPIC"])

    # define code to create the output stream
    def create_stream():
        output_stream = output_topic.create_stream()
        output_stream.properties.name = "tweede_kamer_subtitle_stream_results"
        output_stream.properties.location = "/tweede_kamer_subtitle_data"

        print("CONNECTED!")

        return output_stream
    
    def get_stream(output_stream):
        global run

        subtitle_function = SubtitleFunction(output_stream)
        
        while run:
            try:
                subs = subtitle_function.run()
                for sub in subs:
                    if not run:
                        break

                    if sub:
                        subtitle_function.data_handler(sub)
            
            except ChunkedEncodingError:
                # if we get a ChunkedEncodingError error sleep then try again
                time.sleep(6)
                continue

            except Exception:
                # some unexpected error occurred.. stop the loop
                run = False
            

    def before_shutdown():
        global run

        # Stop the main loop
        run = False


    def main():
        global output_topic
        output_stream = create_stream()

        thread = Thread(target=get_stream, args=(output_stream,))
        thread.start()

         # wait for sigterm
        App.run(before_shutdown=before_shutdown)

        # wait for worker thread to end
        thread.join()

        print("Exiting")


    if __name__ == "__main__":
        main()

except Exception as e:
    raise e
