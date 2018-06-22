"""module contains flask application settings"""
import os


class Config:
    """Base configuration."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../..'))
    app_dir = os.path.join(base_dir, 'webui')
    bin_dir = os.path.join(app_dir, 'bin')

    WKHTMLTOPDF_PATH_LOCAL = os.path.join(bin_dir, 'wkhtmltopdf')
    WKHTMLTOPDF_PATH_SYSTEM = \
        os.getenv('WKHTMLTOPDF_PATH_SYSTEM', 'wkhtmltopdf')
    PYTHON_PATH = {
        'linode': '/home/pydevd/projects/conv-webui/.venv/bin/python3'
    }['linode']

    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "?x1234567890x!"  # TODO: To env.
    SECRET_KEY = "!x1234567890x?"  # TODO: To env.
    DEBUG = False
    TESTING = False


class StagingConfig(Config):
    """Production configuration."""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig  # TODO: Change?
}
