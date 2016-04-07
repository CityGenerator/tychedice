
class BaseConfiguration(object):
    # Statement for enabling the development environment
    DEBUG = True

    LOG_PATH = 'data/logging.json'



class ProductionConfiguration(BaseConfiguration):
    # Statement for enabling the development environment
    DEBUG = False

    LOG_PATH = 'data/logging.json'



class TestConfiguration(BaseConfiguration):
    # Statement for enabling the development environment
    DEBUG = True

    LOG_PATH = 'data/logging.json'


class IntegrationTestConfiguration(BaseConfiguration):
    # Statement for enabling the development environment
    DEBUG = True

    LOG_PATH='data/logging.json'


