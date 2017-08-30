Name: nodeconductor-paypal
Summary: PayPal plugin for NodeConductor
Group: Development/Libraries
Version: 0.5.0
Release: 1.el7
License: MIT
Url: http://nodeconductor.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor >= 0.102.0
Requires: python-paypal-rest-sdk >= 1.10.0, python-paypal-rest-sdk < 2.0
Requires: python-xhtml2pdf >= 0.0.6
Requires: python-html5lib < 1:0.99999999

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
* Fri Sep 16 2016 Jenkins <jenkins@opennodecloud.com> - 0.5.0-1.el7
- New upstream release

* Sun Jun 26 2016 Jenkins <jenkins@opennodecloud.com> - 0.4.0-1.el7
- New upstream release

* Thu Apr 28 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.5-1.el7
- New upstream release

* Mon Apr 4 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.4-1.el7
- New upstream release

* Tue Jan 19 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.3-1.el7
- New upstream release

* Tue Jan 19 2016 Jenkins <jenkins@opennodecloud.com> - v0.3.2-1.el7
- New upstream release

* Tue Dec 8 2015 Jenkins <jenkins@opennodecloud.com> - 0.3.1-1.el7
- New upstream release

* Tue Dec 8 2015 Jenkins <jenkins@opennodecloud.com> - 0.3.0-1.el7
- New upstream release

* Wed Nov 18 2015 Jenkins <jenkins@opennodecloud.com> - 0.2.2-1.el7
- New upstream release

* Wed Nov 18 2015 Jenkins <jenkins@opennodecloud.com> - 0.2.1-1.el7
- New upstream release

* Wed Nov 18 2015 Jenkins <jenkins@opennodecloud.com> - 0.2.0-1.el7
- New upstream release

* Tue Nov 17 2015 Roman Kosenko <roman@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package
