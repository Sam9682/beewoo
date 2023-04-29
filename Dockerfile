FROM public.ecr.aws/amazonlinux/amazonlinux:2
# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0
RUN yum -y update && yum -y install epel-release  && yum -y install gcc git pcre-devel python3-devel python3-pip tkinter postgresql && pip install --upgrade pip  && pip install uwsgi  && git clone --recursive https://github.com/web2py/web2py.git /opt/web2py && mv /opt/web2py/handlers/wsgihandler.py /opt/web2py && groupadd -g 1000 web2py && useradd -r -u 1000 -g web2py web2py
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
ADD ./entrypoint.sh /usr/local/bin/
RUN chown -R web2py /opt/web2py/
RUN chown -R web2py /usr/local/bin/
RUN echo "db ${DB-BEEWOO}" > /etc/host.aliases
RUN echo "export HOSTALIASES=/etc/host.aliases" >> /etc/profile
RUN . /etc/profile
RUN pip3 install psycopg2 simplejson pyparse pyparsing numpy scipy scikit-learn pandas matplotlib setuptools_rust pyjwt urllib3
USER web2py
RUN . /etc/profile
CMD ["./entrypoint.sh","http"]
