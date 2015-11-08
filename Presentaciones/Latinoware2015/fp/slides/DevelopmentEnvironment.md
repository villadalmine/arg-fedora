<!SLIDE center subsection>
# Development Environments

<!SLIDE>
# Setting up a local development environment

* Desktop virtualization software (VirtualBox/VMWare Player)
* VM with your target OS/distribution
* Puppet Agent package for that OS
* Puppet code repository (git, SVN, etc...)
* Text editor (Geppetto, vim, sublime, etc...)
* Syntax highlighting/code autocomplete
* Vagrant (optional)

<!SLIDE>
# Setting up Vagrant

* https://www.vagrantup.com/downloads.html
* Select a box: `vagrant box add puppetlabs/centos-6.6-64-puppet`

.break text

    @@@ Shell
    $ vagrant box add puppetlabs/centos-6.6-64-puppet 
    ==> box: Loading metadata for box 'puppetlabs/centos-6.6-64-puppet'
        box: URL: https://atlas.hashicorp.com/puppetlabs/centos-6.6-64-puppet
    This box can work with multiple providers! The providers that it
    can work with are listed below. Please review the list and choose
    the provider you will be working with.
    
    1) virtualbox
    2) vmware_desktop
    3) vmware_fusion
    
    Enter your choice: 1
    ==> box: Adding box 'puppetlabs/centos-6.6-64-puppet' (v1.0.2) for provider: virtualbox
        box: Downloading: https://atlas.hashicorp.com/puppetlabs/boxes/centos-6.6-64-puppet/versions/1.0.2/providers/virtualbox.box
        box: Progress: 98% (Rate: 893k/s, Estimated time remaining: 0:02:49)

<!SLIDE>
# Vagrantfile

* Create a Vagrantfile

.break text

    @@@ Shell
    # ~/puppet/workshop/Vagrantfile
    Vagrant::Config.run do |config|
      config.vm.box       = "puppetlabs/centos-6.6-64-puppet"
      config.vm.box_url   = "https://atlas.hashicorp.com/puppetlabs/boxes/centos-6.6-64-puppet"
      config.vm.host_name = "puppetworkshop.edrans.vm"
      config.vm.network :hostonly, "10.16.40.10"
      config.vm.forward_port 80, 8084
      config.vm.provision :shell, :path => "centos_6_x.sh"
    
      # Puppet Shared Folder
      config.vm.share_folder "puppet_mount", "/puppet", "~/puppet/workshop/puppet"
    end

<!SLIDE>
# Bootstrap file

* Source: https://github.com/hashicorp/puppet-bootstrap

.break text

    @@@ Shell
    #!/usr/bin/env bash
    # This bootstraps Puppet on CentOS 6.x
    # It has been tested on CentOS 6.4 64bit
    
    set -e
    
    REPO_URL="http://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm"
    
    if [ "$EUID" -ne "0" ]; then
      echo "This script must be run as root." >&2
      exit 1
    fi
    
    if which puppet > /dev/null 2>&1; then
      echo "Puppet is already installed."
      rm -rf /etc/puppetlabs/code/modules
      ln -s /puppet /etc/puppetlabs/code/modules
      exit 0
    fi
    
    # Install puppet labs repo
    echo "Configuring PuppetLabs repo..."
    repo_path=$(mktemp)
    wget --output-document="${repo_path}" "${REPO_URL}" 2>/dev/null
    rpm -i "${repo_path}" >/dev/null
    
    # Install Puppet...
    echo "Installing puppet"
    yum install -y puppet > /dev/null
    rm -rf /etc/puppetlabs/code/modules
    ln -s /puppet /etc/puppetlabs/code/modules
    
    echo "Puppet installed!"

<!SLIDE>
# Working with our code

Use any text editor in your host system (you're working on the host's filesystem!)

    @@@ Shell
    [vagrant@puppetworkshop ~]$ ll /etc/puppetlabs/code/
    total 8
    drwxr-xr-x 3 root root 4096 Jul 27 11:43 environments
    -rw-r--r-- 1 root root  371 Jul 21 20:58 hiera.yaml
    lrwxrwxrwx 1 root root    7 Sep 10 01:45 modules -> /puppet
    
    [vagrant@puppetworkshop ~]$ mount | grep puppet
    puppet_mount on /puppet type vboxsf (uid=500,gid=500,rw)

/puppet maps to our code directory

<!SLIDE>
# Hands-on lab: sharing our module directory in VirtualBox

* Configure a shared folder in VirtualBox
* Use it to edit Puppet code from your host computer

<!SLIDE>
# Geppetto
Geppetto is an Eclipse-based IDE focused on Puppet development. Some of its features are:

* Module boilerplate generation (similar to `puppet module generate`)
* Import modules from folders or directly from the Forge
* Syntax checks and autocomplete
* Integrates with version control systems (using Eclipse plugins such as Eclipse EGit)
* Integrates with Puppet Enterprise and PuppetDB to display Puppet run data

<!SLIDE>
# Hands-on lab: first look at Geppetto

* Install Geppetto
* Import a module from the Forge and inspect it with the Project Explorer
