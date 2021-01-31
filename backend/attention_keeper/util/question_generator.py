import random
import re
import threading
import time

import wikipedia
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from attention_keeper.model.city import City
from attention_keeper.model.question import Question, QuestionOption
from attention_keeper.util import logger
from attention_keeper.view.api import app
from attention_keeper.view.api import db

DATE_REGEX = re.compile('\d{4}')
LOGGER = logger.get_logger(__name__)


def extract_ner(text: str):
    chunks = []
    tree = ne_chunk(pos_tag(word_tokenize(text)))
    for leaf in tree:
        if hasattr(leaf, 'label'):
            chunks.append([leaf.label(), ' '.join(c[0] for c in leaf)])
    return chunks


def location_question(title: str, text: str, event_id: int) -> bool:
    entity_list = extract_ner(text)
    with app.app_context():
        cities = [city.name for city in City.query.all()]
    for entity in entity_list:
        # Question Number 1. Location Generation
        if entity[0] == "GPE" and entity[1] != "American":
            options = [entity[1]]
            if entity[1] in cities:
                cities.remove(entity[1])

            city_numbers = random.sample(range(0, len(cities)), 3)

            for i in range(0, 3):
                options.append(cities[city_numbers[i]])
            with app.app_context():
                question = Question(event_id=event_id, prompt=title + ": " + text.replace(entity[1], "_______"))
                db.session.add(question)
                db.session.commit()
                for option in random.sample(options, len(options)):
                    db.session.add(
                        QuestionOption(question_id=question.question_id, option=option, correct=option == entity[1]))
                db.session.commit()
            return True
    return False


def person_question(title: str, text: str, event_id: int) -> bool:
    entity_list = extract_ner(text)
    options = []
    for entity in entity_list:
        if entity[0] == "PERSON" and (" " in entity[1]):
            if options:
                options = [entity[1]]

            try:
                possible_names = extract_ner(wikipedia.page(entity[1]).content)
            except:
                return False

            for names in possible_names:
                if names[0] == "PERSON" and (names[1] not in entity_list) and (len(options) < 4) and " " in names[
                    1] and (names[1] not in options) and ("college" not in names[1].lower()) and (
                        "university" not in names[1].lower()):
                    options.append(names[1])
    if len(options) == 4:
        with app.app_context():
            question = Question(event_id=event_id, prompt=title + ": " + text.replace(options[0], "_______"))
            db.session.add(question)
            db.session.commit()
            for option in options:
                db.session.add(
                    QuestionOption(question_id=question.question_id, option=option, correct=option == options[0]))
            db.session.commit()
        return True
    else:
        return False


def date_question(title: str, text: str, event_id: int) -> bool:
    target_date = DATE_REGEX.search(text)
    if target_date:
        target_date = int(target_date.group())
        # if the time difference is less than 5 years, we need to apply a shift so the answers are not obviously wrong
        # future dates are not affected (in case there is sci-fi etc)
        if 5 > time.localtime(time.time())[0] - target_date > 0:
            shift = time.localtime(time.time())[0] - target_date
            options = random.sample(list(range(target_date - 10 + shift - 1, target_date - 1)), 3)
        else:
            options = random.sample(
                list(range(target_date - 5, target_date - 1)) + list(range(target_date + 1, target_date + 5)), 3)
        with app.app_context():
            options.append(target_date)
            question = Question(event_id=event_id, prompt=title + ": " + text.replace(str(target_date), "_______"))
            db.session.add(question)
            db.session.commit()
            for option in options:
                db.session.add(
                    QuestionOption(question_id=question.question_id, option=option, correct=option == target_date))
            db.session.commit()
        return True
    else:
        return False


class QuestionGenerator(threading.Thread):
    def __init__(self, text: str, event_id: int):
        threading.Thread.__init__(self)
        self.event_id = event_id
        self.text = text

    def run(self):
        try:
            wiki_query = wikipedia.search(self.text)
            # Theres a corner case in particular with the U.S. that makes this code go haywire. Just remove it. Its a
            # rare case.
            wiki_list = wikipedia.summary(wiki_query[0], 0, 0, False, True).replace('U.S.', 'US').replace(' v. ', ' v ')
        except wikipedia.WikipediaException:
            return None

        query_sentences = wiki_list.split('. ')
        good_sentences = []
        remove_next = False
        for number, sentence in enumerate(query_sentences):
            if remove_next:
                remove_next = False
                continue
            if len(sentence) < 10:
                if good_sentences:
                    good_sentences.pop()
                    remove_next = True
            else:
                good_sentences.append(sentence)

        for sentence in good_sentences:
            person_question(wiki_query[0], sentence, self.event_id)
            date_question(wiki_query[0], sentence, self.event_id)
            location_question(wiki_query[0], sentence, self.event_id)
        LOGGER.debug("done generating questions")
