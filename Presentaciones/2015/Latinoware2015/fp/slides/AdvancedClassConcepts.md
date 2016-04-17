<!SLIDE center subsection>
# Advanced Class Concepts

<!SLIDE>
# Ordering
Resource order is non-deterministic

    @@@ Puppet
    package { 'httpd':
      ensure => present,
    }
    
    service { 'httpd':
      ensure => running,
    }

No guarantee that the package will be installed before attempting to start the service.

<!SLIDE>
# References
To define order, we explicitly create relationships between resources. To do this, we use references:

    @@@ Puppet
    file { 'joker':
      ensure => file,
      path   => '/arkham/joker',
    }
    
    # The reference for this resource is:
    File['joker']

<!SLIDE>
# Ordering attributes
Meta-attributes can be used to specify relationships between resources

    @@@ Puppet
    package { 'openssh-server':
      ensure => installed,
    }
    
    service { 'sshd':
      ensure  => running,
      require => Package['openssh-server'],
    }

Both of these code snippets ensure that the package resource will be executed before the service.

    @@@ Puppet
    package { 'openssh-server':
      ensure => installed,
      before => Service['sshd'],
    }
    
    service { 'sshd':
      ensure => running,
    }

`before` and `require` create exactly the same relationship. There is no difference in using one or the other.

<!SLIDE>
# Refresh events

    @@@ Puppet
    file { 'sshd_config':
      ensure  => file,
      content => template('sshd/config.erb'),
      before  => Service['sshd'],
    }
    
    service { 'sshd':
      ensure => running,
    }

What happens if the file content changes? We need to reload the ssh service.

    @@@ Puppet
    file { 'sshd_config':
      ensure  => file,
      content => template('sshd/config.erb'),
      notify  => Service['sshd'],
    }
    
    service { 'sshd':
      ensure => running,
    }

The `notify` and `subscribe` attributes create the same relationships as `before` and `require`, but they also send a *refresh event* to the second resource.

<!SLIDE>
# Refresh effects

The effect of a refresh event depends on the resource type receiving it.

* **service**: restarts the service
* **exec**: runs the command. See the `refreshonly` attribute
* **mount**: attempts to unmount and remount
 
<!SLIDE>
# Order arrows
A compact way to define resource relationships:

    @@@ Puppet
    package { 'httpd':
      ensure => installed,
    } ->
    
    file { 'httpd.conf':
      ensure => file,
    } ~>
    
    service { 'httpd':
      ensure => running,
    }

Or:

    @@@ Puppet
    Package['httpd'] -> File['httpd.conf'] ~> Service['httpd']
    
    package { 'httpd':
      ensure => installed,
    }
    
    file { 'httpd.conf':
      ensure => file,
    }
    
    service { 'httpd':
      ensure => running,
    }

<!SLIDE>
# Puppet variables
## Define values in one place and re-use them in the manifest

    @@@ Puppet
    class httpd {
      $httpd_confdir = '/etc/httpd/conf'
      
      file { $httpd_confdir:
        ensure => directory,
      }
      
      file { "${httpd_confdir}/httpd.conf":
        ensure => file,
      }
    }

## Important! Variables in Puppet are actually *constants* - They can't be reassigned.

<!SLIDE>
# Data types
The main data types available are:

## String

    @@@ Puppet
    $keyword = 'Puppet'
    $phrase  = "This is a ${keyword} workshop with ${puppetversion}"

## Array

    @@@ Puppet
    $users = ['larry', 'curly', 'moe']
    user { 'stooge':
      groups => ['tv', 'movies', 'reruns'],
    }

## Hash

    @@@ Puppet
    $hosts = {
      'puppetmaster' => ['default', 'security'],
      'fileserver'   => ['default', 'webserver'],
      'workstation'  => 'default',
    }

<!SLIDE>
# Other data types

## Boolean

    @@@ Puppet
    $secure_flag = false
    if $secure_flag {
      include ::security
    } else {
      include ::moresecurity
    }

## Regex

    @@@ Puppet
    $pattern = /^[a-z]+$/
    if $somestring =~ $pattern {
      # ...
    }

## Undef

Undefined variable. Can be assigned `undef` explicitly.

