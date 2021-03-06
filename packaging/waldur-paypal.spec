Name: waldur-paypal
Summary: PayPal plugin for Waldur
Group: Development/Libraries
Version: 0.9.0
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: waldur-core >= 0.151.0
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
* Tue Jun 26 2018 Jenkins <jenkins@opennodecloud.com> - 0.9.0-1.el7
- New upstream release

* Fri Jun 1 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.2-1.el7
- New upstream release

* Tue May 22 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.1-1.el7
- New upstream release

* Thu May 10 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.0-1.el7
- New upstream release

* Sat Feb 3 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.0-1.el7
- New upstream release

* Fri Dec 1 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.3-1.el7
- New upstream release

* Wed Oct 4 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.2-1.el7
- New upstream release

* Tue Sep 19 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.1-1.el7
- New upstream release

* Fri Sep 8 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.0-1.el7
- New upstream release

* Tue Sep 5 2017 Victor Mireyev <victor@opennodecloud.com> - 0.5.0-1.el7
- Rename package to waldur-paypal
