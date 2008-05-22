rm -r /tmp/dms
rm /tmp/dms.tgz
cd ..
svn export ./ /tmp/dms
cd /tmp
tar -czvf dms.tgz dms
cd /data/django_projects/dms_projekt/dms/externe_dateien

