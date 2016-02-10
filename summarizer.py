## Example app for stack overflow question
# This person was not using quotes correctly in their curl

#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from flask import request
from flask import Flask
from flask import jsonify
import cgi
import cgitb
cgitb.enable()
import json

# form = cgi.FieldStorage()
# search = request.args.get("search")


LANGUAGE = "en"
SENTENCES_COUNT = 10

app = Flask(__name__)
app.debug = True


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return jsonify(dict(message='pong'))


@app.route('/', methods=['POST'])
def index():
    # url = "http://www.dawn.com/news/1216282"
    # -------------------------------------------------------------------------------
    # -------  Need help here ------------------#
    if request.method == 'POST':
         url = request.json.get('url')
         line_count = request.json.get('line_count')
    # ---------------------------------------------------------------------------

         parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
         print (parser)
    # stemmer = Stemmer(LANGUAGE)
    #
    # summarizer = Summarizer(stemmer)
    # summarizer.stop_words = get_stop_words(LANGUAGE)

    # s = ""
    # for sentence in summarizer(parser.document, SENTENCES_COUNT):
    #     s += str(sentence)

    return jsonify(dict(message='stuff'))

if __name__ == "__main__":
        app.run(host="127.0.0.1", port=5111)
