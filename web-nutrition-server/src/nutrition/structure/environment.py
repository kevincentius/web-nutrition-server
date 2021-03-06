
# SRC_FOLDER: path to the 'src' folder, needed to load models.
SRC_FOLDER = '/home/webnutrition/web-nutrition-server/web-nutrition-server/src'

# URL to the Stanford Core NLP Server
STANFORD_SERVER = 'http://localhost:9000'


# Twitter API access key
TWITTER_CONSUMER_KEY = "KQIA4UKnXvLfQZX8ycTCXxT1V"
TWITTER_CONSUMER_SECRET = "fUjoxxJoyZSe0KjMkPrtvnlQ3LPBSNOrokjC9Si7YrVFGy5OX6"
TWITTER_ACCESS_TOKEN = "1006645590992785408-OKIM9hFF41PTrXdXfX62LVS4UYa2Yv"
TWITTER_ACCESS_TOKEN_SECRET = "lyunnQNPeBPHHnlWBFmj5fKgS6OeX58O1UF3iNP54KDax"


# Credibility external resources
PAGE_RANK_QUOTE = 'https://www.checkpagerank.net/'
THRESHOLD_URL = 'google.com'
OPEN_PAGE_RANK_API_URL = 'https://openpagerank.com/api/v1.0/getPageRank';
OPEN_PAGE_RANK_API_KEY = 'gcsw00c8ccc0c8gk0wgwc0w408kc4sw4g4kgskks'

# ROOT_FOLDER: path to the folder that contains data sets and intermediate results
#   It is recommended to put this folder OUTSIDE the IDE's workspace as it may slow down the IDE.
#   This is not required to start the web nutrition server.
ROOT_FOLDER = '/home/webnutrition/data'

# Bias external resources
BIAS_DATADIR = SRC_FOLDER + '/nutrition/bias/data'
BIAS_MODEL = ['bias.pkl', 'tfidf.pkl']
BIAS_URLS = ['https://www.dropbox.com/s/hy1q9gy3maohyz6/bias.pkl?dl=1',
            'https://www.dropbox.com/s/kyclzw2gx80v24b/tfidf.pkl?dl=1']