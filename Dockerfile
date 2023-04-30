FROM public.ecr.aws/amazonlinux/amazonlinux:2
# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0
RUN yum -y update
RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget tar gzip git tkinter postgresql make
RUN wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
RUN gunzip ./Python-3.8.0.tgz
RUN tar -xf ./Python-3.8.0.tar
WORKDIR ./Python-3.8.0
RUN ./configure --enable-optimizations
RUN make -j 8
RUN make altinstall
WORKDIR ..
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.8 get-pip.py
RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install simplejson pyparse pyparsing numpy scipy scikit-learn pandas matplotlib setuptools_rust pyjwt urllib3
RUN git clone --recursive https://github.com/web2py/web2py.git /opt/web2py
RUN mv /opt/web2py/handlers/wsgihandler.py /opt/web2py
RUN groupadd -g 1000 web2py
RUN useradd -r -u 1000 -g web2py web2py
EXPOSE 8080
LABEL AUTHOR="Samuel LEPETRE <slepetre@amazon.fr>"
ENV WEB2PY_ROOT=/opt/web2py
ENV WEB2PY_VERSION=
ENV WEB2PY_PASSWORD=Asbaasba1234
ENV WEB2PY_ADMIN_SECURITY_BYPASS=true
ENV UWSGI_OPTIONS=
ENV DB-BEEWOO=othsec.cluster-ctanxovsyvqd.eu-west-1.rds.amazonaws.com
ENV DB-PASSWORD=Asbaasba1
WORKDIR /opt/web2py
ADD ./web2py /opt/web2py
ADD entrypoint.sh /usr/local/bin/
RUN chown -R web2py:web2py /opt/web2py/
RUN chown -R web2py:web2py /usr/local/bin/
RUN chmod a+x /usr/local/bin/entrypoint.sh
RUN echo "db ${DB-BEEWOO}" > /etc/host.aliases
RUN echo "export HOSTALIASES=/etc/host.aliases" >> /etc/profile
RUN . /etc/profile
USER web2py
RUN . /etc/profile
CMD ["entrypoint.sh","http"]
