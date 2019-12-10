"""main_a4.py

"""

import nltk
import re
import os
from nltk.corpus import PlaintextCorpusReader
import sys
import spacy
from spacy import displacy
import en_core_web_sm
#overrides max_length, doesn't seem to work?
#nlp = en_core_web_sm.load(max_length=4000000)
nlp = en_core_web_sm.load()


# NLTK stoplist with 3136 words (multilingual)
STOPLIST = set(nltk.corpus.stopwords.words())

# Vocabulary with 234,377 English words from NLTK
ENGLISH_VOCABULARY = set(w.lower() for w in nltk.corpus.words.words())

# The five categories from Brown that we are using
BROWN_CATEGORIES = ('adventure', 'fiction', 'government', 'humor', 'news')

# Global place to store Brown vocabularies so you calculate them only once
BROWN_VOCABULARIES = None


def is_content_word(word):
    """A content word is not on the stoplist and its first character is a letter."""
    return word.lower() not in STOPLIST and word[0].isalpha()


class PosTags(object):
    """Create POS-tagged class"""
    def __init__(self, text):

        self.text = text

        self.tagged = nltk.pos_tag(self.text)

        self.tag_freq = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in self.tagged)

        self.text_lower = nltk.Text(word.lower() for word in self.text)


class Text(object):

    def __init__(self, path, name=None):
        """Takes a file path, which is assumed to point to a file or a directory,
        extracts and stores the raw text and also stores an instance of nltk.text.Text."""
        self.name = name
        if os.path.isfile(path):
            self.raw = open(path).read()
        elif os.path.isdir(path):
            corpus = PlaintextCorpusReader(path, '.*')
            self.raw = corpus.raw()
        self.text = nltk.text.Text(nltk.word_tokenize(self.raw))
#        create tagged attribute using above POS class
        self.tagged = PosTags(self.text)

    def __len__(self):
        return len(self.text)

    def __getitem__(self, i):
        return self.text[i]

    def __str__(self):
        name = '' if self.name is None else " '%s'" % self.name
        return "<Text%s tokens=%s>" % (name, len(self))

    def token_count(self):
        """Just return the length of the text."""
        return len(self)

    def type_count(self):
        """Returns the type count, with minimal normalization by lower casing."""
        # an alternative would be to use the method nltk.text.Text.vocab()
        return len(set([w.lower() for w in self.text]))

    def sentence_count(self):
        """Return number of sentences, using the simplistic measure of counting period,
        exclamation marks and question marks."""
        # could also use nltk.sent.tokenize on self.raw
        return len([t for t in self.text if t in '.!?'])

    def most_frequent_content_words(self):
        """Return a list with the 25 most frequent content words and their
        frequencies. The list has (word, frequency) pairs and is ordered
        on the frequency."""
        dist = nltk.FreqDist([w for w in self.text if is_content_word(w.lower())])
        return dist.most_common(n=25)

    def most_frequent_bigrams(self, n=25):
        """Return a list with the 25 most frequent bigrams that only contain
        content words. The list returned should have pairs where the first
        element in the pair is the bigram and the second the frequency, as in
        ((word1, word2), frequency), these should be ordered on frequency."""
        filtered_bigrams = [b for b in list(nltk.bigrams(self.text))
                            if is_content_word(b[0]) and is_content_word(b[1])]
        dist = nltk.FreqDist([b for b in filtered_bigrams])
        return dist.most_common(n=n)

    def find_locs(self):
        doc = nlp(self.raw)
        duos = [(X.text, X.label_) for X in doc.ents if X.label_ in ('GPE','LOC','FAC')]
        return duos 

    def concordance(self, word):
        self.text.concordance(word)

    def search(self, pattern):
        return re.finditer(pattern, self.raw)

    def find_sirs(self):
        answer = set()
        for match in self.search(r"\bSir \S+\b"):
            answer.add(match.group())
        return sorted(answer)

    def find_brackets(self):
        answer = set()
        # use a non-greedy match on the characters between the brackets
        for match in self.search(r"([\(\[\{]).+?([\)\]\}])"):
            brackets = "%s%s" % (match.group(1), match.group(2))
            # this tests for matching pairs
            if brackets in ['[]', '{}', '()']:
                answer.add(match.group())
        return sorted(answer)

    def find_roles(self):
        answer = set()
        for match in re.finditer(r"^([A-Z]{2,}[^\:]+): ", self.raw, re.MULTILINE):
            answer.add(match.group(1))
        return sorted(answer)

    def find_repeated_words(self):
        answer = set()
        for match in self.search(r"(\w{3,}) \1 \1"):
            answer.add(match.group())
        return sorted(answer)

    def nouns_more_common_in_plural_form(self):
        return nouns_more_common_in_plural_form(self.tagged)

    def which_word_has_greatest_number_of_distinct_tags(self):
        return which_word_has_greatest_number_of_distinct_tags(self.tagged)

    def tags_in_order_of_decreasing_frequency(self):
        return tags_in_order_of_decreasing_frequency(self.tagged)

    def tags_that_nouns_are_most_commonly_found_after(self):
        return tags_that_nouns_are_most_commonly_found_after(self.tagged)

    def proportion_ambiguous_word_types(self):
        return proportion_ambiguous_word_types(self.tagged)

    def proportion_ambiguous_word_tokens(self):
        return proportion_ambiguous_word_tokens(self.tagged)


if len(sys.argv) > 1:
    if sys.argv[1] == '--tagger-train':
        train_tagger()

    elif sys.argv[1] == '--tagger-run':
        tag_a_sentence(sys.argv[2])

    elif sys.argv[1] == '--tagger-test' and sys.argv[2] == 'news':
        evaluate_news()

    elif sys.argv[1] == '--tagger-test' and sys.argv[2] == 'reviews':
        evaluate_reviews()
