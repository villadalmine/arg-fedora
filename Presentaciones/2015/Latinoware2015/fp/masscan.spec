%global commit d4656ad8a32d694723da49e6f31d33e0c47e22c7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name:	masscan
Version:	1.0.3
Release:	10%{?dist}
Summary:	This is the fastest Internet port scanner
License:	BSD
URL:		https://github.com/robertdavidgraham/%{name}	
Source0:	https://github.com/robertdavidgraham/%{name}/archive/%{commit}/%{commit}.tar.gz
Patch0:		%{name}-1.0.3-secondary.patch

BuildRequires:	libpcap-devel

%description
It is a faster port scan that produces results similar to nmap,
the most famous port scanner. Internally, it operates more like
scanrand, unicornscan, and ZMap, using asynchronous transmission.

%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1 -b .secondary
sed -i 's/\r$//' VULNINFO.md

%build
make %{?_smp_mflags} CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_bindir}/
install -pm 0755 bin/masscan %{buildroot}%{_bindir}/%{name}

%files
%doc LICENSE VULNINFO.md README.md
%{_bindir}/masscan



%changelog
* Mon Jun 23 2014 Rino Rondan <villadalmine@fedoraproject.org> - 1.0.3-10
- Rebuilt for version 1.0.3 and fix Source0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Dan Horák <dan[at]danny.cz> - 1.0-8
- fix build on secondary arches

* Wed Jan 01 2014 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-7
- Change the description

* Mon Nov 04 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-6
- Change the version macro, and all relationship with it

* Thu Oct 31 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-5
- Change summary and description

* Thu Oct 31 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-4
- Add some variables to build

* Thu Oct 31 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-3
- Add the correct info on changelog
- Fix the problem with doc

* Thu Oct 31 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-2
- Add the correct tag for pre-release on Version and Release
- Add global variable for checkout

* Wed Sep 11 2013 Rino Rondan <villadalmine@fedoraproject.org> - 1.0-1
- Initial Package
