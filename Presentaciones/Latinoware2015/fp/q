1. Good Practices (4h)
  Puppet Concepts
    - What, not how
        * `Define the desired end state of the system instead of the steps required to get there`
        * `Declarative vs Imperative`
    - Abstraction
       Facter
        * `Extract information from systems with a consistent interface`
        * `Add information about your systems easily and integrate them with facter`
       RAL
        * `Common system concepts represented as resource types`
        * `Implementation of those concepts via resource providers`
       Idempotency
        * `Apply once or multiple times - same resulting state`
    - Resources
        * `Resources represent units of configuration`
        * `Anything from files, system packages to firewall rules and database tables can be managed as resources`
        * `Common resources and syntax`
    - Functions
        * `Provide data manipulation capabilities before the code is compiled`
        * `Custom and specialized functionality on the Puppet master`
    - Templates
        * `Parametrize configuration files`
        * `Insert logic and variables`
  Modules and Classes
    - Classes & namespaces
        * `Classes are collections of resources`
        * `Modules are directories that contain classes within a namespace`
        * `Subclasses are contained in modules - syntax and filenames`
    - Module layout & autodiscovery
        * `Standard directories for manifests, files and templates`
        * `Module locations enabling autodiscovery`
    - Creating modules
        * `Puppet module tool`
        * `Simple module structure`
        * `Module examples`
  Advanced Classes
    - Ordering
        * `Resource execution order is non-deterministic`
        * `Order can be defined explicitly with meta-attributes`
    - Data types
        * `Puppet variables`
        * `Strings, Arrays and Hashes`
        * `Other data types: References, Regex`
    - Parametrized classes and Hiera autolookup
        * `Class parameters as interfaces`
        * `Inheritance pattern`
        * `Separation of data and code`
        * `Automatic parameter lookup in Hiera`
    - Defined types
        * `Repeatable pieces of configuration`
        * `Abstract away your own configuration units`

2. Developing Modules (5.5h)
  Good practices in Module Development
    - Package/File/Service
    - Style
    - Parameters & Hiera good practices
  Developing automation modules
    - Desired module properties
       Sufficiently generic
       Composable
       Parameterized
       Documented
       Clear scope
       Reasonable defaults
       Idempotent
  Design Patterns
    - Revisiting Package/File/Service
    - Roles & Profiles
  Using community modules
    - Using the Forge
    - Forge module rating
    - Real-life usage of community modules
  Hands-on: Developing a module to automate some linux components
    - Module from scratch
    - Adapting a Forge module
3. Puppet & Windows (4h)
  Puppet scope with Windows
    - Resource details
       Generic resources
       System-specific resources
    - Puppet limitations in Windows
  Hands-on: Developing a basic automation module for Windows
    - User & file management
  Hands-on: Developing and advanced automation module for Windows
    - IIS
    - Chocolatey package management
4. Development Framework (2h)
  Development environment for Puppet
  Using an IDE for Module development
5. Test driven development applied to Puppet Modules (5h)
  Tools
    - Geppetto IDE
    - puppet-lint
    - rspec-puppet
    - Beaker
    - serverspec
  Continuous Integration
    - Git hooks
    - Jenkins & Vagrant
  Hands-on: Developing Modules + Tests + Deployment
6. Puppet Administration (9.5h)
  Puppet Master Installation
    - Monolithic package installation
    - Manual package installation
    - Common configuration options
  PuppetDB
    - Uses
    - Common configuration options
  Multimaster configuration alternatives
    - Reasons for multimaster setup
    - Load balancing
    - Environment separation
  Hands-on: Implementing a Multimaster environment
  Version Control
    - Keeping code in sync
    - Access control
  Hands-on: Modules Deployment and Rollback in a Multimaster environment
