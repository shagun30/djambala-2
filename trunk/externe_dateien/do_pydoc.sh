cd ..
export PYTHONPATH=$PYTHONPATH:/data/django_projects/dms_projekt/dms
export DJANGO_SETTINGS_MODULE=dms.settings
#epydoc --html -o Docs/pydocs ./
epydoc --check ./
cd externe_dateien
