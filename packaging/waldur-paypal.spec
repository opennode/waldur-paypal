Name: waldur-paypal
Summary: PayPal plugin for Waldur
Group: Development/Libraries
Version: 0.5.0
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor >= 0.146.2
Requires: python-paypal-rest-sdk >= 1.10.0, python-paypal-rest-sdk < 2.0

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
Waldur PayPal allows to make payments via PayPal.

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
* Tue Sep 5 2017 Victor Mireyev <victor@opennodecloud.com> - 0.5.0-1.el7
- Rename package to waldur-paypal
