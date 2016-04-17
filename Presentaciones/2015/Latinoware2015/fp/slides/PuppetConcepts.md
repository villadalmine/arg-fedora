<!SLIDE center subsection>
# Puppet Concepts & Good Practices

<!SLIDE>
# What is Puppet?

* Automation tool
* Infrastructure as code
* Models systems with a Domain Specific Language
* Centralized server stores all configs

<!SLIDE>
# Puppet Basic Concepts #

- What, not how
  - Define the desired end state of the system instead of the steps required to get there
  - Declarative vs Imperative
  - Idempotency
- Abstraction
  - Facter
  - Resource Abstraction Layer

<!SLIDE>
# What, not how
<table class="comparison">
<tr><th>Imperative</th><th>Declarative</th></tr>
<tr>
    <td>
        <pre class="highlight sh_shell">
            <code class="language-shell">
if [ 0 -ne $(getent passwd batman > /dev/null)$? ]
then
    useradd batman --gid detectives -n
fi

GID=`getent passwd batman | awk -F: '{print $4}'`
GROUP=`getent group $GID | awk -F: '{print $1}'`

if [ "$GROUP" != "$GID" ] && [ "$GROUP" != "detectives" ]
then
    usermod --gid $GROUP $USER
fi
            </code>
        </pre>
    </td>
    <td>
        <pre class="highlight sh_puppet">
            <code class="language-puppet">
user { 'batman':
  ensure => present,
  gid    => 'detectives',
}
            </code>
        </pre>
    </td>
<tr>
<tr>
    <td>
        <pre class="highlight sh_shell">
            <code class="language-shell">
if [ "`getent group detectives | awk -F: '{print $1}'`" == "" ]
then
    groupadd detectives
fi
            </code>
        </pre>
    </td>
    <td>
        <pre class="highlight sh_puppet">
            <code class="language-puppet">
group { 'detectives':
  ensure => present,
}
            </code>
        </pre>
    </td>
</tr>
</table>

<!SLIDE>
# "The Puppet way"

    @@@ Puppet
    user { 'batman':
      ensure  => present,
      gid     => 'detectives',
      homedir => '/batcave',
    }

* Clear intent and effects
* Readable
* Easier to maintain
* Dedicated error checking
* System independent
* *Idempotent*: only changes the system when it deviates from the desired state

<!SLIDE>
# Abstraction

## Facter
Extract information from systems with a consistent interface

    @@@ Shell
    $ facter operatingsystem
    CentOS
    $ facter ipaddress
    10.8.0.5
    $ facter osfamily
    RedHat

<!SLIDE>
# Resource Abstraction Layer (RAL)
## Resources
Common system concepts represented as *resource types*

    @@@ Puppet
    user { 'robin':
      ensure  => present,
      comment => 'Dick Grayson',
    }

    package { 'telnet':
      ensure => absent,
    }

    service { 'slapd':
      ensure => running,
    }

<!SLIDE>
# Resource Abstraction Layer (RAL)
## Providers
Implementation of those concepts via *resource providers*

    @@@ Shell
    # ls /opt/puppetlabs/puppet/lib/ruby/vendor_ruby/puppet/provider/package/
    aix.rb        fink.rb      pacman.rb   portage.rb      up2date.rb
    appdmg.rb     freebsd.rb   pip3.rb     ports.rb        urpmi.rb
    apple.rb      gem.rb       pip.rb      portupgrade.rb  windows
    aptitude.rb   hpux.rb      pkgdmg.rb   puppet_gem.rb   windows.rb
    apt.rb        macports.rb  pkgin.rb    rpm.rb          yum.rb
    aptrpm.rb     nim.rb       pkgng.rb    rug.rb          zypper.rb
    blastwave.rb  openbsd.rb   pkg.rb      sunfreeware.rb
    dpkg.rb       opkg.rb      pkgutil.rb  sun.rb

Providers map each resource type to the specific system's implementation

<!SLIDE>
# Resource types

`puppet describe --list` returns the full list of available types on a system

    @@@ Shell
    $ puppet describe --list
    These are the types known to puppet:
    augeas          - Apply a change or an array of changes to the  ...
    computer        - Computer object management using DirectorySer ...
    cron            - Installs and manages cron jobs
    exec            - Executes external commands
    file            - Manages files, including their content, owner ...
    filebucket      - A repository for storing and retrieving file  ...
    group           - Manage groups
    host            - Installs and manages host entries
    interface       - This represents a router or switch interface
    k5login         - Manage the `.k5login` file for a user
    macauthorization - Manage the Mac OS X authorization database
    mailalias       - .. no documentation ..
    maillist        - Manage email lists
    mcx             - MCX object management using DirectoryService  ...
    mount           - Manages mounted filesystems, including puttin ...
    [...]

<!SLIDE>
# Resource types

`puppet describe <type name>` returns the documentation for that type

    @@@ Shell
    $ puppet describe group

    group
    =====
    Manage groups. On most platforms this can only create groups.
    Group membership must be managed on individual users.
    On some platforms such as OS X, group membership is managed as an
    attribute of the group, not the user record. Providers must have
    the feature 'manages_members' to manage the 'members' property of
    a group record.
    
    
    Parameters
    ----------
    
    - **allowdupe**
        Whether to allow duplicate GIDs. Defaults to `false`.
        Valid values are `true`, `false`, `yes`, `no`. 
    [...]

<!SLIDE>
# Resource declaration syntax
All resource declarations have the following syntax:

    @@@ Puppet
    type { 'title':
      attribute1 => "value1",
      attribute2 => "value2",
    }

