
import pickle
from pycorenlp.corenlp import StanfordCoreNLP

from nutrition.readability.feature_extraction import extract_features
from nutrition.structure.environment import STANFORD_SERVER, SRC_FOLDER
from wnserver.response import Label


class Readability(object):

    debug = False

    def __init__(self):
        # prepare to use Stanford parser
        self.nlp = StanfordCoreNLP(STANFORD_SERVER)

        # load trained model
        with open(SRC_FOLDER + '/models/readability', 'rb') as file:
            self.model = pickle.load(file)  # DataSet('cepp').load_model('random-forest')

    def get_readability(self, text):
        if self.debug:
            print('text length: {} characters'.format(len(text)))

        # call stanford annotate api
        if self.debug:
            print('Calling Stanford API...')
        annotation = self.nlp.annotate(text[:1000], properties={
            'annotators': 'lemma,parse',
            'outputFormat': 'json'
        })
        if self.debug:
            print('Calling Stanford API done.')

        if type(annotation) is str:
            print('Error returned by stanford parser:', annotation)
            return 0

        x = extract_features(text, annotation)
        
        y = self.model.predict([x])[0]

        return Label(100 - y*20, [])


if __name__ == '__main__':
    print(Readability().get_readability('Google has announced major changes to its news aggregator service – Google News – at its I/O 2018 developer conference. The service now uses advanced machine learning and artificial intelligence tools to ensure that users receive in-depth information on any topic. Google News’ refresh has so far received a mixed reaction from users. Many users have complained of bugs in the new user interface (UI), which has already been rolled out on desktops as well as iOS and Android mobile apps. While some users reported a broken scroll, others felt disoriented by the excessive white space on their phones. This is probably because the new UI has not been optimised for different screen sizes. Another major issue facing the new Google News is the removal of important subjects like technology, education and science from the main app for Indian users. Some of these topics, however, appear in Google News’ US version. In order to follow your favourite topics like Technology on Google News, here’s what you should do: Tap on the menu button on the top left of the application or desktop. Then, tap on Favourites to look up your desired subjects. Search for technology, science or education, depending upon your preference. Note that adding a favourite will not automatically include the topic on the home page, the way older Google News used to. Instead, following your favourite topics will require a two-step process.').dict)