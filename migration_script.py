# Script to make the model migrations

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import models
from app import db, create_app

from run import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
