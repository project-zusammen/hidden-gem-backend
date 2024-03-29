import logging
import sys

from flask import Flask
from flask_cors import CORS
from app import commands
from app.extensions import (
    bcrypt,
    db,
    api,
    debug_toolbar,
    migrate,
)

from app.main.controller.review_controller import ns as review_ns
from app.main.controller.user_controller import ns as user_ns
from app.main.controller.comment_controller import ns as comment_ns
from app.main.controller.region_controller import ns as region_ns
from app.main.controller.appeal_controller import ns as appeal_ns
from app.main.controller.report_controller import ns as report_ns
from app.main.controller.tag_controller import ns as tag_ns


from app.main.controller.category_controller import ns as category_ns

from app.main.controller.bookmark_controller import ns as bookmark_ns


def create_app(config_object="app.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    register_extensions(app)
    register_errorhandlers(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(review_ns)
    api.add_namespace(user_ns)
    api.add_namespace(comment_ns)
    api.add_namespace(region_ns)
    api.add_namespace(appeal_ns)
    api.add_namespace(report_ns)
    api.add_namespace(tag_ns)
    api.add_namespace(bookmark_ns)
    api.add_namespace(category_ns)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
