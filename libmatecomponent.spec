# NOTE: this package is deprecated, meant for MATE <= 1.4 compatibility only
#
# Conditional build:
%bcond_with	static_libs	# static library
#
Summary:	Library for compound documents in MATE
Summary(pl.UTF-8):	Biblioteka do łączenia dokumentów w MATE
Summary(pt_BR.UTF-8):	Biblioteca para documentos compostos no MATE
Name:		libmatecomponent
Version:	1.4.0
Release:	1
License:	LGPL v2+ (libraries), GPL v2+ (programs)
Group:		Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	7ba05884fec91eb5c3bb2cf7300b0e16
Patch0:		%{name}-am.patch
Patch1:		%{name}-glib.patch
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	docbook-dtd412-xml
BuildRequires:	flex
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	mate-common
BuildRequires:	mate-corba-devel >= 1.1.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post):	/sbin/ldconfig
Requires:	glib2 >= 1:2.26.0
Requires:	libxml2 >= 1:2.6.31
Requires:	popt >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmatecomponent is a library that provides the necessary framework
for MATE applications to deal with compound documents, i.e. those with
a spreadsheet and graphic embedded in a word-processing document.

%description -l pl.UTF-8
libmatecomponent jest biblioteką dającą aplikacjom MATE szkielet
pozwalający im pracować ze złożonymi dokumentami. Dzięki niemu można
np. osadzić arkusz kalkulacyjny i grafikę w dokumencie edytora tekstu.

%description -l pt_BR.UTF-8
libmatecomponent é uma biblioteca que fornece uma camada necessária
para os aplicativos do MATE funcionarem com documentos compostos, por
exemplo planilhas de cálculo e gráficos juntos num documento texto.

%package devel
Summary:	Include files for the libmatecomponent document model
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmatecomponent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
Requires:	mate-corba-devel >= 1.1.0
# for header only
Requires:	popt-devel >= 1.5

%description devel
This package provides the necessary include files to allow you to
develop programs using the libmatecomponent document model.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
korzystających z modelu dokumentów libmatecomponent.

%package static
Summary:	Static libmatecomponent libraries
Summary(pl.UTF-8):	Biblioteki statyczne libmatecomponent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmatecomponent libraries.

%description static -l pl.UTF-8
Biblioteki statyczne libmatecomponent.

%package apidocs
Summary:	libmatecomponent API documentation
Summary(pl.UTF-8):	Dokumentacja API libmatecomponent
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libmatecomponent API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libmatecomponent.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e 's|/lib|/%{_lib}|g' utils/matecomponent-slay.in

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static matecorba or matecomponent modules and *.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{matecomponent/monikers,matecorba-2.0}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{matecomponent/monikers,matecorba-2.0}/*.a
%endif
# Seems to be only test tool during build
%{__rm} $RPM_BUILD_ROOT%{_bindir}/matecomponent-activation-run-query

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_sbindir}/matecomponent-activation-sysconf --add-directory=%{_libdir}/matecomponent/servers

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README changes.txt
%attr(755,root,root) %{_bindir}/matecomponent-activation-client
%attr(755,root,root) %{_bindir}/matecomponent-slay
%attr(755,root,root) %{_bindir}/matecomponent-echo-client-2
%attr(755,root,root) %{_sbindir}/matecomponent-activation-sysconf
%attr(755,root,root) %{_libdir}/libmatecomponent-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatecomponent-2.so.0
%attr(755,root,root) %{_libdir}/libmatecomponent-activation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatecomponent-activation.so.4
%attr(755,root,root) %{_libdir}/matecomponent-activation-server
%dir %{_libdir}/matecomponent-2.0
%dir %{_libdir}/matecomponent-2.0/samples
%attr(755,root,root) %{_libdir}/matecomponent-2.0/samples/matecomponent-echo-2
%dir %{_libdir}/matecomponent
%dir %{_libdir}/matecomponent/monikers
%attr(755,root,root) %{_libdir}/matecomponent/monikers/libmoniker_std_2.so
%dir %{_libdir}/matecomponent/servers
%{_libdir}/matecomponent/servers/MateComponent_CosNaming_NamingContext.server
%{_libdir}/matecomponent/servers/MateComponent_Moniker_std.server
%{_libdir}/matecomponent/servers/MateComponent_Sample_Echo.server
%attr(755,root,root) %{_libdir}/matecorba-2.0/MateComponent_module.so
%dir %{_sysconfdir}/matecomponent-activation
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/matecomponent-activation/matecomponent-activation-config.xml
%{_datadir}/idl/matecomponent-2.0
%{_datadir}/idl/matecomponent-activation-2.0
%{_mandir}/man1/matecomponent-activation-server.1*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) %{_libdir}/libmatecomponent-2.so
%attr(755,root,root) %{_libdir}/libmatecomponent-activation.so
%{_includedir}/libmatecomponent-2.0
%{_includedir}/matecomponent-activation-2.0
%{_pkgconfigdir}/matecomponent-activation-2.0.pc
%{_pkgconfigdir}/libmatecomponent-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmatecomponent-2.a
%{_libdir}/libmatecomponent-activation.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%{_gtkdocdir}/matecomponent-activation
