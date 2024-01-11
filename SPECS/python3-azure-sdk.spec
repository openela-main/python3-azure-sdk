%global srcname azure-sdk
%global common_description This project provides a set of Python packages that make it easy to access\
Management (Virtual Machines, ...) or Runtime (ServiceBus using HTTP, Batch,\
Monitor) components of Microsoft Azure Complete feature list of this repo and\
where to find Python packages not in this repo can be found on our Azure SDK for\
Python documentation.

# EL is missing recommonmark library to build documentation
%global _with_doc 0%{?fedora}
%global pydoc_prefix %{?rhel:python}%{?fedora:python%{python3_pkgversion}}
%global sphinxbuild sphinx-build%{?fedora:-%{python3_version}}

%global azure_storage_min_version 1.0.0
%global msrest_min_version 0.4.26
%global msrestazure_min_version 0.5.0

# bundles
%global bundled_lib_dir    bundled
# python3-certifi bundle
%global certifi			certifi
%global certifi_version		2018.10.15
%global certifi_dir		%{bundled_lib_dir}/azure/%{certifi}
# python3-isodate bundle
%global isodate			isodate
%global isodate_version		0.5.4
%global isodate_dir		%{bundled_lib_dir}/azure/%{isodate}
# python3-msrest bundle
%global msrest			msrest
%global msrest_version		0.6.2
%global msrest_dir		%{bundled_lib_dir}/azure/%{msrest}
# python3-adal bundle
%global adal			adal
%global adal_version		1.2.0
%global adal_dir		%{bundled_lib_dir}/azure/%{adal}
# python3-SecretStorage bundle
%global secretstorage		SecretStorage
%global secretstorage_version	2.3.1
%global secretstorage_dir	%{bundled_lib_dir}/azure/%{secretstorage}
# python3-keyring bundle
%global keyring			keyring
%global keyring_version		13.2.1
%global keyring_dir		%{bundled_lib_dir}/azure/%{keyring}
# python3-msrestazure bundle
%global msrestazure		msrestazure
%global msrestazure_version	0.5.1
%global msrestazure_dir		%{bundled_lib_dir}/azure/%{msrestazure}

Name:           python3-%{srcname}
Version:        4.0.0
Release:        9%{?dist}
Summary:        Microsoft Azure SDK for Python

# All packages are licensed under the MIT license, except:
# - azure-servicebus
# - azure-servicemanagement-legacy
License:        MIT and ASL 2.0 and MPLv2.0 and BSD and Python
URL:            https://github.com/Azure/azure-sdk-for-python
Source0:        %{url}/archive/azure_%{version}/%{srcname}-%{version}.tar.gz
Source1:        %{certifi}-%{certifi_version}.tar.gz
Source2:        %{isodate}-%{isodate_version}.tar.gz
Source3:        %{msrest}-%{msrest_version}.tar.gz
Source4:        %{adal}-%{adal_version}.tar.gz
Source5:        %{secretstorage}-%{secretstorage_version}.tar.gz
Source6:        %{keyring}-%{keyring_version}.tar.gz
Source7:        %{msrestazure}-%{msrestazure_version}.tar.gz
# Install namespace package modules (disabled by default, may be required by
# modules depending on Azure SDK for development)
Patch0:         python-azure-sdk-4.0.0-nspkgs.patch
# bundles 
Patch1000:      certifi-2018.10.15-use-system-cert.patch
Patch1001:      python-msrest-0.6.1-setup.patch
Patch1002:      python-msrest-0.6.1-isodate.patch
Patch1003:      python-msrest-0.6.1-tests.patch
Patch1004:      python-adal-1.2.0-tests.patch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# bundles
# python3-certifi bundle
BuildRequires: ca-certificates
# python3-keyring bundle
BuildRequires: python3-setuptools_scm
%if 0%{?_with_doc}
BuildRequires:  %{pydoc_prefix}-recommonmark
BuildRequires:  %{pydoc_prefix}-sphinx
BuildRequires:  %{pydoc_prefix}-sphinx_rtd_theme
%endif
Requires: python%{python3_pkgversion}-pyOpenSSL
Requires: python%{python3_pkgversion}-requests
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
# bundles
# python3-certifi bundle
Provides: bundled(python3-%{certifi}) = %{certifi_version}
# python3-isodate bundle
Provides: bundled(python3-%{isodate}) = %{isodate_version}
# python3-msrest bundle
Provides: bundled(python3-%{msrest}) = %{msrest_version}
# python3-adal bundle
Provides: bundled(python3-%{adal}) = %{adal_version}
# python3-SecretStorage bundle
Provides: bundled(python3-%{secretstorage}) = %{secretstorage_version}
# python3-keyring bundle
Provides: bundled(python3-%{keyring}) = %{keyring_version}
# python3-msrestazure bundle
Provides: bundled(python3-%{msrestazure}) = %{msrestazure_version}
# python3-certifi bundle
Requires: ca-certificates
# python3-msrest bundle
Requires: python3-requests-oauthlib
# python3-adal bundle
Requires: python3-cryptography
Requires: python3-dateutil
Requires: python3-jwt
BuildArch:      noarch

%description
%{common_description}


%if 0%{?_with_doc}
%package doc
Summary:        Documentation for %{name}

%description doc
This package provides documentation for %{name}.
%endif


%prep
%setup -q -n %{srcname}-for-python-azure_%{version}%{?prerelease}
%patch0

# bundles
mkdir -p %{bundled_lib_dir}/azure

