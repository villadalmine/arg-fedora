1. Good Practices (4h) - real time: 7-8h
  * Puppet Concepts - real time: 3h
    - Abstraction
       * Facter
       * RAL
       * Idempotency
    - What, not how
    - Resources
    - Functions
    - Templates
  * Modules and Classes - real time 2h
    - Classes & namespaces
    - Module layout & autodiscovery
    - Creating modules
  * Advanced Classes - real time 3-4h
    - Ordering
    - Hiera autolookup
    - Defined types
    - Data types
2. Developing Modules (5.5h)
  * Good practices in Module Development
    - Package/File/Service
    - Style
    - Parameters & Hiera good practices
  * Developing automation modules
    - Desired module properties
       * Sufficiently generic
       * Composable
       * Parameterized
       * Documented
       * Clear scope
       * Reasonable defaults
       * Idempotent
  * Design Patterns
    - Revisiting Package/File/Service
    - Roles & Profiles
  * Using community modules
    - Using the Forge
    - Forge module rating
    - Real-life usage of community modules
  * Hands-on: Developing a module to automate some linux components - REVISAR nginx
    - Module from scratch
    - Adapting a Forge module
3. Puppet & Windows (4h)
  * Puppet scope with Windows
    - Resource details
       * Generic resources
       * System-specific resources
    - Puppet limitations in Windows
  * Hands-on: Developing a basic automation module for Windows
    - User & file management
  * Hands-on: Developing and advanced automation module for Windows
    - IIS
    - Chocolatey package management
4. Development Framework (2h)
  * Development environment for Puppet
  * Using an IDE for Module development
5. Test driven development applied to Puppet Modules (5h)
  * Tools
    - Geppetto IDE
    - puppet-lint
    - rspec-puppet
    - Beaker
    - serverspec
  * Continuous Integration
    - Git hooks
    - Jenkins & Vagrant
  * Hands-on: Developing Modules + Tests + Deployment
6. Puppet Administration (9.5h)
  * Puppet Master Installation
    - Monolithic package installation
    - Manual package installation
    - Common configuration options
  * PuppetDB
    - Uses
    - Common configuration options
  * Multimaster configuration alternatives
    - Reasons for multimaster setup
    - Load balancing
    - Environment separation
  * Hands-on: Implementing a Multimaster environment
  * Version Control
    - Keeping code in sync
    - Access control
  * Hands-on: Modules Deployment and Rollback in a Multimaster environment
