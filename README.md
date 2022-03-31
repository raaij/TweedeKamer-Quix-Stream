# TweedeKamer Quix Stream

This code streams transcribed text from debates held in the Tweede Kamer (Second Chamber) to Quix.

## How to run

1. Copy the `settings-template.json` into a `settings.json` file
2. Fill in the values corresponding to the keys
3. Run `pip install -e .` (TODO: Add required libraries to `setup.py`)
4. Run `python stream/source/main.py`

## Ideas for what to do with this data

1. Sentiment analysis
2. Automatically create highlights like https://www.youtube.com/watch?v=gR1eYB8AnYg
