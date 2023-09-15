#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.1
%define		qtver		5.15.2
%define		kaname		akonadi-contacts
Summary:	Akonadi Contacts
Name:		ka5-%{kaname}
Version:	23.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	4df84de1b858577020549a9ca410daa7
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	gpgme-qt5-devel
BuildRequires:	ka5-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka5-grantleetheme-devel >= %{kdeappsver}
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	ka5-libkleo-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= 5.51.0
BuildRequires:	kf5-kcmutils-devel >= 5.87.0
BuildRequires:	kf5-kcodecs-devel >= 5.51.0
BuildRequires:	kf5-kcompletion-devel >= 5.51.0
BuildRequires:	kf5-kcontacts-devel >= 5.65.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.51.0
BuildRequires:	kf5-ki18n-devel >= 5.51.0
BuildRequires:	kf5-kiconthemes-devel >= 5.51.0
BuildRequires:	kf5-kio-devel >= 5.51.0
BuildRequires:	kf5-kitemmodels-devel >= 5.87.0
BuildRequires:	kf5-ktextwidgets-devel >= 5.51.0
BuildRequires:	kf5-prison-devel >= 5.51.0
BuildRequires:	ninja
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Contacts is a library that effectively bridges the
type-agnostic API of the Akonadi client libraries and the
domain-specific KContacts library. It provides jobs, models and other
helpers to make working with contacts and addressbooks through Akonadi
easier.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt5/plugins/akonadi_serializer_addressee.so
%attr(755,root,root) %{_libdir}/qt5/plugins/akonadi_serializer_contactgroup.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%{_datadir}/kf5/akonadi/contact
%{_datadir}/qlogging-categories5/akonadi-contacts.categories
%{_datadir}/qlogging-categories5/akonadi-contacts.renamecategories
%ghost %{_libdir}/libKPim5AkonadiContact.so.5
%attr(755,root,root) %{_libdir}/libKPim5AkonadiContact.so.*.*.*
%ghost %{_libdir}/libKPim5ContactEditor.so.5
%attr(755,root,root) %{_libdir}/libKPim5ContactEditor.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/qt5/mkspecs/modules/qt_AkonadiContact.pri
%{_libdir}/qt5/mkspecs/modules/qt_ContactEditor.pri
%{_includedir}/KPim5/AkonadiContact
%{_includedir}/KPim5/AkonadiContactEditor
%{_libdir}/cmake/KF5AkonadiContactEditor
%{_libdir}/cmake/KPim5AkonadiContact
%{_libdir}/cmake/KPim5ContactEditor
%{_libdir}/libKPim5AkonadiContact.so
%{_libdir}/libKPim5ContactEditor.so
