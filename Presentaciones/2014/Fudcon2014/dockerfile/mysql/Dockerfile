FROM fedora:20
RUN yum -y install community-mysql-server community-mysql pwgen supervisor bash-completion psmisc net-tools; yum clean all
ADD ./start.sh /start.sh
ADD ./config_mysql.sh /config_mysql.sh
ADD ./supervisord.conf /etc/supervisord.conf
RUN chmod 755 /start.sh
RUN chmod 755 /config_mysql.sh
RUN /config_mysql.sh
EXPOSE 3306
CMD ["/bin/bash", "/start.sh"]
