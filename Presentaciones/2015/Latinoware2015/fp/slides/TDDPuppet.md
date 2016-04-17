<!SLIDE center subsection>
# Test driven development in Puppet

<!SLIDE>
# Tools

* puppet-lint
* rspec-puppet
* serverspec

<!SLIDE>
# puppet-lint
Lint tool for Puppet. Checks style and optionally fixes it:

    @@@ Shell
    # To install:
    gem install puppet-lint

    $ puppet-lint snmp/manifests/*
    snmp/manifests/config.pp - WARNING: indentation of => is not properly aligned on line 10
    snmp/manifests/config.pp - WARNING: indentation of => is not properly aligned on line 11
    snmp/manifests/config.pp - WARNING: indentation of => is not properly aligned on line 12
    snmp/manifests/config.pp - WARNING: indentation of => is not properly aligned on line 13
    snmp/manifests/params.pp - WARNING: quoted boolean value found on line 8
    snmp/manifests/service.pp - WARNING: string containing only a variable on line 22
    snmp/manifests/service.pp - WARNING: variable not enclosed in {} on line 22
    snmp/manifests/service.pp - WARNING: quoted boolean value found on line 3
    snmp/manifests/service.pp - WARNING: unquoted file mode on line 14
    
    $ puppet-lint --fix snmp/manifests/*
    snmp/manifests/config.pp - FIXED: indentation of => is not properly aligned on line 10
    snmp/manifests/config.pp - FIXED: indentation of => is not properly aligned on line 11
    snmp/manifests/config.pp - FIXED: indentation of => is not properly aligned on line 12
    snmp/manifests/config.pp - FIXED: indentation of => is not properly aligned on line 13
    snmp/manifests/params.pp - FIXED: quoted boolean value found on line 8
    snmp/manifests/service.pp - FIXED: string containing only a variable on line 22
    snmp/manifests/service.pp - FIXED: variable not enclosed in {} on line 22
    snmp/manifests/service.pp - FIXED: quoted boolean value found on line 3
    snmp/manifests/service.pp - FIXED: unquoted file mode on line 14


<!SLIDE>
# rspec-puppet
Behavior driven development framework. Describe what your module is supposed to do!

Leverages Ruby's rspec library

    @@@ Ruby
    require 'spec_helper'
    
    describe '<name of the thing being tested>' do
      # Your tests go in here
    end

Using our ifcfg defined type, a first attempt might look like this:

    @@@ Ruby
    require 'spec_helper'
    
    describe 'ifcfg' do
      let(:title) { 'eth0' }
    
      it do
        should contain_file('/home/workshop/pablo/ifcfg-eth0').with({
          'ensure' => 'file',
          'owner'  => 'root',
          'group'  => 'root',
          'mode'   => '0644',
        })
      end
    end

<!SLIDE>
# Deeper into rspec-puppet

    @@@ Ruby
    require 'spec_helper'
    
    describe 'ifcfg' do
      let(:title) { 'eth0' }
    
      it do
        should contain_file('/home/workshop/pablo/ifcfg-eth0').with({
          'ensure' => 'file',
          'owner'  => 'root',
          'group'  => 'root',
          'mode'   => '0644',
        })
      end
    
      context 'with bootproto => dhcp' do
        let(:params) { {:bootproto => 'dhcp'} }
    
        it do
          should contain_file('/home/workshop/pablo/ifcfg-eth0') \
            .with_content(/^BOOTPROTO="dhcp"$/)
        end
      end
    
      context 'with bootproto => static' do
        let(:params) { {:bootproto => 'static'} }
    
        it do
          should contain_file('/home/workshop/pablo/ifcfg-eth0') \
            .with_content(/^BOOTPROTO="static"$/)
        end
      end
    

<!SLIDE>
# Serverspec
RSpec tests for your servers:

    @@@ Ruby
    require 'spec_helper'
    
    describe package('httpd'), :if => os[:family] == 'redhat' do
      it { should be_installed }
    end
    
    describe package('apache2'), :if => os[:family] == 'ubuntu' do
      it { should be_installed }
    end
    
    describe service('httpd'), :if => os[:family] == 'redhat' do
      it { should be_enabled }
      it { should be_running }
    end
    
    describe service('apache2'), :if => os[:family] == 'ubuntu' do
      it { should be_enabled }
      it { should be_running }
    end
    
    describe service('org.apache.httpd'), :if => os[:family] == 'darwin' do
      it { should be_enabled }
      it { should be_running }
    end
    
    describe port(80) do
      it { should be_listening }
    end


<!SLIDE>
# Serverspec vs rspec-puppet

Serverspec tests the outcome of a manifest, while rspec-puppet tests the defined behavior beforehand.

* rspec-puppet would run in a CI server (or locally while developing) before deploying the code to productive environments
* serverspec would run (on a development) server after a Puppet run to ensure the desired state was reached

<!SLIDE>
# Continuous Integration

<!SLIDE>
# Hands-on: Developing Modules + Tests + Deployment
