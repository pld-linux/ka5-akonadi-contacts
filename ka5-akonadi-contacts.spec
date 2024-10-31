#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	%{version}
# packages version, not cmake config version (which is 5.24.5)
%define		ka_ver		%{version}
%define		kf_ver		5.105.0
%define		qt_ver		5.15.2
%define		kaname		akonadi-contacts
Summary:	Akonadi Contacts
Summary(pl.UTF-8):	Komponent kontaktów dla Akonadi
Name:		ka5-%{kaname}
Version:	23.08.5
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	e4b501e5a6fedcb972b3ff2c31e8577a
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	grantlee-qt5-devel >= 5.3
BuildRequires:	ka5-akonadi-devel >= %{ka_ver}
BuildRequires:	ka5-grantleetheme-devel >= %{ka_ver}
BuildRequires:	ka5-kmime-devel >= %{ka_ver}
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kcodecs-devel >= %{kf_ver}
BuildRequires:	kf5-kcompletion-devel >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kconfigwidgets-devel >= %{kf_ver}
BuildRequires:	kf5-kcontacts-devel >= %{kf_ver}
BuildRequires:	kf5-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf5-ki18n-devel >= %{kf_ver}
BuildRequires:	kf5-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf5-kio-devel >= %{kf_ver}
BuildRequires:	kf5-kservice-devel >= %{kf_ver}
BuildRequires:	kf5-ktextwidgets-devel >= %{kf_ver}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kxmlgui-devel >= %{kf_ver}
BuildRequires:	kf5-prison-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	grantlee-qt5 >= 5.3
Requires:	ka5-akonadi >= %{ka_ver}
Requires:	ka5-grantleetheme >= %{ka_ver}
Requires:	ka5-kmime >= %{ka_ver}
Requires:	kf5-kcodecs >= %{kf_ver}
Requires:	kf5-kcompletion >= %{kf_ver}
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kconfigwidgets >= %{kf_ver}
Requires:	kf5-kcontacts >= %{kf_ver}
Requires:	kf5-kcoreaddons >= %{kf_ver}
Requires:	kf5-ki18n >= %{kf_ver}
Requires:	kf5-kiconthemes >= %{kf_ver}
Requires:	kf5-kio >= %{kf_ver}
Requires:	kf5-prison >= %{kf_ver}
Requires:	kf5-ktextwidgets >= %{kf_ver}
Requires:	kf5-kwidgetsaddons >= %{kf_ver}
Requires:	kf5-kxmlgui >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Contacts is a library that effectively bridges the
type-agnostic API of the Akonadi client libraries and the
domain-specific KContacts library. It provides jobs, models and other
helpers to make working with contacts and addressbooks through Akonadi
easier.

%description -l pl.UTF-8
Akonadi Contacts to biblioteka efektywnie łącząca niezależne od typów
API bibliotek klienckich Akonadi oraz bibliotekę KContacts. Zapewnia
funkcje pomocnicze dla zadań, modeli itp., ułatwiające pracę z
kontaktami i książkami adresowymi poprzez Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qt_ver}
Requires:	ka5-akonadi-devel >= %{ka_ver}
Requires:	ka5-grantleetheme-devel >= %{ka_ver}
Requires:	kf5-kcontacts-devel >= %{kf_ver}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# akonadicontact5 and akonadicontact5-serializer domains
%find_lang %{kaname} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKPim5AkonadiContact.so.5
%attr(755,root,root) %{_libdir}/libKPim5AkonadiContact.so.*.*.*
%ghost %{_libdir}/libKPim5ContactEditor.so.5
%attr(755,root,root) %{_libdir}/libKPim5ContactEditor.so.*.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/akonadi_serializer_addressee.so
%attr(755,root,root) %{_libdir}/qt5/plugins/akonadi_serializer_contactgroup.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%{_datadir}/kf5/akonadi/contact
%{_datadir}/qlogging-categories5/akonadi-contacts.categories
%{_datadir}/qlogging-categories5/akonadi-contacts.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim5AkonadiContact.so
%{_libdir}/libKPim5ContactEditor.so
%{_includedir}/KPim5/AkonadiContact
%{_includedir}/KPim5/AkonadiContactEditor
%{_libdir}/cmake/KF5AkonadiContactEditor
%{_libdir}/cmake/KPim5AkonadiContact
%{_libdir}/cmake/KPim5ContactEditor
%{_libdir}/qt5/mkspecs/modules/qt_AkonadiContact.pri
%{_libdir}/qt5/mkspecs/modules/qt_ContactEditor.pri
