import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.database import db
from app.users.models import User, Role, RolesUsers

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, RolesUsers=RolesUsers)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