# python3-certifi bundle
tar -xzf %SOURCE1 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{certifi}-%{certifi_version} %{certifi_dir}
# Remove bundled egg-info
rm -rf %{certifi_dir}/*.egg-info
rm -rf %{certifi_dir}/certifi/*.pem
cp %{certifi_dir}/README.rst %{certifi}_README.rst
cp %{certifi_dir}/LICENSE %{certifi}_LICENSE
pushd %{certifi_dir}
%patch1000 -p1
popd

# python3-isodate bundle
tar -xzf %SOURCE2 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{isodate}-%{isodate_version} %{isodate_dir}
cp %{isodate_dir}/README.rst %{isodate}_README.rst

# python3-msrest
tar -xzf %SOURCE3 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{msrest}-for-python-%{msrest_version} %{msrest_dir}
cp %{msrest_dir}/README.rst %{msrest}_README.rst
cp %{msrest_dir}/LICENSE.md %{msrest}_LICENSE.md
pushd %{msrest_dir}
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
popd

# python3-adal
tar -xzf %SOURCE4 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/azure-activedirectory-library-for-python-%{adal_version} %{adal_dir}
cp %{adal_dir}/README.md %{adal}_README.md
cp %{adal_dir}/LICENSE %{adal}_LICENSE
pushd %{adal_dir}
%patch1004 -p1
popd

# python3-SecretStorage bundle
tar -xzf %SOURCE5 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{secretstorage}-%{secretstorage_version} %{secretstorage_dir}
cp %{secretstorage_dir}/README.rst %{secretstorage}_README.rst
cp %{secretstorage_dir}/LICENSE %{secretstorage}_LICENSE

# python3-keyring bundle
tar -xzf %SOURCE6 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{keyring}-%{keyring_version} %{keyring_dir}
cp %{keyring_dir}/README.rst %{keyring}_README.rst
cp %{keyring_dir}/LICENSE %{keyring}_LICENSE

# python3-msrestazure bundle
tar -xzf %SOURCE7 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/%{msrestazure}-for-python-%{msrestazure_version} %{msrestazure_dir}
cp %{msrestazure_dir}/README.rst %{msrestazure}_README.rst
cp %{msrestazure_dir}/LICENSE.md %{msrestazure}_LICENSE.md

# append bundled-directory to search path
sed -i "/^import keyring/iimport sys\nsys.path.insert(0, '%{_libdir}/fence-agents/bundled')" azure-batch/azure/batch/batch_auth.py

%build
%py3_build

%if 0%{?_with_doc}
%make_build -C doc/ html SPHINXBUILD=%{sphinxbuild}
rm doc/_build/html/.buildinfo
%endif

# bundles
# python3-certifi bundle
pushd %{certifi_dir}
%{__python3} setup.py build
popd

# python3-isodate bundle
pushd %{isodate_dir}
%{__python3} setup.py build
popd

# python3-msrest bundle
pushd %{msrest_dir}
%{__python3} setup.py build
popd

# python3-adal bundle
pushd %{adal_dir}
%{__python3} setup.py build
popd

# python3-SecretStorage bundle
pushd %{secretstorage_dir}
%{__python3} setup.py build
popd

# python3-keyring bundle
pushd %{keyring_dir}
%{__python3} setup.py build
popd

# python3-msrestazure bundle
pushd %{msrestazure_dir}
%{__python3} setup.py build
popd


%install
%py3_install

# bundles
# python3-certifi bundle
pushd %{certifi_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-isodate bundle
pushd %{isodate_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-msrest bundle
pushd %{msrest_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-adal bundle
pushd %{adal_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-SecretStorage bundle
pushd %{secretstorage_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-keyring bundle
pushd %{keyring_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd

# python3-msrestazure bundle
pushd %{msrestazure_dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/fence-agents/%{bundled_lib_dir}/azure
popd


%files
%doc CONTRIBUTING.md README.rst
%license LICENSE.txt
# bundled libraries
%doc %{certifi}_README.rst %{isodate}_README.rst %{msrest}_README.rst %{adal}_README.md %{secretstorage}_README.rst %{keyring}_README.rst %{msrestazure}_README.rst
%license %{certifi}_LICENSE %{msrest}_LICENSE.md %{adal}_LICENSE %{secretstorage}_LICENSE %{keyring}_LICENSE %{msrestazure}_LICENSE.md
%{python3_sitelib}/azure/
%{python3_sitelib}/azure_*.egg-info/
# bundled libraries
%dir /usr/lib/fence-agents
%dir /usr/lib/fence-agents/%{bundled_lib_dir}
/usr/lib/fence-agents/%{bundled_lib_dir}/azure
%exclude /usr/bin/keyring


%if 0%{?_with_doc}
%files doc
%doc doc/_build/html/
%license LICENSE.txt
%endif


%changelog
* Tue May 14 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.0-9
- Update to 4.0.0 + azure-mgmt-compute 5.0.0 (for skip_shutdown feature)
  Resolves: rhbz#1708129
- Add CI gating tests
  Resolves: rhbz#1682879

* Wed Jan 30 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.0-8
- Bundled libraries
  Resolves: rhbz#1630844

* Fri Jan 25 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.0-4
- Initial import
  Resolves: rhbz#1630844

* Thu Nov 22 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-3
- Build documentation with Python 3 on Fedora
- Fix Python 3-only file deployment
- Don't glob everything under the Python sitelib directory

* Mon Aug 06 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-2
- Delete all Python 3-only files from the python2 subpackage

* Mon Aug 06 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0
