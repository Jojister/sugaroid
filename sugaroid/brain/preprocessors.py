import logging
import re
import string
import unicodedata
from nltk.corpus import wordnet as wn
import nltk

short_forms = {
    "coz": "because",
    "bcoz": "because",
    "ye": "yea",
    "bro": "brother",
    "sis": "sister",
    "tk": "thank you",
    "tq": "thank you",
    "ty": "thank you",
    "hwy": "how are you",
    "hi": "Hello",
    "Hoi": "Hello",
    "nvm": "never mind",
    "rotfl": "rolling on the floor with laughter",
    "wtf": "You are bad",  # PS: thats enough for this course of code ;)
    "ikr": "I know right",
    "idk": "I dont know"
    "idc": "I dont care"
    "hbu": "how about you"
    "y": "why"
    "ofc": "of course",
    "10q": "thank you",
    "2moro": "tomorrow",
    "tbh": "to be honest",
    "cya": "see you",
    "'m": "am",
    "i": "I",
    "k": "okay"
    "noice": "nice",
    "u": "you",
    "pls": "please",
    "plz" : "please"
    "'ll": "will",
    "'d": "would",
    "btw": "by the way",
    "becoz": "because",
    "yaya": "yea",
    "thnx": "thanks",
    "thenks": "thanks",
}


def preprocess(string_arg: str, should_expand=True):
    """
    EXPERIMENTAL
    Testing Required

    Remove unwanted characters, expand words, replace short forms
    and fix capitalization for certain pronouns
    :param string_arg: String argument which you would like to process
    :return: String stype containing expanded texts
    :return_type: <class 'str'>
    """
    logging.info("PREPROCESSOR: Received {}".format(string_arg))
    proc = string_arg
    proc = proc.replace("n't", " not").replace(
        "'re", " are"
    )  # replace short word to expanded words
    proc = proc.replace(" i ", " I ")
    k = nltk.word_tokenize(proc)
    if len(k) >= 1:
        k[0] = k[0].capitalize()
        if (k[0].lower().startswith("say")) or (k[0].lower().startswith("tell")):
            del k[0]
    if len(k) >= 1:
        if k[0] == "me":
            del k[0]  # Needs testing

    for i in range(len(k)):
        for j in short_forms:
            if not should_expand:
                continue

            if k[i].lower() == j:
                k[i] = short_forms[j]
    proc = " ".join(k)
    proc = proc.replace("$ wolf", "$wolf")
    logging.info("PREPROCESSOR: Returned {}".format(proc))
    return proc


def non_punkt_normalize(txt):
    return nltk.WordNetLemmatizer(txt)


def normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    # word tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))

    # remove ascii
    new_words = []
    for word in word_token:
        new_word = (
            unicodedata.normalize("NFKD", word)
            .encode("ascii", "ignore")
            .decode("utf-8", "ignore")
        )
        new_words.append(new_word)

    # Remove tags
    rmv = []
    for w in new_words:
        text = re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w)
        rmv.append(text)

    # pos tagging and lemmatization
    tag_map = nltk.defaultdict(lambda: wn.NOUN)
    tag_map["J"] = wn.ADJ
    tag_map["V"] = wn.VERB
    tag_map["R"] = wn.ADV
    lemmatizer = nltk.WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list


def purify(tokenized, args, lemma=False):
    """
    Scans tokenized text
    removes any common words in args
    :param tokenized:
    :param args:
    :return:
    """
    purified = []
    for token in tokenized:
        for element in args:
            if token.lower_ == element:
                break
            elif lemma and token.is_stop:
                break
        else:
            purified.append(str(token))
    return purified


def spac_token(statement, chatbot=False):
    try:
        if statement.doc:
            return statement.doc
        else:
            if chatbot:
                return chatbot.lp.nlp(str(statement))
            return False
    except AttributeError:
        if chatbot:
            return chatbot.lp.nlp(str(statement))
        return False


def tokenize(txt):
    word_token = nltk.word_tokenize(txt.lower())
    return word_token


def current_time():
    """Returns a tuple containing (hour, minute) for current local time."""
    import time

    local_time = time.localtime(time.time())
    return local_time.tm_hour, local_time.tm_min
