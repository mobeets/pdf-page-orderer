import os
CURDIR = os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.abspath(os.path.join(CURDIR, '..'))

settings = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', '5000')),
        'server.environment': 'development',
    },
}

root_settings = {
    '/': {
        'tools.staticdir.root': ROOTDIR,
    },
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(ROOTDIR, 'static', 'favicon.ico')
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static'
    },
    '/tmp': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'tmp'
    }
}

pdf_helper_settings = {
    'media_dir': 'tmp',
    'full_media_dir': os.path.join(ROOTDIR, 'tmp'),
    'exe_path': os.path.join(ROOTDIR, 'bin', 'pdf_booklet.py')
}
