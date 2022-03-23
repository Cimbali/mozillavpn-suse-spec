%define _srcdir .
Version: 2.7.1
Release: 1
Source0: mozillavpn_2.7.1.orig.tar.gz
Patch0: support_lib_path.patch

Name:      mozillavpn
Summary:   Mozilla VPN
License:   MPL-2.0
URL:       https://vpn.mozilla.org
Packager:  Cimbali
Requires:  libQt5Core5
Requires:  libQt5Charts5 >= 5.15
Requires:  libqt5-qtcharts-imports >= 5.15
Requires:  libQt5NetworkAuth5 >= 5.15
Requires:  libQt5QuickControls2-5 >= 5.15
Requires:  libQt5Svg5 >= 5.15
Requires:  libpolkit-gobject-1-0 >= 0.105
Requires:  wireguard-tools >= 1.0.20200513

BuildRequires: golang >= 1.13
BuildRequires: cargo
BuildRequires: python3 >= 3.6
BuildRequires: python3-PyYAML
BuildRequires: polkit-devel
BuildRequires: libqt5-qtbase-devel >= 5.15
BuildRequires: libqt5-qtbase-common-devel >= 5.15
BuildRequires: libQt5Charts5-devel >= 5.15
BuildRequires: libqt5-qtnetworkauth-devel >= 5.15
BuildRequires: libqt5-qtwebsockets-devel >= 5.15
BuildRequires: libqt5-qtdeclarative-devel >= 5.15
BuildRequires: libqt5-qtsvg-devel >= 5.15
BuildRequires: libqt5-qttools-devel >= 5.15
BuildRequires: systemd-rpm-macros

%description
A fast, secure and easy to use VPN. Built by the makers of Firefox.
Read more on https://vpn.mozilla.org

The Mozilla VPN team does not currently provide official support for Linux distributions other than Ubuntu.

%prep
%setup
%patch0 -p1
%undefine _lto_cflags

%build
%{_srcdir}/scripts/utils/import_languages.py
qmake-qt5 %{_srcdir}/mozillavpn.pro QT+=svg CONFIG+=webextension CONFIG-=debug LIBPATH=%{_libdir} ETCPATH=%{_sysconfdir} USRPATH=%{_prefix}
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE.md
%{_sysconfdir}/chromium/native-messaging-hosts/mozillavpn.json
%{_sysconfdir}/opt/chrome/native-messaging-hosts/mozillavpn.json
%{_sysconfdir}/xdg/autostart/MozillaVPN-startup.desktop
%{_unitdir}/mozillavpn.service
%{_bindir}/mozillavpn
%{_libdir}/mozillavpn/mozillavpnnp
%{_libdir}/mozilla/native-messaging-hosts/mozillavpn.json
%{_datadir}/applications/MozillaVPN.desktop
%{_datadir}/dbus-1/system-services/org.mozilla.vpn.dbus.service
%{_datadir}/dbus-1/system.d/org.mozilla.vpn.conf
%{_datadir}/icons/hicolor/128x128/apps/mozillavpn.png
%{_datadir}/icons/hicolor/16x16/apps/mozillavpn.png
%{_datadir}/icons/hicolor/32x32/apps/mozillavpn.png
%{_datadir}/icons/hicolor/48x48/apps/mozillavpn.png
%{_datadir}/icons/hicolor/64x64/apps/mozillavpn.png
%{_datadir}/polkit-1/actions/org.mozilla.vpn.policy
