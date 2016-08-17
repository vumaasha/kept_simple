from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from kiss.models import DBSession
from kiss.models.models import MyModel
import json
import codecs

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_kiss_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='home', renderer='templates/base.html.jinja2')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'kiss'}


@view_config(route_name='verify', renderer='templates/verify.html.jinja2')
def verify(request):
    return {'one': 1, 'project': 'kiss'}


@view_config(route_name='create', renderer='templates/create.html.jinja2')
def create(request):
    if request.method == 'POST':
        reader = codecs.getreader("utf-8")
        filename = request.POST['json-export'].filename
        input_file = request.POST['json-export'].file
        data = json.load(reader(input_file))
        size = len(data)
        return {'one': 1, 'project': 'kiss', 'name': filename, 'size':size}
    else:
        return {'one': 1, 'project': 'kiss'}
