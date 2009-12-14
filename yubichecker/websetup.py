"""Setup the yubichecker application"""
import logging

from paste.deploy import appconfig
from yubichecker.config.environment import load_environment
from yubichecker import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup yubichecker here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info('Creating database')
    model.meta.create_all(bind=model.engine)