<!SLIDE>
# Hands-on lab: variables
* Create a module that manages a "hosts file".
* Define the host list as a Puppet variable.

<!SLIDE>
# Conditionals

## if, else, elsif

    @@@ Puppet
    if $is_virtual {
      warning('Tried to include class ntp on virtual machine; this node may be misclassified.')
    }
    elsif $operatingsystem == 'Darwin' {
      warning('This NTP module does not yet work on our Mac laptops.')
    }
    else {
      include ntp
    }

## unless

    @@@ Puppet
    unless $memorysize > 1024 {
      $maxclient = 500
    }

## case

    @@@ Puppet
    case $operatingsystem {
      'Solaris':          { include role::solaris }
      'RedHat', 'CentOS': { include role::redhat  }
      /^(Debian|Ubuntu)$/:{ include role::debian  }
      default:            { include role::generic }
    }

<!SLIDE>
# Selectors
Selectors return a value depending on what the variable matches

      @@@ Puppet
      $rootgroup = $osfamily ? {
          'Solaris'          => 'wheel',
          /(Darwin|FreeBSD)/ => 'wheel',
          default            => 'root',
      }
      
      file { '/etc/passwd':
        ensure => file,
        owner  => 'root',
        group  => $rootgroup,
      }

<!SLIDE>
# Hands-on lab
* Create a class to manage an NTP client
* Make sure it uses conditionals to assign different servers depending on the network segment, if it's a virtual machine and on a possible "location" fact.

<!SLIDE>
# Class parameters
Define an "interface" for your classes. Interact with the parameters instead of editing the class.

    @@@ Puppet
    class sshd (
      $allow_root = false,
      $port       = 22,
    ) {
      package { 'openssh-server':
        ensure => installed,
      } ->
    
      file { 'sshd_config':
        ensure  => file,
        content => template('sshd/config'),
      } ~>
    
      service { 'sshd':
        ensure => running,
      }
    }

<!SLIDE>
# Using class parameters

    @@@ Puppet
    # sshd/examples/init.pp
    # instead of using "include ::ssh"
    
    class { '::sshd':
      port => 2222,
    }

This is called a *resource-like class declaration*

<!SLIDE>
# Hands-on lab: class parameters
* Modify your NTP class to take a "server" parameter
* Test it with different values in your examples directory
* Bonus round: you can add conditionals in your test manifest to assign different values to the class

<!SLIDE>
# Defined types
Create repeatable pieces of configuration *on the same server*

    @@@ Puppet
    #modules/admin_user/manifests/init.pp
    define admin_user (
      $username     = $title,
      $admin_group  = 'wheel',
      $homedir      = "/home/${username}",
      $ssh_pubkey   = undef,
    ) {
      user { $username:
        ensure  => present,
        homedir => $homedir,
        gid     => $admin_group,
      }
      
      file { $homedir:
        ensure => directory,
        owner  => $username,
      }
    
      if $ssh_pubkey {
        file { "${homedir}/.ssh":
          ensure => directory,
          owner  => $username,
          mode   => 0700,
        }
    
        ssh_authorized_key { "${username}_sshkey":
          ensure => present,
          user   => $username,
          key    => $ssh_pubkey,
          type   => 'ssh-rsa',
        }
      }
    }

<!SLIDE>
# Defined type usage
Once the type has been defined, we can use it as if it were any other resource type:

    @@@ Puppet
    #modules/admin_user/examples/admin_user_test.pp
    admin_user { 'carlos':
      homedir    => '/opt/carlos',
      ssh_pubkey => 'AAAZZZZB12345',
    }
    
    admin_user { 'john':
    }

<!SLIDE>
# Hands-on lab: defined types
* Create a defined type that creates a new ifcfg script to manage network interfaces.
* Make sure you use a path you can write to!

.break text

    @@@ Shell
    HWADDR="08:00:27:0C:5C:77"
    TYPE="Ethernet"
    NAME="eth0"
    ONBOOT="yes"
    # Either dhcp:
    BOOTPROTO="dhcp"
    # Or static IP
    BOOTPROTO="none"
    IPADDR="192.168.1.10"
    NETMASK="255.255.255.0"
    NETWORK="192.168.1.0"
