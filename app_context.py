from flask import Flask, render_template_string, current_app
from flask.views import View


stuff = "<h1>Hello World</h1>"

class MyClass(View):
    def __init__(self):
        pass

    def my_function(self):
        pass

    def dispatch_request(self):
        return render_template_string(stuff)


def create_app(package_name, settings=None):

    app = Flask(package_name, template_folder='templates')

    if settings is not None:
        app.config.from_object(settings)

    return app


if __name__ == '__main__':
    app = create_app(__name__)

    app.add_url_rule('/hello', view_func = MyClass.as_view('my_function'))

    app.run(debug=True)
