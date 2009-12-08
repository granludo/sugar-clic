#!/usr/bin/env python


try:
    from sugar.activity import bundlebuilder
    bundlebuilder.start()
except ImportError:
    import os
    os.system("find ./ | sed 's,^./,JClicDownloader.activity/,g' > MANIFEST")
    os.system('rm gtktest.xo')
    os.chdir('..')
    os.system('zip -r JClicDownloader.xo JClicDownloader.activity')
    os.system('mv JClicDownloader.xo ./JClicDownloader.activity')
    os.chdir('JClicDownloader.activity')

