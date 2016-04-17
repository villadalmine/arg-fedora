# Base on the Fedora image created by Matthew
FROM mattdm/fedora

# Install the JBoss Application Server 7
RUN yum install -y jboss-as

# Run the JBoss AS after the container boots
ENTRYPOINT /usr/share/jboss-as/bin/launch.sh standalone standalone.xml 0.0.0.0
