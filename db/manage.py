#!/usr/bin/env python
from migrate.versioning.shell import main
import os

if __name__ == '__main__':
    db_url = os.environ.get('DATABASE_URL').replace('postgres:', 'postgresql:', 1)
    main(url=db_url, debug='False', repository='db')
