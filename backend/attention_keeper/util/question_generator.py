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


def location_question(title: str, text: str, event_id: int) -> bool:
    entity_list = extract_ner(text)
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
            question = Question(event_id=event_id, prompt=title+": "+text.replace(entity[1], "_______"))
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
                if names[0] == "PERSON" and (names[1] not in entity_list) and (len(options) < 4) and  " " in names[1] and (names[1] not in options) and ("college" not in names[1].lower()) and ("university" not in names[1].lower()):
                    options.append(names[1])
    if len(options) == 4:
        question = Question(event_id=event_id, prompt=title+": "+text.replace(options[0], "_______"))
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
        question = Question(event_id=event_id, prompt=title+": "+text.replace(str(x), "_______"))
        db.session.add(question)
        db.session.commit()
        for option in options:
            db.session.add(
                QuestionOption(question_id=question.question_id, option=option, correct=option == x))
        db.session.commit()
        return True
    except:
        return False


def query(text: str, event_id: int):
    try:
        wiki_query = wikipedia.search(text)
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

    person_q_list = []
    date_q_list = []
    location_q_list = []

    for sentence in good_sentences:
        person_q_list.append(person_question(wiki_query[0], sentence, event_id))
        date_q_list.append(date_question(wiki_query[0], sentence, event_id))
        location_q_list.append(location_question(wiki_query[0], sentence, event_id))

    return {"person_q_list": person_q_list, "date_q_list": date_q_list, "location_q_list": location_q_list}
