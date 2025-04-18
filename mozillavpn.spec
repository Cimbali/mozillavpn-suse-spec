%define _srcdir .
Version: 2.27.0
Release: 1
Source0: mozillavpn_2.27.0.orig.tar.gz
%{!?_version: %define _version %(cat %{_srcdir}/version.txt)}

Name:      mozillavpn
Summary:   Mozilla VPN
License:   MPL-2.0
URL:       https://vpn.mozilla.org
Packager:  Cimbali
Requires:  libQt6Core6 >= 6.0
Requires:  libQt6NetworkAuth6 >= 6.0
Requires:  libQt6QuickControls2-6 >= 6.0
Requires:  libQt6Svg6 >= 6.0
Requires:  libQt6Core5Compat6 >= 6.0
Requires:  qt6-qt5compat-imports >= 6.0
Requires:  wireguard-tools

BuildRequires: cargo >= 1.75
BuildRequires: golang >= 1.18
BuildRequires: libcap-devel
BuildRequires: libsecret-devel
BuildRequires: libopenssl-devel
BuildRequires: python3 >= 3.6
BuildRequires: python3-PyYAML
BuildRequires: python3-lxml
BuildRequires: qt6-base-devel >= 6.0
BuildRequires: qt6-base-common-devel >= 6.0
BuildRequires: qt6-base-private-devel >= 6.0
BuildRequires: qt6-networkauth-devel >= 6.0
BuildRequires: qt6-declarative-devel >= 6.0
BuildRequires: qt6-svg-devel >= 6.0
BuildRequires: qt6-tools-devel >= 6.0
BuildRequires: qt6-websockets-devel >= 6.0
BuildRequires: qt6-qt5compat-devel >= 6.0
BuildRequires: qt6-tools-linguist >= 6.0
BuildRequires: qt6-sql-mysql >= 6.0
BuildRequires: qt6-sql-unixODBC => 6.0
BuildRequires: qt6-sql-postgresql => 6.0
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

%description
A fast, secure and easy to use VPN. Built by the makers of Firefox.
Read more on https://vpn.mozilla.org

The Mozilla VPN team does not currently provide official support for Linux distributions other than Ubuntu.
This package is also not currently validated by an OpenSUSE security review.

%prep
%autosetup -p1
%undefine _lto_cflags

%build
%cmake -DWEBEXT_INSTALL_LIBDIR:PATH=%{_libdir} -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} -DCMAKE_INSTALL_DATADIR:PATH=%{_datadir} -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%pre
%service_add_pre mozillavpn.service socksproxy.service

%post
%service_add_post mozillavpn.service socksproxy.service

%preun
%service_del_preun mozillavpn.service socksproxy.service

%postun
%service_del_postun mozillavpn.service socksproxy.service

%files
%license LICENSE.md
%config %{_sysconfdir}/chromium/native-messaging-hosts/mozillavpn.json
%config %{_sysconfdir}/opt/chrome/native-messaging-hosts/mozillavpn.json
%config %{_sysconfdir}/xdg/autostart/org.mozilla.vpn-startup.desktop
%{_unitdir}/mozillavpn.service
%{_unitdir}/socksproxy.service
%{_bindir}/mozillavpn
%{_bindir}/socksproxy
%{_libdir}/mozillavpn
%{_libdir}/mozilla/native-messaging-hosts/mozillavpn.json
%{_datadir}/applications/org.mozilla.vpn.desktop
%{_datadir}/dbus-1/system-services/org.mozilla.vpn.dbus.service
%{_datadir}/dbus-1/system.d/org.mozilla.vpn.conf
%{_datadir}/icons/hicolor/128x128/apps/org.mozilla.vpn.png
%{_datadir}/icons/hicolor/16x16/apps/org.mozilla.vpn.png
%{_datadir}/icons/hicolor/32x32/apps/org.mozilla.vpn.png
%{_datadir}/icons/hicolor/48x48/apps/org.mozilla.vpn.png
%{_datadir}/icons/hicolor/64x64/apps/org.mozilla.vpn.png
%dir %{_sysconfdir}/chromium
%dir %{_sysconfdir}/chromium/native-messaging-hosts
%dir %{_sysconfdir}/opt/chrome
%dir %{_sysconfdir}/opt/chrome/native-messaging-hosts
%dir %{_libdir}/mozilla
%dir %{_libdir}/mozilla/native-messaging-hosts
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/128x128
%dir %{_datadir}/icons/hicolor/128x128/apps
%dir %{_datadir}/icons/hicolor/16x16
%dir %{_datadir}/icons/hicolor/16x16/apps
%dir %{_datadir}/icons/hicolor/32x32
%dir %{_datadir}/icons/hicolor/32x32/apps
%dir %{_datadir}/icons/hicolor/48x48
%dir %{_datadir}/icons/hicolor/48x48/apps
%dir %{_datadir}/icons/hicolor/64x64
%dir %{_datadir}/icons/hicolor/64x64/apps
