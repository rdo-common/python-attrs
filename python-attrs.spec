%global modname attrs

Name:           python-attrs
Version:        16.1.0
Release:        1%{?dist}
Summary:        Python attributes without boilerplate

License:        MIT
URL:            https://attrs.readthedocs.io/
BuildArch:      noarch
Source0:        https://github.com/hynek/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz


%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-devel python-setuptools
# Can't run tests on EPEL7 due to need for pytest >= 2.8
%else
BuildRequires:  python2-devel python2-setuptools
BuildRequires:  python2-pytest python2-hypothesis python-zope-interface
%endif

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if 0%{?rhel} && 0%{?rhel} <= 7
# can't run tests on EPEL7 because we don't yet have python3x-zope-interface
%else
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-hypothesis
BuildRequires:  python%{python3_pkgversion}-zope-interface
%endif

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%package -n python%{python3_pkgversion}-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

%description -n python%{python3_pkgversion}-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{modname}-%{version}

%build
%py2_build
%py3_build

%install
# Doesn't install anything to /usr/bin, so I don't think the order of
# installing python2 and python3 actually matters.
%py3_install
%py2_install

%check
%if 0%{?rhel} && 0%{?rhel} <= 7
# Can't run tests on EPEL7 due to need for pytest >= 2.8
%else
PYTHONPATH=%{buildroot}/%{python2_sitelib} py.test-2.7 -v
PYTHONPATH=%{buildroot}/%{python3_sitelib} py.test-3 -v
%endif

%files -n python2-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python2_sitelib}/*

%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/*

%changelog
* Sat Sep 10 2016 Eric Smith <brouhaha@fedoraproject.org> 16.1.0-1
- Updated to latest upstream.
- Removed patch, no longer necessary.
- Removed "with python3" conditionals.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-6
- Build for Python 3.4 in EPEL7.

* Thu Aug 18 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-5
- Updated based on Fedora package review (#1366878).
- Fix check section, though tests can not be run for EPEL7.
- Add patch to skip two tests with keyword collisions.

* Tue Aug 16 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-4
- Fix python2 BuildRequires.

* Mon Aug 15 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-3
- Updated based on Fedora package review (#1366878).

* Sun Aug 14 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-2
- Updated based on Fedora package review (#1366878).

* Sat Aug 13 2016 Eric Smith <brouhaha@fedoraproject.org> 16.0.0-1
- Initial version.
