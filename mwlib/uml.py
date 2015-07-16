#! /usr/bin/env python

# implement PlantUML extension
# https://www.mediawiki.org/wiki/Extension:PlantUML

import os
import tempfile
import subprocess
from hashlib import md5

_basedir = None


def _get_global_basedir():
    global _basedir
    if not _basedir:
        _basedir = tempfile.mkdtemp(prefix='uml-')
        import atexit
        import shutil
        atexit.register(shutil.rmtree, _basedir)
    return _basedir


def drawUml(script, basedir=None):
    if isinstance(script, unicode):
        script = script.encode('utf8')

    if basedir is None:
        basedir = _get_global_basedir()

    m = md5()
    m.update(script)
    ident = m.hexdigest()

    pngfile = os.path.join(basedir, '%s.png' % ident)

    if os.path.exists(pngfile):
        return pngfile

    scriptfile = os.path.join(basedir, ident + '.txt')

    with open(scriptfile, 'w') as scruml:
        scruml.write(script)

    plantumjar_path = os.path.join(os.path.dirname(__file__))

    cmd = subprocess.Popen('java -Djava.awt.headless=true -Dplantuml.include.path="%(plantumjar_path)s" -jar plantuml.jar -o "%(basedir)s" %(scriptfile)s' % {
        'plantumjar_path': plantumjar_path, 'scriptfile': scriptfile, 'basedir': basedir}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    err = cmd.communicate()

    if err[0]:
        return None

    if os.path.exists(pngfile):
        return pngfile

    return None