The *type* identifies the resource to use, and the *title* identifies that resource specifically.
Resource *attributes* affect that resource's properties, such as ownership for files or groups for users.

    @@@ Puppet
    file { '/etc/motd':
      ensure  => file,
      content => 'Created in Buenos Aires',
    }

The resource type is **file** and the resource title is **/etc/motd**.

<!SLIDE>
# Interacting with the RAL

## Using the RAL to read the system state

    @@@ Shell
    $ puppet resource file sudoers
    file { '/etc/sudoers':
      ensure   => 'file',
      content  => '{md5}ef817e657e3ffa6b0a88f59e3fc7241b',
      ctime    => '2015-08-24 11:45:09 -0300',
      group    => '0',
      mode     => '0440',
      mtime    => '2015-03-05 23:42:03 -0300',
      owner    => '0',
      selrange => 's0',
      selrole  => 'object_r',
      seltype  => 'etc_t',
      seluser  => 'system_u',
      type     => 'file',
    }

## Using the RAL to change the system state

    @@@ Shell
    $ puppet apply -e 'user { "gordon": ensure => present }'
    Notice: Compiled catalog for gotham.puppet.net in environment production in 0.51 seconds
    Notice: /Stage[main]/Main/User[gordon]/ensure: created
    Notice: Applied catalog in 0.11 seconds

`puppet apply` can be used inline or with a file.
`puppet apply --noop` will simulate the changes needed to reach the state defined.

<!SLIDE>
# Commonly used resource types

## Package

    @@@ Puppet
    package { 'httpd':
      ensure    => installed,
      provider  => 'yum',
    }

## Service

    @@@ Puppet
    service { 'sshd':
      ensure  => running,
      enable  => true,    #enables the service to start up on boot
    }

## File

    @@@ Puppet
    file { '/etc/resolv.conf':
      ensure  => file,
      content => "nameserver 8.8.8.8\nnameserver 8.8.4.4\n",
      owner   => 'root',
      group   => 'root',
    }

<!SLIDE>
# File resources
Manage files, directories and symbolic links

## Directories

    @@@ Puppet
    file { 'tomcat_dir':
      ensure => directory,
      path   => '/opt/tomcat',
    }

## Links

    @@@ Puppet
    file { 'symlink_to_motd':
      ensure => link,
      path   => '/etc/custom/motd',
      target => '/etc/motd,
    }

<!SLIDE>
# File contents
There are 2 basic ways of managing a file's content

## Content attribute

    @@@ Puppet
    file { '/opt/location':
      ensure  => file,
      content => 'Las Vegas, NV',
    }

Defines the string of characters in the file.

## Source attribute

    @@@ Puppet
    file { '/etc/sudoers':
      ensure => file,
      mode   => 0600,
      source => 'puppet:///modules/sudoers/sudoers.definitions',
    }

Defines a remote file path to copy to the file path.

<!SLIDE>
# Hands-on lab: file resource

* Create a file named content.pp and declare a file resource in it. Have the resource use the *content* attribute to insert a string into the file.
* Create a file named source.pp and declare a file resource that uses the *source* attribute to copy over another file.
* Test both *manifests* with `puppet apply --noop`

Syntax reminder:

    @@@ Puppet
    type { 'title':
      attribute1 => 'value',
      ...
    }

    file { '/tmp/something':
      ensure => file,
      source => '/home/workshop/pablo/something.source',
    }

<!SLIDE>
# Templates
Static files are nice, but what about those other servers that use other settings?

## ERB Templates
* Ruby templating system
* Allows us to define certain parameters and logic in our files
* One file, many server profiles

<!SLIDE>
# Template syntax
Templates allow us to use *variables* in our files. All facter facts are available as variables inside a template.

## Print a variable

    @@@ Ruby
    # /etc/motd
    This is a template test for <%= @fqdn %>. 
    We are running <%= @operatingsystem %> with Ruby <%= @ruby['version'] %>.

## Use conditionals and iteration

    @@@ Ruby
    # /opt/monitoring/mountpoints.cfg
    <% if @disks.length >= 2 -%>
      <%- @disks.each do |diskname,attributes| -%>
        <%= diskname %>: <%= attributes['size'] %>
      <%- end -%>
    <% end -%>

<!SLIDE>
# The *template* function
Called from a manifest, it parses the template and returns a static string.

## Template file

    @@@ Puppet
    file { '/opt/localdata':
      ensure  => file,
      content => template('/path/to/localdata.erb'),
    }
    
.break text

    @@@ Ruby
    # localdata.erb
    This host runs <%= @operatingsystem %>


<!SLIDE>
# Functions
Functions run *before* code compilation, allowing data to be manipulated before it's used.

## Functions that return a value (rvalue)

* *template*: parses an ERB template and returns a static string 
* *regsubst*: performs a regex substitution on a string
* *md5*: returns an md5 hash

## Functions that don't return a value

* *include*: incorporates another manifest into the current one
* *notice*: prints a message in the Puppet log
* *fail*: fail compilation with an error message

<!SLIDE>
# Hands-on lab: templates

* Create a manifest that manages an HTML file that prints assorted system information taken from facter.
* Test it with `puppet apply --noop`

Syntax reminder:

    @@@ Puppet
    file { '/opt/localdata':
      ensure  => file,
      content => template('/path/to/filename.erb'),
    }

.break text

    @@@ Ruby
    This is a Ruby <%= @ruby['version'] %> template

