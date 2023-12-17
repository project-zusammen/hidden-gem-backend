import os
import unittest

from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand

from app.main import create_app, db

config_name = os.getenv('APP_SETTINGS') or 'dev'
app = create_app(config_name=config_name)

app.app_context().push()

cli = FlaskGroup(create_app=create_app)

migrate = Migrate(app, db)

cli.add_command('db', MigrateCommand)

@cli.command
def run():
    app.run()

@cli.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()
