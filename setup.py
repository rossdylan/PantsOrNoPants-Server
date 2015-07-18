from setuptools import setup, find_packages


requires = ['flask',
            'flask-restful',
            'Flask-SQLAlchemy',
            'gunicorn',
            'gevent',
            'celery',
            'requests',
            'psycopg2', ]


setup(name='ponp_server',
      version='0.1.0',
      description='The API server for Pants or No Pants',
      author='Ross Delinger',
      author_email='ross.delinger@gmail.com',
      packages=find_packages(),
      install_requires=requires,
      zip_safe=False)
