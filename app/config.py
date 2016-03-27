import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  DEBUG = True
  TESTING = False
  REPOS_DIR_PATH = "repos"


class ProductionConfig(Config):
  DEBUG = False


class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True


class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True


class TestingConfig(Config):
  TESTING = True
