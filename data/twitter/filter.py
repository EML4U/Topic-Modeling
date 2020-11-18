import csv
import string
import pickle
import datetime
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
DetectorFactory.seed = 0


def process_tweet(text):
    # remove hashtags
    text = text.replace('#', '')
    # remove @'s (todo: maybe replace names with generic name like Joe or Dave for more consistency)
    text = text.replace('@', '')
    # remove all non-ascii-chars
    cleaned_text = ''
    for character in text:
        if character in string.ascii_letters + string.digits + string.punctuation + string.whitespace:
            cleaned_text = cleaned_text + character
    for whitespace in string.whitespace:
        cleaned_text = cleaned_text.replace(whitespace, ' ')
    text = ' '.join(cleaned_text.split())  # eliminate potential double whitespaces

    # reject tweets which are....
    if len([word for word in text.split(' ') if 'https://t.co/' not in word]) < 4:  # ...not at least 4 non-link words long,
        return None
    if len([char for char in text if char not in string.whitespace and char not in string.punctuation]) < 10:  # ...do only contain spaces and punctuation,
        return None
    try:
        if detect(text) != 'en':  # ...are not in english,
            return None
    except LangDetectException:  # ... or where the language is not detectable
        print('Language Detect Exception with string: ', text)
        return None

    return text


def process_dataset(filename):
    raw_data_ = []
    with open(filename, 'r') as f:
        for line in csv.reader(f, delimiter=','):
            raw_data_.append(line)

    processed = []

    too_few_entries = []  # some rows don't have enough entries... weird
    wrong_order = []  # some rows are not ordered in the right way... weird again, but apparently all are in too_few_entries

    for row in raw_data_[1:]:
        if len(row) < len(raw_data_[0]):
            too_few_entries.append(row)
            continue
        text = process_tweet(row[2])
        try:
            time = datetime.datetime.fromisoformat(row[0])
        except Exception:
            wrong_order.append(row)
            continue
        if text:
            processed.append((time, text))

    print('Number of malformated rows:', len(too_few_entries), '+', len(wrong_order))
    return processed


print('Processing Biden Dataset...')
processed_biden = process_dataset('hashtag_joebiden.csv')

print('Processing Trump Dataset...')
processed_trump = process_dataset('hashtag_donaldtrump.csv')

print('Dumping the data...')
with open('election_dataset.pickle', 'wb') as handle:
    pickle.dump({
        'biden': processed_biden,
        'trump': processed_trump
    }, handle)
