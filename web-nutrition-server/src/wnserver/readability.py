
import pickle
from nutrition.structure.environment import ROOT_FOLDER, READABILITY_MODEL, STANFORD_SERVER
from pycorenlp.corenlp import StanfordCoreNLP
from nutrition.feature.extract_feature import extract_features

class Readability(object):

    debug = False

    def __init__(self):
        # prepare to use Stanford parser
        self.nlp = StanfordCoreNLP(STANFORD_SERVER)
    
        # load trained model
        with open('{}/_model/{}'.format(ROOT_FOLDER, READABILITY_MODEL), 'rb') as file:
            self.model = pickle.load(file)
        
    def get_readability(self, text):
        if self.debug:
            print('text length: {} characters'.format(len(text)))
        
        # call stanford annotate api
        annotation = self.nlp.annotate(text[:1000], properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse',
            'outputFormat': 'json'
        })
        
        if type(annotation) is str:
            print('Error returned by stanford parser:', str)
            return 0
        
        x = extract_features(text, annotation)
        
        y = self.model.predict([x])[0]
        readability = max(0, min(6, (5-y))) * 100/6
        return readability
        
if __name__ == '__main__':
    print(Readability().get_readability('Google has announced major changes to its news aggregator service – Google News – at its I/O 2018 developer conference. The service now uses advanced machine learning and artificial intelligence tools to ensure that users receive in-depth information on any topic. Google News’ refresh has so far received a mixed reaction from users. Many users have complained of bugs in the new user interface (UI), which has already been rolled out on desktops as well as iOS and Android mobile apps. While some users reported a broken scroll, others felt disoriented by the excessive white space on their phones. This is probably because the new UI has not been optimised for different screen sizes. Another major issue facing the new Google News is the removal of important subjects like technology, education and science from the main app for Indian users. Some of these topics, however, appear in Google News’ US version. In order to follow your favourite topics like Technology on Google News, here’s what you should do: Tap on the menu button on the top left of the application or desktop. Then, tap on Favourites to look up your desired subjects. Search for technology, science or education, depending upon your preference. Note that adding a favourite will not automatically include the topic on the home page, the way older Google News used to. Instead, following your favourite topics will require a two-step process.'))
    pass