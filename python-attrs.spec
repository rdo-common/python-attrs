%global modname attrs

# can't yet build python3 package for EPEL7
# Python 3.5 is available in EPEL7, but as of 2016-08-14, packaging guidelines
# aren't up to date, and example spec at
#   https://fedoraproject.org/wiki/User:Bkabrda/EPEL7_Python3#Specfiles.2C_Macros.2C_Packaging_Process
# isn't actually working for me.

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-attrs
Version:        16.0.0
Release:        5%{?dist}
Summary:        Python attributes without boilerplate

License:        MIT
URL:            https://attrs.readthedocs.io/
BuildArch:      noarch
Source0:        https://github.com/hynek/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz

# Patch two skip two tests with keyword collisions, fixed upstream in git,
# so patch won't be necessary in 16.1.0 and later
# https://github.com/hynek/attrs/issues/65
# https://github.com/hynek/attrs/commit/d10e5c41d614f8ca7b1b7a7c7a98f9dbe2d2b6fc
Patch1:         %{modname}-16.0.0-skiptests.patch


%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-devel python-setuptools
%else
BuildRequires:  python2-devel python2-setuptools
BuildRequires:  python2-pytest python-zope-interface
%endif
BuildRequires:  python2-hypothesis

%if %{with python3}
BuildRequires:  python3-devel python3-setuptools python3-hypothesis
BuildRequires:  python3-pytest python3-zope-interface
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

%if %{with python3}
%package -n python%{python3_pkgversion}-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname}
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.
%endif

%prep
%setup -q -n %{modname}-%{version}
%patch1 -p1 -b .skiptests

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
# Doesn't install anything to /usr/bin, so I don't think the order of
# installing python2 and python3 actually matters.
%if %{with python3}
%py3_install
%endif
%py2_install

%check
%if 0%{?rhel} && 0%{?rhel} <= 7
# Can't run tests on EPEL7 due to need for pytest >= 2.8
%else
PYTHONPATH=%{buildroot}/%{python2_sitelib} py.test-2.7 -v
%if %{with python3}
PYTHONPATH=%{buildroot}/%{python3_sitelib} py.test-3 -v
%endif
%endif

%files -n python2-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{modname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/*
%endif

%changelog
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
