###############################################
##               DISCLAIMER                  ##
## Code adapted from                         ##
##     https://github.com/lw4z/Similarities  ##
###############################################

from jiwer import wer
import nltk 
import distance
import re, math
from collections import Counter
from nltk.corpus import stopwords
from nltk import tokenize
import argparse
import os
from pathlib import Path


class CompareTexts:
    def __init__(self):
        self.WORD = re.compile(r'\w+')
        self.sws = stopwords.words('portuguese')

    # Stopwords removal
    def _text_normalized(self, text):
        palavras_tokenize = tokenize.word_tokenize(text, language='portuguese')
        filtered_sentence  = list(filter(lambda x: x.lower() not in self.sws, palavras_tokenize))
        return " ".join(filtered_sentence)

    # Cosine
    def _get_cosine_result(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def _text_to_vector(self, text):
        words = self.WORD.findall(text)
        return Counter(words)

    def _get_cosine(self, text1, text2):
        vector1 = self._text_to_vector(text1)
        vector2 = self._text_to_vector(text2)
        cosine = self._get_cosine_result(vector1, vector2)
        return cosine

    # Jaccard
    def _get_jaccard(self, text1, text2):
        jaccard = nltk.jaccard_distance(set(text1), set(text2))
        return jaccard

    # Levenshtein
    def _get_levenshtein(self, text1, text2):
        levenshtein = distance.levenshtein(text1, text2)
        return levenshtein

    # Word Error Rate
    def _get_wer(self, text1, text2):
        return wer(text1, text2)

    # Punctuations
    def _get_pontuation(self, text):
        numberOfFullStops = 0
        numberOfQuestionMarks= 0
        numberOfExclamationMarks= 0
        numberOfCommaMarks = 0
        numberOfColonMarks= 0
        numberTotalPunctuation = 0

        for line in text:
            numberOfFullStops += line.count(".")
            numberOfQuestionMarks += line.count("?")
            numberOfExclamationMarks += line.count("!")
            numberOfCommaMarks += line.count(",")
            numberOfColonMarks += line.count(":")

        numberTotalPunctuation = numberOfFullStops + numberOfCommaMarks + numberOfQuestionMarks + numberOfExclamationMarks + numberOfColonMarks
        return numberOfFullStops, numberOfCommaMarks, numberOfQuestionMarks, numberOfExclamationMarks, numberOfColonMarks, numberTotalPunctuation

    def compare_texts(self, test_text, gt_text):
        # Get punctuation
        numberOfPunctuation = self._get_pontuation(gt_text)

        # Stopwords removal
        # test1 = text_normalized(text1)
        # test2 = text_normalized(text2)

        out_str = ""
        # Similatities results
        out_str += "WER:         {:.2f}\n".format(self._get_wer(gt_text, test_text))
        out_str += "Jaccard:     {:.2f}\n".format(self._get_jaccard(gt_text, test_text))
        out_str += "Levenshtein: {}\n"   .format(self._get_levenshtein(gt_text, test_text))
        out_str += "Cosine:      {:.2f}\n".format(self._get_cosine(gt_text, test_text))

        # Punctuation results
        out_str += '\n'
        out_str += 'Quantidade de Pontos:           {}\n'.format(numberOfPunctuation[0])
        out_str += 'Quantidade de Virgulas:         {}\n'.format(numberOfPunctuation[1])
        out_str += 'Quantidade de Interrogações:    {}\n'.format(numberOfPunctuation[2])
        out_str += 'Quantidade de Exclamações:      {}\n'.format(numberOfPunctuation[3])
        out_str += 'Quantidade de Dois Pontos:      {}\n'.format(numberOfPunctuation[4])
        out_str += 'Quantidade Total de Pontuações: {}\n'.format(numberOfPunctuation[5])

        return out_str
