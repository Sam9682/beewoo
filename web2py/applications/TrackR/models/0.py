from gluon.storage import Storage

settings = Storage()

settings.migrate = False
settings.title = 'BeeWoo OthSEC'
settings.subtitle = 'Internet trafic System Analyze with esgyn DB'
settings.author = 'Samuel LEPETRE'
settings.author_email = 'slepetre@beewoo.fr'
settings.keywords = 'Track,analyze,internet,tracking,web,request,esgyn,poc,secure'
settings.description = 'Intelligent Internet Trafic System'
settings.layout_theme = 'Default'
settings.database_uri = 'postgres://postgres:Asbaasba1@db/othsec'
settings.security_key = '48abe5ce-5c74-4ac2-af4b-d5f39bde7e8b'
settings.email_server = 'localhost'
settings.email_sender = 'info@beewoo.fr'
settings.email_login = 'info@beewoo.fr'
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
