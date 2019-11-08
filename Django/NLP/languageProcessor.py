import spacy
from NLP.entityMatchers import EntityMatchers
from NLP.sectionizer import Sectionizer


class LanguageProcessor:
    def __init__(self, text):
        nlp = spacy.load('en_core_web_lg')
        self.doc = nlp(text)

        self.sectionizer = Sectionizer(self.doc)
        self.entityMatcher = EntityMatchers(self.doc, nlp)

    def getDocumentSections(self):
        return self.sectionizer.getSectionsForAnnotation()

    def getDocumentEntities(self):
        return self.entityMatcher.getMatchesForAnnotation()
