<!SLIDE center subsection>
# Modules and Classes

<!SLIDE>
# Classes & namespaces
A class (in Puppet) is a collection of resource declarations.

    @@@ Puppet
    class sshd {
      package { 'openssh-server':
        ensure => installed,
      }
    
      file { '/etc/sshd_config':
        ensure  => file,
        content => '...',
      }
     
      service { 'sshd':
        ensure => running,
        enable => true,
      }
    }

Subclasses can be declared to logically group certain configuration groups.

    @@@ Puppet
    class sshd::bastion {
      include ::sshd
    
      file { '/etc/sshd_config_extra':
        ensure  => file,
        content => '...',
      }
    }

<!SLIDE>
# Module layout & autodiscovery
A *module* is a collection of directories that contain manifests with class definitions and any other files, such as static files or templates.

* Predefined structure to allow Puppet to autoload all classes
* Ease of redistribution
* Separation of different scopes

.break text

    @@@ Shell
    modules/
    └── sshd
        ├── files
        │   └── ssh_config_extra
        ├── manifests
        │   └── init.pp
        └── templates
            └── ssh_config.erb

<!SLIDE>
# Creating modules

* The *manifests* directory contains all of the Puppet code
* The main module class must be contained in a file named `init.pp`

## Referencing files
In `source` attributes:

    @@@ Puppet
    file { '/etc/resolv.conf':
      ensure => file,
      source => 'puppet:///modules/resolv/resolv.conf',
    }

In template functions:

    @@@ Puppet
    file { '/etc/resolv.conf':
      ensure  => file,
      content => template('resolv/resolv.conf.erb'),
    }
