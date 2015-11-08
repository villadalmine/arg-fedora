<!SLIDE center subsection>
# Developing modules

<!SLIDE>
# Good practices in Module Development
## Desired module properties
- Sufficiently generic
- Composable
- Parameterized
- Readable
- Documented
- Clear scope
- Reasonable defaults
- Idempotent

<!SLIDE>
# Generating the correct module structure
`puppet module generate <author name>/<module name>` creates the basic structure of a module.

    @@@ Shell
    $ puppet module generate edrans/batman
    Puppet uses Semantic Versioning (semver.org) to version modules.
    What version is this module?  [0.1.0] --> 1.0.0
    Who wrote this module?  [edrans]
    What license does this module code fall under?  [Apache 2.0]
    How would you describe this module in a single sentence?
    --> Nana nana nana nana nana nana Batmaaan
    Where is this module's source code repository? --> batcave
    Where can others go to learn more about this module? --> gotham
    Where can others go to file issues about this module? --> wayne manor

    Notice: Generating module at edrans-batman...
    Notice: Populating templates...
    Finished; module generated in edrans-batman.
    edrans-batman/manifests
    edrans-batman/manifests/init.pp
    edrans-batman/metadata.json
    edrans-batman/README.md
    edrans-batman/Gemfile
    edrans-batman/tests
    edrans-batman/tests/init.pp
    edrans-batman/Rakefile
    edrans-batman/spec
    edrans-batman/spec/classes
    edrans-batman/spec/classes/init_spec.rb
    edrans-batman/spec/spec_helper.rb

<!SLIDE>
# Boilerplate
The module structure is Forge-ready and has most of the boilerplate to start working with unit tests

    @@@ Shell
    edrans-batman
    ├── Gemfile
    ├── manifests
    │   └── init.pp
    ├── metadata.json
    ├── Rakefile
    ├── README.md
    ├── spec
    │   ├── classes
    │   │   └── init_spec.rb
    │   └── spec_helper.rb
    └── tests
        └── init.pp
    
    4 directories, 8 files

<!SLIDE>
# Style
There's an Official Puppet Stye guide at docs.puppetlabs.com/guides/style_guide.html

    @@@ Puppet
    class style (
      $any    = undef,
      $one    = "$::puppetversion",
      $can    = 'write',
      $puppet = ['code'],
    ) {
    
      file { 'its_easy':
        ensure    => file,
        content   => 'If you try',
      }

    }

The gist:

* Readability matters
* Scoping and simplicity are key
* Your module is a piece of software


<!SLIDE>
# Design Patterns

There are several design patterns floating around. The two most commonly discussed and used are _Package/File/Service_ and _Roles and Profiles_.

<!SLIDE>
# Package/File/Service pattern

Basic class-level pattern:

* Install a package

.break text

    @@@ Puppet
    package { 'nginx':
      ensure => installed,
    }

* Modify configuration parameters

.break text

    @@@ Puppet
    file { 'nginx.conf':
      ensure  => file,
      path    => '/etc/nginx/nginx.conf',
      content => template('nginx/nginx.conf.erb'),
    }

* Manage the service state

.break text

    @@@ Puppet
    service { 'nginx':
      ensure => running,
      enable => true,
    }

<!SLIDE>
# Give it some order

Ensure that the module is predictable in its outcome

    @@@ Puppet
    package { 'nginx':
      ensure => installed,
    } ->

    file { 'nginx.conf':
      ensure  => file,
      path    => '/etc/nginx/nginx.conf',
      content => template('nginx/nginx.conf.erb'),
    } ~>

    service { 'nginx':
      ensure  => running,
      enable  => true,
      restart => '/etc/init.d/nginx reload',
    }

<!SLIDE>
# Increased readability
An extension of this pattern separates each "phase" of the pattern into a subclass of its own. This makes the module easier to understand at a glance and allows for extension in the future.

    @@@ Puppet
    # nginx/manifests/install.pp
    class nginx::install {
      package { 'nginx':
        ensure => installed,
      }
    }
    
    # nginx/manifests/configure.pp
    class nginx::configure {
      file { '/etc/nginx/nginx.conf':
        ensure  => file,
      }
    
      file { '/etc/nginx/conf.d/default.conf':
        ensure  => file,
      }
    }
    
    # nginx/manifests/service.pp
    class nginx::service {
      service { 'nginx':
        ensure  => running,
      }
    }

