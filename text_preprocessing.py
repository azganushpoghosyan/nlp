# Importing libraries
import pandas as pd
import numpy as np
import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from textblob import Word, TextBlob
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')
import re

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('vader_lexicon', quiet=True)

sample_text = 'Overview:\nThe PBNA Insights Reporting Analyst’s role will work primarily with Sparkling team where his/her role will be focused on enhancing and automating business reporting to fuel stronger, faster business performance insight for the PBNA Marketing and Insights teams. This includes connecting multiple data sources through curated metrics and developing calculated metrics to focus on the key outcome and diagnostic measures. A critical element of this role is to be able to deliver the strategic presentation focused around future Growth for PepsiCo.\nResponsibilities:\nExecute against team charter for Reporting vertical within SSC\no Execute market, portfolio, and brand level reporting of marketing KPI performance (utilizing dashboards, templated decks, and reporting tools)\no Leverage business performance explanations from teams around the world to incorporate considerations beyond data into reporting\no Explain business performance, drivers, and optimization opportunities\no Monitor key channel, customer, competitor (incl. PL) and emerging player performance and execute reporting at required intervals\no Deliver against needs of stakeholders, requestors and sector/functional leaders\no Support processes for output adherence and delivery to agreed scope – in line with the agreed timelines, aligned templates and content management\no Monitor and act upon regular feedback inputs from deliverables end-users and Business Partners\no Flag and monitor any business risks related to delivering the operational output (facilities, IT resources, recruitment efforts)\no Primary executor responsible for flawless support process and structure, including knowledge management and transfer\no Support communication processes with Reporting vertical leaders and Business Partners (project planning, workflow monitoring, quality checks, on-going changes)\no Help Reporting vertical leadership develop and finetune internal COE processes (work-flow mapping, pain-points and bottlenecks management) both related to service delivery and internal center operations\no Improve existing processes based on frequent end-user and Business Partner feedback loop Qualifications:'
df = pd.DataFrame({'original_text': [sample_text]})

"""
Processing

*   Standardize text: make lowercase
*   Remove punctuation
*   Remove numbers
*   Remove english stopwords
*   Create tokens from words
*   Stem the tokens
*   Lemmatize the tokens

"""

def text_preprocessing(text):
    """
    Preprocesses the raw text applying the following steps: standardize, remove numbers, punctuation and stopwords, stem and lemmatize the words.
    Returns a tuple containing the result of each of the above steps applied
    """

    # remove newline characters
    combined_text = text.replace('\n', ' ')

    # standardization of letters (make lowercase)
    standardized_text = combined_text.lower()

    # remove punctuation
    no_punctuation = re.sub(r'[^\w\s]', '', standardized_text)

    # remove numbers
    no_numbers = re.sub(r'\d', '', no_punctuation)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    no_stopwords = " ".join([word for word in no_numbers.split() if word not in stop_words])

    # tokenization
    tokens = nltk.word_tokenize(no_stopwords)

    # spacy tokenization
    nlp = spacy.load('en_core_web_sm')
    doc_tokenize = nlp(no_stopwords)
    tokens_spacy = [token.text for token in doc_tokenize]

    # stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens_spacy]

    # lemmatization
    sentence = " ".join(tokens_spacy)
    doc_lemmitize = nlp(sentence)
    lemmatized_tokens = [token.lemma_ for token in doc_lemmitize]

    # final cleaning: remove empty strings, single letters and duplicates

    clean_data = [token for token in list(set(lemmatized_tokens)) if token.strip()  != '' and token not in (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                                                                                                             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                                                                                                             'u', 'v', 'w', 'x', 'y', 'z'])]

    return (standardized_text, no_punctuation, no_numbers, no_stopwords, stemmed_tokens, lemmatized_tokens, clean_data)

standardized_text, no_punctuation, no_numbers, no_stopwords, stemmed_tokens, lemmatized_tokens, clean_data = text_preprocessing(sample_text)

df['standardized_text'] = standardized_text
df['no_punctuation'] = no_punctuation
df['no_numbers'] = no_numbers
df['no_stopwords'] = no_stopwords
df['stemmed_tokens'] = " ".join(stemmed_tokens)
df['lemmatized_tokens'] = " ".join(lemmatized_tokens)
df['clean_data'] = " ".join(clean_data)
df.head()
