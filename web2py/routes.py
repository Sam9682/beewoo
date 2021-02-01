#!/usr/bin/python
#ended up using nano to do this
routes_in = (
  ('/.well-known/acme-challenge/$anything','/TrackR/static/$anything'),
  ('/admin/$anything', '/admin/$anything'),
  ('/static/$anything', '/TrackR/static/$anything'),
  ('/appadmin/$anything', '/TrackR/appadmin/$anything'),
  ('/favicon.ico', '/TrackR/static/favicon.ico'),
  ('/robots.txt', '/TrackR/static/robots.txt'),
  ('/', '/TrackR/default/index'),
)
routes_out = [(x, y) for (y, x) in routes_in[:-2]]
#routers = dict( 
#    BASE = dict( 
#        default_application='TrackR', 
#    ) 
#) 
#default_application = 'TrackR'
#default_controller = 'default'
#default_function = 'index'
routes_onerror = [
        ('TrackR/400', '!'),
        ('TrackR/401', '!'),
        ('TrackR/509', '!'),
        ('TrackR/*', '/TrackR/errors/index'),
        ('*/*', '/TrackR/errors/index'),
    ]
