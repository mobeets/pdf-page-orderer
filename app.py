import os
import cgi
import urllib.request, urllib.parse, urllib.error
from subprocess import Popen
from tempfile import NamedTemporaryFile

import cherrypy
from mako.lookup import TemplateLookup

import conf
import bin.pdf_booklet

lookup = TemplateLookup(directories=['templates'])
class Root(object):
    def __init__(self, media_dir, media_path, exe_path):
        self.media_dir = media_dir
        self.media_path = media_path
        self.exe_path = exe_path

    @cherrypy.expose
    def index(self, *tmp, **data):
        result, error = '', ''
        if cherrypy.request.method == 'POST':
            if not error:
                try:
                    pps = int(data['pages_per_sheet'])
                    sp = 1 #int(data['start_page'])
                except:
                    error = 'Error processing input. Make sure to input integers for the last two form arguments.'
            if not error and pps % 2 == 1:
                error = 'Value above must be even.'
            if not error:
                try:
                    myfile = data['myfile']
                    inf = self.upload(myfile)
                except:
                    error = 'Error uploading file.'
            if not error:
                error, result = self.process(inf, pps/2, sp)
        error = '' if error is None else error
        result = '' if result is None else result
        tmp = lookup.get_template('index.html')
        return tmp.render(result=result, error=error)

    def upload(self, myfile):
        outfile = self.destfile()
        with open(outfile, 'wb') as f:
            f.write(myfile.file.read())
        return outfile

    def test_pdf(self, infile):
        try:
            bin.pdf_booklet.read(infile)
        except Exception as e:
            return "ERROR reading pdf: " + str(e)

    def process(self, inf, pps, sp):
        outf = self.destfile()
        err = self.test_pdf(inf)
        if err:
            return err, None
        args = ['python', self.exe_path, '--infile', inf, '--outfile', outf, '--pairs_per_sheet', str(pps), '--start_page', str(sp)]
        print('=========================')
        print(' '.join(args))
        print('=========================')
        Popen(args)
        outf_name = os.path.split(outf)[1]
        return None, 'Your new .pdf is <a href="/{0}/{1}">here</a> (temporarily).'.format(self.media_dir, outf_name)

    def download_file(self, url, outfile):
        urllib.request.urlretrieve(url, outfile)

    def destfile(self):
        f = NamedTemporaryFile(suffix='.pdf', dir=self.media_path, delete=False)
        f.close()
        return f.name

def inner_main(settings):
    media_dir = settings['media_dir']
    media_path = settings['full_media_dir']
    exe_path = settings['exe_path']
    if not os.path.exists(media_path):
        os.mkdir(media_path)
    return Root(media_dir, media_path, exe_path)

def main():
    cherrypy.config.update(conf.settings)
    
    page_order_app = inner_main(conf.pdf_helper_settings)
    root_app = cherrypy.tree.mount(page_order_app, '/', conf.root_settings)
    root_app.merge(conf.settings)

    if hasattr(cherrypy.engine, "signal_handler"):
        cherrypy.engine.signal_handler.subscribe()
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
