Name:           flatpak
Version:        0.6.5
Release:        1%{?dist}
Summary:        Application deployment framework for desktop apps

Group:          Development/Tools
License:        LGPLv2+
URL:            https://flatpak.github.io/
Source0:        https://github.com/flatpak/flatpak/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(libelf) >= 0.8.12
BuildRequires:  pkgconfig(libgsystem) >= 2015.1
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(ostree-1) >= 2016.5
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(xau)
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  intltool
BuildRequires:  libattr-devel
BuildRequires:  libcap-devel
BuildRequires:  libdwarf-devel
BuildRequires:  systemd
BuildRequires:  /usr/bin/xsltproc

# Crashes with older kernels (the bug being introduced in 4.0.2), without the
# upstream fixes in this version.
Requires:       kernel >= 4.0.4-202

# Needed for the document portal.
Requires:       /usr/bin/fusermount

# Remove in F27.
Provides:       xdg-app = %{version}-%{release}
Obsoletes:      xdg-app <= 0.5.2-2

%description
flatpak is a system for building, distributing and running sandboxed desktop
applications on Linux. See https://wiki.gnome.org/Projects/SandboxedApps for
more information.

%package builder
Summary:        Build helper for %{name}
Group:          Development/Tools
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       /usr/bin/bzr
Requires:       /usr/bin/git
Requires:       /usr/bin/patch
Requires:       /usr/bin/strip
Requires:       /usr/bin/tar
Requires:       /usr/bin/unzip
# Remove in F27.
Provides:       xdg-app-builder = %{version}-%{release}
Obsoletes:      xdg-app-builder <= 0.5.2-2

%description builder
flatpak-builder is a tool that makes it easy to build applications and their
dependencies by automating the configure && make && make install steps.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# Remove in F27.
Provides:       xdg-app-devel%{?_isa} = %{version}-%{release}
Obsoletes:      xdg-app-devel <= 0.5.2-2

%description devel
This package contains the pkg-config file and development headers for %{name}.

%package libs
Summary:        Libraries for %{name}
Group:          Development/Libraries
License:        LGPLv2+
# Remove in F27.
Provides:       xdg-app-libs%{?_isa} = %{version}-%{release}
Obsoletes:      xdg-app-libs <= 0.5.2-2

%description libs
This package contains libflatpak.


%prep
%setup -q


%build
# User namespace support is sufficient.
%configure --with-dwarf-header=%{_includedir}/libdwarf --with-priv-mode=none
%make_build V=1


%install
%make_install
# The system repo is not installed by the flatpak build system.
install -d %{buildroot}%{_localstatedir}/lib/flatpak
rm -f %{buildroot}%{_libdir}/libflatpak.la


%post
# Create an (empty) system-wide repo.
flatpak remote-list --system

%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%license COPYING
%doc NEWS README.md
%{_bindir}/flatpak
%{_datadir}/bash-completion
%{_datadir}/dbus-1/interfaces/org.freedesktop.Flatpak.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.Documents.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.impl.portal.PermissionStore.xml
%{_datadir}/dbus-1/services/org.freedesktop.Flatpak.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.PermissionStore.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Documents.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
# Co-own directory.
%{_datadir}/gdm/env.d
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.Flatpak.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.Flatpak.rules
%{_libexecdir}/flatpak-bwrap
%{_libexecdir}/flatpak-dbus-proxy
%{_libexecdir}/flatpak-session-helper
%{_libexecdir}/flatpak-system-helper
%{_libexecdir}/xdg-document-portal
%{_libexecdir}/xdg-permission-store
%dir %{_localstatedir}/lib/flatpak
%{_mandir}/man1/%{name}*.1*
%exclude %{_mandir}/man1/flatpak-builder.1*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
%{_sysconfdir}/profile.d/flatpak.sh
%{_unitdir}/flatpak-system-helper.service
%{_userunitdir}/flatpak-session-helper.service
%{_userunitdir}/xdg-document-portal.service
%{_userunitdir}/xdg-permission-store.service

%files builder
%{_bindir}/flatpak-builder
%{_mandir}/man1/flatpak-builder.1*

%files devel
%{_datadir}/gir-1.0/Flatpak-1.0.gir
%{_datadir}/gtk-doc/
%{_includedir}/%{name}/
%{_libdir}/libflatpak.so
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%license COPYING
%{_libdir}/girepository-1.0/Flatpak-1.0.typelib
%{_libdir}/libflatpak.so.*


%changelog
* Fri Jun 10 2016 David King <amigadave@amigadave.com> - 0.6.5-1
- Update to 0.6.5

* Wed Jun 01 2016 David King <amigadave@amigadave.com> - 0.6.4-1
- Update to 0.6.4

* Tue May 31 2016 David King <amigadave@amigadave.com> - 0.6.3-1
- Update to 0.6.3
- Move bwrap to main package

* Tue May 24 2016 David King <amigadave@amigadave.com> - 0.6.2-1
- Rename from xdg-app to flatpak (#1337434)
