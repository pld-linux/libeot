#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for parsing and converting Embedded OpenType files
Summary(pl.UTF-8):	Biblioteka do analizy i konwersji plików Embedded OpenType
Name:		libeot
# version fron AC_INIT()
Version:	0.01
# git snapshot date
Release:	0.20131006.1
License:	MPL v2.0
Group:		Libraries
Source0:	http://dev-www.libreoffice.org/src/%{name}.tar.bz2
# Source0-md5:	4c3fdbae53f3c155af94d6df0b6e12b6
URL:		https://github.com/umanwizard/libeot
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	git-core
BuildRequires:	libtool >= 2:2
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for parsing Embedded OpenType files (Microsoft embedded font
"standard"), and converting them to other formats.

%description -l pl.UTF-8
Biblioteka do analizy plików Embedded OpenTyoe ("standard" osadzonych
fontów Microsoftu) oraz konwersji ich do innych formatów.

%package devel
Summary:	Header files for libeot library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libeot
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libeot library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libeot.

%package static
Summary:	Static libeot library
Summary(pl.UTF-8):	Statyczna biblioteka libeot
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libeot library.

%description static -l pl.UTF-8
Statyczna biblioteka libeot.

%prep
%setup -q -n %{name}

%build
# restore deleted required files
unset GIT_DIR GIT_WORK_TREE
git checkout Makefile.am configure.ac
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# fix public header braindamage
%{__sed} -i -e 's,\.\./src/,,' $RPM_BUILD_ROOT%{_includedir}/libeot/libeot.h
cp -p src/{EOT,EOTError}.h $RPM_BUILD_ROOT%{_includedir}/libeot

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE PATENTS
%attr(755,root,root) %{_bindir}/eot2ttf
%attr(755,root,root) %{_libdir}/libeot.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeot.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeot.so
%{_libdir}/libeot.la
%{_includedir}/libeot

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeot.a
%endif
