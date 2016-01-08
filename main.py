import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

import jinja2
import os


template_dir = os.path.join(os.path.dirname(__file__), "templates")

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True
    )


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, params):
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, template_vars):
        self.write(self.render_str(template, template_vars))


class Greeting(db.Model):
    """
    Models an individual Guestbook entry with an author, content, and date.
    """
    author = db.StringProperty()
    content = db.StringProperty(multiline=True, indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)


def _GuestbookKey(guestbook_name=None):
    """
    Constructs a Datastore key for a Guestbook entity with guestbook_name.
    """
    return db.Key.from_path('Guestbook', guestbook_name)




class LessonHandler(Handler):

    def get(self, template_file, guestbook):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }

        self.render(template_file, template_values)
        self.render('the_web.html', template_values)


    def post(self, guestbook):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/?' + urllib.urlencode(query_params))




class MainPage(LessonHandler):
    
    def page_one(self):
        guestbook_one = 'lesson_one_guestbook'
        # self.render('the_web.html', template_values)
        self.get('the_web.html', guestbook_one)

    # def get(self):
    #     """Handle GET requests."""
    #     guestbook_name = self.request.get('guestbook_name', guestbook_one)
    #     greetings_query = Greeting.all().ancestor(
    #         _GuestbookKey(guestbook_name)).order('-date'),l l
    #     num_greetings = 10
    #     greetings = greetings_query.fetch(num_greetings)
    #     error = self.request.get("error")

    #     if users.get_current_user():
    #         url = users.create_logout_url(self.request.uri)
    #         url_linktext = 'Logout'
    #     else:
    #         url = users.create_login_url(self.request.uri)
    #         url_linktext = 'Login'

    #     template_values = {
    #         'greetings': greetings,
    #         'guestbook_name': urllib.quote_plus(guestbook_name),
    #         'url': url,
    #         'url_linktext': url_linktext,
    #         "error": error,
    #     }

    #     self.render("the_web.html", template_values)

    # def post(self):
    #     """Handle POST requests."""
    #     guestbook_name = self.request.get('guestbook_name', guestbook_one)
    #     greeting = Greeting(parent=_GuestbookKey(guestbook_name))

    #     if users.get_current_user():
    #         greeting.author = users.get_current_user().nickname()

    #     greeting.content = self.request.get('content')
    #     if greeting.content.strip():
    #         greeting.put()
    #         query_params = {'guestbook_name': guestbook_name, }
    #     else:
    #         error = "Please enter text to leave a comment"
    #         query_params = {'guestbook_name': guestbook_name, "error": error}
    #     self.redirect('/?' + urllib.urlencode(query_params))

guestbook_two = 'lesson_two_guestbook'


class LessonTwo(Handler):
    def get(self):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_two)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }
        self.render("structure.html", template_values)

    def post(self):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_two)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/structure?' + urllib.urlencode(query_params))

guestbook_three = 'lesson_three_guestbook'


class LessonThree(Handler):
    def get(self):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_three)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }

        self.render("styling.html", template_values)

    def post(self):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_three)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/styling?' + urllib.urlencode(query_params))

guestbook_four = 'servers_guestbook'


class ServersContent(Handler):
    def get(self):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_four)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }

        self.render("servers_content.html", template_values)

    def post(self):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_four)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/servers?' + urllib.urlencode(query_params))

guestbook_five = 'validating_input'


class ValidInput(Handler):
    def get(self):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_five)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }

        self.render("valid_input.html", template_values)

    def post(self):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_five)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/validation?' + urllib.urlencode(query_params))

guestbook_six = 'templates'


class UsingTemplates(Handler):
    def get(self):
        """Handle GET requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_six)
        greetings_query = Greeting.all().ancestor(
            _GuestbookKey(guestbook_name)).order('-date')
        num_greetings = 10
        greetings = greetings_query.fetch(num_greetings)
        error = self.request.get("error")

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            "error": error,
        }

        self.render("using_templates.html", template_values)

    def post(self):
        """Handle POST requests."""
        guestbook_name = self.request.get('guestbook_name', guestbook_six)
        greeting = Greeting(parent=_GuestbookKey(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        if greeting.content.strip():
            greeting.put()
            query_params = {'guestbook_name': guestbook_name, }
        else:
            error = "Please enter text to leave a comment"
            query_params = {'guestbook_name': guestbook_name, "error": error}
        self.redirect('/templates?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/structure", LessonTwo),
    ("/styling", LessonThree),
    ("/servers", ServersContent),
    ("/validation", ValidInput),
    ("/templates", UsingTemplates)
    ])
