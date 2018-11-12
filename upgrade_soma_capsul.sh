python3 -m pip uninstall capsul
git clone https://github.com/populse/capsul.git /tmp/capsul
cd /tmp/capsul
python3 setup.py install --user
cd /tmp
rm -rf /tmp/capsul

python3 -m pip uninstall soma-base
git clone https://github.com/populse/soma-base.git /tmp/soma-base
cd /tmp/soma-base
python3 setup.py install --user
cd /tmp
rm -rf /tmp/soma-base
