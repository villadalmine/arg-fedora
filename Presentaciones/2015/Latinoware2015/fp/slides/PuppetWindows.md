<!SLIDE center subsection>
# Puppet & Windows

<!SLIDE>
# Scope

* Most versions of Windows (down to 2003 R2) are supported and have official installers for the Puppet Agent
* The Puppet Master can't be run on Windows
* Support for most commands and resources, with some exceptions
* System-specific resources for Windows-only configuration concepts

<!SLIDE>
# Running Puppet

## Supported commands

* puppet agent
* puppet apply
* puppet module
* puppet resource
* puppet config
* puppet help
* puppet man

Note: most of these commands need to be run with a user with administrative permissions

<!SLIDE>
# Windows core resources

Supported core resources for Windows:

* file
* user
* group
* scheduled\_task
* package
* service
* exec
* host

<!SLIDE>
# Forge modules:

* puppetlabs/acl
* puppetlabs/registry
* puppetlabs/reboot
* puppetlabs/dism
* puppetlabs/powershell

All of these can be installed together by installing `puppetlabs/windows`

<!SLIDE>
# Writing manifests

Windows is fundamentally different from \*nix in several ways. Puppet attempts to abstract away most of it, but some of it "leaks over"

* File paths: Forward slash or backslash?
* Line endings: CRLF vs LF
* Facts: OS-specific information

<!SLIDE>
# File paths

If the file path is being passed directly to a Windows program, backslashes may be mandatory. Otherwise, forward slashes can be used safely in most cases.

* Mandatory backslashes:

  - Any file paths included in the *command* of a scheduled\_task resource.
  - Any file paths included in the *install\_options* of a package resource.

*  Backslashes supported, forward slashes recommended for consistency:

  - The *path* attribute or *title* of a file resource
  - The *source* attribute of a package resource
  - Local paths in a file resource's *source* attribute (local to the agent)
  - The *command* of an exec resource

* Forward slashes only:

  - Template paths
  - Remote paths in a file resource's *source* (puppet:/// URIs)

<!SLIDE>
# File paths example

    @@@ Puppet
    file { 'C:/Windows/System/some.dll': # This could be C:\Windows\System\some.dll too
      ensure => file,
      source => 'puppet:///modules/windows_dlls/other.dll', # Needs forward slashes
    }
    
    scheduled_task { 'call-me-cron':
      ensure  => present,
      command => 'C:\Program Files\NotCron\cron.exe', # Needs backslashes
      trigger => {
        schedule   => daily,
        start_time => '03:30',
      },
    }

<!SLIDE>
# Escaping backslashes

When using double quotes, you need to use double backslashes for each literal backslash:

    @@@ Puppet
    $filepath = "I'm a path! C:\\\\Look\\\\at\\\\me"

When using single quotes, backslashes are literal _except_ when followed by a single quote. Then, they are escaping the single quote character:

    @@@ Puppet
    $filepath = 'I\\'m a path! C:\Look\at\me'

## Remember: readability should take precedence! Choose whichever is clearer

<!SLIDE>
# Line endings

Windows uses CRLF line endings, while \*nix uses LF line endings. Puppet will *not* convert between them in most cases.

* In file resources, when using *content* or *source*, Puppet will use whichever line endings are present in the content.
* In other resources that make partial changes to a file's content (like the host resource), Puppet will convert between the two.

<!SLIDE>
# User management

Puppet can manage local users and groups. The core user resource doesn't manage domain users, but the group resource supports adding domain users as members.

Group and user names can take any of the following forms. Please ensure you are consistent throughout the code!

- Administrators
- \<host\>\Administrators
- BUILTIN\Administrators
- S-1-5-32-544

<!SLIDE>
# Installing packages

Since there is no Windows package manager by default, we have a few options:

* The MSI provider for the package resource doesn't support URLs in the source attribute. Declare a file resource to download the file and then the package resource:

.break text

    @@@ Puppet
    
    file { 'C:/temp/sqlncli.msi':
      ensure => file,
      source => 'puppet:///modules/mssql/sqlncli.msi',
    } ->
    package { 'Microsoft SQL Server Native Client':
      ensure => installed,
      source => 'C:/temp/sqlncli.msi',
      install_options => [
          { 'USERNAME' => 'Administrator' },
          { 'IACCEPTSQLNCLILICENSETERMS' => 'YES'}
      ],
    }

* Use a network share to distribute the packages:

.break text

    @@@ Puppet
    
    package { 'Microsoft SQL Server Native Client':
      ensure  => installed,
      source  => '\\NAS\Installation_media\sqlncli.msi',
      install_options => [
          { 'USERNAME' => 'Administrator' },
          { 'IACCEPTSQLNCLILICENSETERMS' => 'YES'}
      ],
    }

<!SLIDE>
# Chocolatey

"Chocolatey is like apt-get, but built with Windows in mind"

* Uses the NuGet packaging system
* Originally for .NET apps, but any app can be packaged and distributed
* The chocolatey/chocolatey module includes a *chocolatey* provider
* Allows us to use the package resource without specifying installer paths:

.break text

    @@@ Puppet
    package { 'notepadplusplus':
      ensure   => installed,
      provider => 'chocolatey',
    }

<!SLIDE>
# Reboot!

Some packages require a reboot to complete their installation. They may not function properly until then. `puppetlabs/reboot` allows us to manage system reboots when necessary.

    @@@ Puppet
    package { 'git_client':
      ensure          => installed,
      source          => '\\server\git_client.exe',
      install_options => ['/Passive', '/NoRestart'],
    }
    reboot { 'after':
      subscribe       => Package['git_client'],
    }


You can also install several packages before rebooting:

    @@@ Puppet
    package { 'Microsoft .NET Framework 4.5':
      ensure => installed,
      # ...
      notify => Reboot['after_run'],
    }
    package { 'Microsoft Windows SDK for Windows 7 (7.0)':
      ensure => installed,
      # ...
      notify => Reboot['after_run'],
    }
    reboot { 'after_run':
      apply  => finished, # reboots at the end of the Puppet run
    }

<!SLIDE>
# Other interesting resources

* puppetlabs/registry - manages registry keys

.break text

    @@@ Puppet
    registry_key { 'HKLM\System\CurrentControlSet\Services\Puppet':
      ensure => present,
    }
    
    registry_value { 'HKLM\System\CurrentControlSet\Services\Puppet\Description':
      ensure => present,
      type   => string,
      data   => "The Puppet Agent service periodically breaks/manages your configuration",
    }
    
    # OR:
    
    registry::value { 'puppetmaster':
      key  => 'HKLM\Software\Vendor\PuppetLabs',
      data => 'puppet.puppetlabs.com',
    }

* puppetlabs/powershell - powershell provider for the exec resource

.break text

    @@@ Puppet
    exec { 'rename-guest':
      command   => '$(Get-WMIObject Win32_UserAccount -Filter "Name=\\'guest\\'").Rename("new-guest")',
      unless    => 'if (Get-WmiObject Win32_UserAccount -Filter "Name=\\'guest\\'") { exit 1 }',
      provider  => powershell,
    }

<!SLIDE>
# Puppet Directories

Useful Puppet directories in Windows:

* Executable dir:     C:\Program Files\Puppet Labs\Puppet\bin
* Configuration dir:  C:\ProgramData\PuppetLabs\puppet\etc

<!SLIDE>
# Hands-on lab: Developing a simple module for Windows

* Create a module that manages a user and a file resource
* Use a source attribute to download the file from the "puppet master"

<!SLIDE>
# Hands-on lab: Using an advanced module for Windows

* Use the puppet/iis module to install IIS and configure some of its features
