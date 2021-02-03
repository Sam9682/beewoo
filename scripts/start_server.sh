#!/bin/bash
if [ "$UWSGI_OPTIONS" == '' ]; then
  UWSGI_OPTIONS='--master --thunder-lock --enable-threads'
fi

selectVersion() {
  if [ "$WEB2PY_VERSION" != '' ]; then
      git checkout $WEB2PY_VERSION
  fi
}

# Run uWSGI using the uwsgi protocol
#if [ "$1" = 'uwsgi' ]; then
# switch to a particular Web2py version if specificed
    selectVersion
      # add an admin password if specified
    if [ "$WEB2PY_PASSWORD" != '' ]; then
	python -c "from gluon.main import save_password; save_password('$WEB2PY_PASSWORD',443)"
    fi
      # run uwsgi
    runuser -u web2py -- uwsgi --http :8080 --protocol uwsgi --chdir /var/www/html/web2py --wsgi wsgihandler:application $UWSGI_OPTIONS > /dev/null 2> /dev/null < /dev/null &
#fi

# Run uWSGI using http
if [ "$1" = 'http' ]; then
  # switch to a particular Web2py version if specificed
    selectVersion
  # disable administrator HTTP protection if requested
    if [ "$WEB2PY_ADMIN_SECURITY_BYPASS" = 'true' ]; then
	    if [ "$WEB2PY_PASSWORD" == '' ]; then
	          echo "ERROR - WEB2PY_PASSWORD not specified"
	        exit 1
	    fi
        echo "WARNING! - Admin Application Security over HTTP bypassed"
	python -c "from gluon.main import save_password; save_password('$WEB2PY_PASSWORD',8080)"
        sed -i "s/elif not request.is_local and not DEMO_MODE:/elif False:/" \
	      $WEB2PY_ROOT/applications/admin/models/access.py
        sed -i "s/is_local=(env.remote_addr in local_hosts and client == env.remote_addr)/is_local=True/" \
          $WEB2PY_ROOT/gluon/main.py
      fi
       # run uwsgi
  exec uwsgi --http 0.0.0.0:8080 --wsgi wsgihandler:application $UWSGI_OPTIONS
fi
