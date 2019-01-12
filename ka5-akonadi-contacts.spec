%define		kdeappsver	18.12.1
%define		qtver		5.9.0
%define		kaname		akonadi-contacts
Summary:	Akonadi Contacts
Name:		ka5-%{kaname}
Version:	18.12.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/applications/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	b3f6da05ea1bcd1f7f42ddee986386e7
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	ka5-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka5-kcontacts-devel >= %{kdeappsver}
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= 5.51.0
BuildRequires:	kf5-kcodecs-devel >= 5.51.0
BuildRequires:	kf5-kcompletion-devel >= 5.51.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.51.0
BuildRequires:	kf5-ki18n-devel >= 5.51.0
BuildRequires:	kf5-kiconthemes-devel >= 5.51.0
BuildRequires:	kf5-kio-devel >= 5.51.0
BuildRequires:	kf5-ktextwidgets-devel >= 5.51.0
BuildRequires:	kf5-prison-devel >= 5.51.0
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
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/akonadi-contacts.categories
/etc/xdg/akonadi-contacts.renamecategories
#/etc/xdg/contact-editor.categories
%ghost %{_libdir}/libKF5AkonadiContact.so.5
%{_libdir}/libKF5AkonadiContact.so.5.*.*
%ghost %{_libdir}/libKF5ContactEditor.so.5
%{_libdir}/libKF5ContactEditor.so.5.*.*
%{_libdir}/qt5/plugins/akonadi/contacts
%{_libdir}/qt5/plugins/akonadi_serializer_addressee.so
%{_libdir}/qt5/plugins/akonadi_serializer_contactgroup.so
%{_libdir}/qt5/plugins/kcm_akonadicontact_actions.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%{_datadir}/kf5/akonadi/contact
%{_datadir}/kservices5/akonadi
%{_datadir}/kservices5/akonadicontact_actions.desktop
%{_datadir}/kservicetypes5/kaddressbookimprotocol.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Akonadi/Contact
%{_includedir}/KF5/ContactEditor
%{_includedir}/KF5/akonadi/contact
%{_includedir}/KF5/contacteditor
%{_libdir}/cmake/KF5AkonadiContact
%{_libdir}/cmake/KF5ContactEditor
%{_libdir}/libKF5AkonadiContact.so
%{_libdir}/libKF5ContactEditor.so
%{_libdir}/qt5/mkspecs/modules/qt_AkonadiContact.pri
%{_libdir}/qt5/mkspecs/modules/qt_ContactEditor.pri
