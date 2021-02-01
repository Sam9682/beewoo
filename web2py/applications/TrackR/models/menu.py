response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
force_scheme='https'
response.menu = [
(T('Accueil'),URL('default','index',scheme=force_scheme)==URL(),URL('default','index',scheme=force_scheme),[]),

(T('CAPTURE & AFFICHE TRAFFIC INTERNET'),URL('othsec','index',scheme=force_scheme)==URL(),URL('othsec','index',scheme=force_scheme),[(T('1- CAPTURE et AFFICHER le traffic internet de mon PC (option remontée du traffic sur beewoo.fr)'),URL('othsec','DisplayXtermFormSnifferAndGeolocMap',scheme=force_scheme)==URL(),URL('othsec','DisplayXtermFormSnifferAndGeolocMap',scheme=force_scheme)),(T(' - CAPTURE le traffic internet de mon PC (option remontée du traffic sur beewoo.fr)'),URL('othsec','DisplayXtermFormSniffer',scheme=force_scheme)==URL(),URL('othsec','DisplayXtermFormSniffer',scheme=force_scheme)),(T('2- AFFICHE mon traffic internet sur GoogleMAPS'),URL('trackrctrl','DisplayGeolocDbRT',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayGeolocDbRT',scheme=force_scheme)),(T('3- AFFICHE les anomalies de mon traffic internet sur GoogleMAPS)'),URL('trackrctrl','DisplayGeolocDbRTAno',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayGeolocDbRTAno',scheme=force_scheme))]),

(T('MACHINE LEARNING'),URL('othsec','index',scheme=force_scheme)==URL(),URL('othsec','index',scheme=force_scheme),[(T('Anomalie detection du traffic BRUT (OTHSEC SVM Unsupervised)'),URL('trackrctrl','DisplayMachLearnUnsup_OTHSEC',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayMachLearnUnsup_OTHSEC',scheme=force_scheme)),(T('Anomalie detection du traffic filtré (IPANALYZED SVM Unsupervised)'),URL('trackrctrl','DisplayMachLearnUnsup_IPANALYZED',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayMachLearnUnsup_IPANALYZED',scheme=force_scheme)),(T('Classification du traffic BRUT (OTHSE KNN k-nearest-neighbors)'),URL('trackrctrl','DisplayMachLearnKNN_OTHSEC',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayMachLearnKNN_OTHSEC',scheme=force_scheme)),(T('Importer un fichier FAIL2BAN et afficher les données avec PYGEOIP'),URL('trackrctrl','DisplayTrackRFormFail2Ban',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayTrackRFormFail2Ban',scheme=force_scheme))]),

(T('DATABASES & TOOLS'),URL('othsec','index',scheme=force_scheme)==URL(),URL('othsec','index',scheme=force_scheme),[(T('OTHSEC DB - Mon traffic Internet brut '),URL('othsec','DisplayOTHSECDbGrid',scheme=force_scheme)==URL(),URL('othsec','DisplayOTHSECDbGrid',scheme=force_scheme)),(T('IPANALYZED DB - Mon traffic Internet géolocalisé'),URL('othsec','DisplayIPANALYZEDDbGrid',scheme=force_scheme)==URL(),URL('othsec','DisplayIPANALYZEDDbGrid',scheme=force_scheme)),(T('LOGANALYSE DB - Mon traffic Internet blacklisté '),URL('othsec','DisplayLOGANALYZEDDbGrid',scheme=force_scheme)==URL(),URL('othsec','DisplayLOGANALYZEDDbGrid',scheme=force_scheme)),(T('IPLIGENCE DB - Base de référence pour la géolocalisation '),URL('ipligencectrl','index',scheme=force_scheme)==URL(),URL('ipligencectrl','index',scheme=force_scheme)), (T('Localiser une @IP sur Google MAP'),URL('trackrctrl','DisplayTrackRClientIPGeo',scheme=force_scheme)==URL(),URL('trackrctrl','DisplayTrackRClientIPGeo',scheme=force_scheme)), (T('WEBRTC entre utilisateurs'),URL('default','exec_webrtc',scheme=force_scheme)==URL(),URL('default','exec_webrtc',scheme=force_scheme))])
]
