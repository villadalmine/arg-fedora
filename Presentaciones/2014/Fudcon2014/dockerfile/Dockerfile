FROM fedora
RUN yum update -y
RUN yum groupinstall -y "Web Server" "php" "mysql" 
EXPOSE 80
RUN chmod 755 /start.sh
# EXPOSE 22
RUN ./start.sh
