#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for parsing and converting Embedded OpenType files
Summary(pl.UTF-8):	Biblioteka do analizy i konwersji plików Embedded OpenType
Name:		libeot
Version:	0.01
Release:	1
License:	MPL v2.0
Group:		Libraries
Source0:	http://dev-www.libreoffice.org/src/%{name}-%{version}.tar.bz2
# Source0-md5:	aa24f5dd2a2992f4a116aa72af817548
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
%setup -q

%build
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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libeot.la

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
%{_includedir}/libeot
%{_pkgconfigdir}/libeot.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeot.a
%endif
