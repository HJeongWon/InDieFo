
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from test import app

manager = Manager(app)
manager.add_command('db', MigrateCommand)
if __name__ == "__main__":
    manager.run()