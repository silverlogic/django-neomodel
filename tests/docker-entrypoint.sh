#!/bin/bash -xe
cd tests
python -c <<EOF |
from django.db import IntegrityError
try:
  python manage.py install_labels
except IntegrityError:
  print("Already installed")
EOF

python manage.py migrate # Apply database migrations
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

$@
python manage.py runserver 0.0.0.0:8000

