import random
import re
import time

import wikipedia
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from attention_keeper.model.city import City
from attention_keeper.model.question import Question, QuestionOption
from attention_keeper.view.api import db


def extract_ner(text: str):
    chunks = []
    tree = ne_chunk(pos_tag(word_tokenize(text)))
    for leaf in tree:
        if hasattr(leaf, 'label'):
            chunks.append([leaf.label(), ' '.join(c[0] for c in leaf)])
    return chunks


def location_question(text: str, event_id: int) -> bool:
    entity_list = extract_ner(text)
    cities = City.query.all()
    for entity in entity_list:
        # Question Number 1. Location Generation
        if entity[0] == "GPE":
            options = [entity[1]]
            if entity[1] in cities:
                cities.remove(entity[1])

            city_numbers = random.sample(range(0, len(cities)), 3)

            for i in range(0, 3):
                options.append(cities[city_numbers[i]][0])
            question = Question(event_id=event_id, prompt=text.replace(entity[1], "_______"))
            db.session.add(question)
            db.session.commit()
            for option in random.sample(options, len(options)):
                db.session.add(
                    QuestionOption(question_id=question.question_id, option=option, correct=option == entity[1]))
            db.session.commit()
            return True
    return False


def person_question(text: str, event_id: int) -> bool:
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
                if names[0] == "PERSON" and (names[1] not in entity_list) and (len(options) < 4) and " " in names[1]:
                    options.append(names[1])
    if len(options) == 4:
        question = Question(event_id=event_id, prompt=text.replace(options[1], "_______"))
        db.session.add(question)
        db.session.commit()
        for option in options:
            db.session.add(
                QuestionOption(question_id=question.question_id, option=option, correct=option == options[1]))
        db.session.commit()
        return True
    else:
        return False


def date_question(text: str, event_id: int) -> bool:
    try:
        x = int(re.search('\d{4}', text).group())
        # if the time difference is less than 5 years, we need to apply a shift so the answers are not obviously wrong
        # future dates are not affected (in case there is sci-fi etc)
        if 5 > time.localtime(time.time())[0] - x > 0:
            shift = time.localtime(time.time())[0] - x
            options = random.sample(list(range(x - 10 + shift - 1, x - 1)), 3)
        else:
            options = random.sample(list(range(x - 5, x - 1)) + list(range(x + 1, x + 5)), 3)
        options.append(x)
        question = Question(event_id=event_id, prompt=text.replace(str(x), "_______"))
        db.session.add(question)
        db.session.commit()
        for option in options:
            db.session.add(
                QuestionOption(question_id=question.question_id, option=option, correct=option == x))
        db.session.commit()
        return True
    except:
        return False
