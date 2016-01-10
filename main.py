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

    def page(self, template_file, guestbook):
        """Generates web pages from templates"""
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

    def comment(self, guestbook, redirection):
        """Adds Comments to Datastore"""
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
        self.redirect(redirection + urllib.urlencode(query_params))


class MainPage(LessonHandler):

    def get(self):
        """Handle GET requests."""
        guestbook_one = 'lesson_one_guestbook'
        page_one = 'the_web.html'
        self.page(page_one, guestbook_one)

    def post(self):
        """Handle POST requests."""
        guestbook_one = 'lesson_one_guestbook'
        lesson_one_link = '/?'
        self.comment(guestbook_one, lesson_one_link)

guestbook_two = 'lesson_two_guestbook'


class LessonTwo(LessonHandler):
    def get(self):
        """Handle GET requests."""
        page_two = "structure.html"
        self.page(page_two, guestbook_two)

    def post(self):
        """Handle POST requests."""
        lesson_two_link = '/structure?'
        self.comment(guestbook_two, lesson_two_link)


guestbook_three = 'lesson_three_guestbook'


class LessonThree(LessonHandler):
    def get(self):
        """Handle GET requests."""
        page_three = "styling.html"
        self.page(page_three, guestbook_three)

    def post(self):
        """Handle POST requests."""
        lesson_three_link = '/styling?'
        self.comment(guestbook_three, lesson_three_link)

guestbook_four = 'servers_guestbook'


class ServersContent(LessonHandler):
    def get(self):
        """Handle GET requests."""
        page_four = "servers_content.html"
        self.page(page_four, guestbook_four)

    def post(self):
        """Handle POST requests."""
        lesson_four_link = '/servers?'
        self.comment(guestbook_four, lesson_four_link)


guestbook_five = 'validating_input'


class ValidInput(LessonHandler):
    def get(self):
        """Handle GET requests."""
        page_five = "valid_input.html"
        self.page(page_five, guestbook_five)

    def post(self):
        """Handle POST requests."""
        lesson_five_link = '/validation?'
        self.comment(guestbook_five, lesson_five_link)


guestbook_six = 'templates'


class UsingTemplates(LessonHandler):
    def get(self):
        """Handle GET requests."""
        page_six = "using_templates.html"
        self.page(page_six, guestbook_six)

    def post(self):
        """Handle POST requests."""
        lesson_six_link = '/templates?'
        self.comment(guestbook_six, lesson_six_link)


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/structure", LessonTwo),
    ("/styling", LessonThree),
    ("/servers", ServersContent),
    ("/validation", ValidInput),
    ("/templates", UsingTemplates)
    ])
