import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from yubichecker.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DocController(BaseController):

  def index(self):
    return render('/doc/index.html')
