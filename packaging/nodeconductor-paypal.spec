Name: nodeconductor-paypal
Summary: PayPal plugin for NodeConductor
Group: Development/Libraries
Version: 0.1.0
Release: 1.el7
License: Copyright 2015 OpenNode LLC. All rights reserved.
Url: http://nodeconductor.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor >= 0.79.0
Requires: python-paypal-rest-sdk >= 1.10.0

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
NodeConductor PayPal allows to make payments via PayPal.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Thu Nov 17 2015 Roman Kosenko <roman@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package