<!SLIDE>
# The main class

    @@@ Puppet
    # nginx/manifests/init.pp
    class nginx {
      Class['::nginx::install'] -> Class['::nginx::configure'] ~> Class['::nginx::service']

      include ::nginx::install
      include ::nginx::configure
      include ::nginx::service
    }

This looks fine, but... What happens when we do this?

    @@@ Puppet
    include nginx
    class { 'webapp':
      require => Class['nginx'],
    }

Classes will automatically **contain** any resources declared in them. This is not automatically true for **classes** declared in other classes.

<!SLIDE>
# The **contain** function
To ensure that subclasses are executed completely before other resources, we use the **contain** function:

    @@@ Puppet
    # nginx/manifests/init.pp
    class nginx {
      Class['::nginx::install'] -> Class['::nginx::configure'] ~> Class['::nginx::service']
      
      contain ::nginx::install
      contain ::nginx::configure
      contain ::nginx::service
    }

<!SLIDE>
# Hands-on lab: create an nginx module

* Use the package/file/service pattern (in a single manifest)
* Manage at least one config file
* Stick to the spirit of the style guide!

<!SLIDE>
# Roles & Profiles
On a larger scale, we have this site-wide pattern first proposed by Craig Dunn

* Business needs dictate server roles
* Abstract away the technology used for those roles

## "Billing app server"
## vs
## "Tomcat, Java, a WAR file, Apache+PHP and MySQL server"

<!SLIDE>
# Layers of abstraction

* Each *role* is composed of several instances of technology
* Each instance of technology is a *profile*
* Profiles are composed of basic classes, which in turn are composed of resources

.break text

    @@@ Puppet
    # roles/manifests/billing_app.pp
    class roles::billing_app {
      include ::profiles::tomcat
      include ::profiles::java
      include ::profiles::lamp
    }
    
    # profiles/manifests/lamp.pp
    class profiles::lamp {
      include ::apache
      include ::mysql
      include ::php
    }
    
    class apache {
      package { 'httpd':
        ensure => installed,
      }
      #[...]
    }

<!SLIDE>
# Puppet Forge
`forge.puppetlabs.com` hosts the community modules repository. This includes:

* Puppetlabs and community user ratings
* Links to source code, issue trackers
* Embedded documentation
* Compatibility notes

<!SLIDE>
# Using the Forge

* Download modules manually
* Use the `puppet module` tool

.break text

    @@@ Shell
    $ puppet module search iptables
    Notice: Searching https://forgeapi.puppetlabs.com ...
    NAME                         DESCRIPTION               AUTHOR        KEYWORDS
    arusso-iptables              iptables management       @arusso       iptables
    erwbgy-iptables              manage iptables allow...  @erwbgy       iptables
    example42-iptables           This module installs ...  @example42            
    zooz-iptables                Puppet iptables modul...  @zooz         iptables
    thias-rhel                   Configure Red Hat Ent...  @thias        iptables
    genebean-firewalld2iptables  A Puppet module to re...  @genebean     iptables
    danfoster-sitefirewall       A module to provide t...  @danfoster    iptables
    netmanagers-fail2ban         Puppet module for fai...  @netmanagers  iptables
    mighq-ipset                  Linux ipsets management.  @mighq        iptables
    puppetlabs-firewall          Manages Firewalls suc...  @puppetlabs   iptables
    bisscuitt-conntrackd         Manages conntrackd se...  @bisscuitt    iptables
    rharrison-lokkit             Use lokkit to manage ...  @rharrison    iptables
    
    $ puppet module install puppetlabs/apache
    Notice: Preparing to install into /etc/puppetlabs/code/environments/production/modules ...
    Notice: Downloading from https://forgeapi.puppetlabs.com ...
    Notice: Installing -- do not interrupt ...
    /etc/puppetlabs/code/environments/production/modules
    └─┬ puppetlabs-apache (v1.6.0)
      ├── puppetlabs-concat (v1.2.4)
      └── puppetlabs-stdlib (v4.8.0)

<!SLIDE>
# Hands-on lab: Real-life usage of community modules

* Pair up and use the following modules to configure a wordpress site:
  - hunner/wordpress
  - jfryman/nginx (or your own!)
  - puppetlabs/mysql
  - any other modules you might need
* Reminder: this is a good oportunity to test out the roles and profiles pattern
