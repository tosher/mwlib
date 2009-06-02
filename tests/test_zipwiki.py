#! /usr/bin/env py.test

import os
import tempfile

from mwlib import parser, zipwiki

class TestZipWiki(object):
    def setup_class(cls):
        fd, cls.zip_filename = tempfile.mkstemp()
        os.close(fd)
        print 'generating ZIP file'
        rc = os.system('mw-zip -c :en -o %s "The Living Sea"' % cls.zip_filename)
        print 'ZIP file generation finished'
        assert rc == 0, 'Could not create ZIP file. Is mw-zip in PATH?'
    
    def teardown_class(cls):
        if os.path.exists(cls.zip_filename):
            os.unlink(cls.zip_filename)
    
    def setup_method(self, method):
        self.wikidb = zipwiki.Wiki(self.zip_filename)
        self.imagedb = zipwiki.ImageDB(self.zip_filename)
    
    def teardown_method(self, method):
        self.imagedb.clean()
    
    def test_getRawArticle(self):
        a = self.wikidb.getRawArticle(u'The Living Sea')
        assert isinstance(a, unicode)
        assert len(a) > 0
    
    def test_getParsedArticle(self):
        p = self.wikidb.getParsedArticle(u'The Living Sea')
        assert isinstance(p, parser.Article)
    
    def test_getURL(self):
        url = self.wikidb.getURL(u'The Living Sea')
        assert url == 'http://en.wikipedia.org/w/index.php?title=The_Living_Sea'

    def test_getTemplate(self):
        t = self.wikidb.getTemplate(u'Infobox Film')
        assert isinstance(t, unicode)
        t = self.wikidb.getTemplate(u'no-such-template')
        assert t is None
    
    def test_ImageDB(self):
        p = self.imagedb.getDiskPath(u'Thelivingseaimax.jpg')
        assert isinstance(p, basestring)
        assert os.path.isfile(p)
        assert os.stat(p).st_size > 0
        assert p == self.imagedb.getDiskPath(u'Thelivingseaimax.jpg', 123)
        
        url = self.imagedb.getURL(u'Thelivingseaimax.jpg')
        assert url == 'http://upload.wikimedia.org/wikipedia/en/1/13/Thelivingseaimax.jpg'
        
        templates = self.imagedb.getImageTemplates(u"Thelivingseaimax.jpg")
        print templates
        assert templates

        contribs = self.imagedb.getContributors(u"Thelivingseaimax.jpg")
        print contribs
        assert contribs

    def test_getSource(self):
        src = self.wikidb.getSource(u'The Living Sea')
        print src

        interwikimap = src['interwikimap']
        assert interwikimap
        assert isinstance(interwikimap, dict)

        loc = src['locals']
        assert loc
        assert isinstance(loc, basestring)
