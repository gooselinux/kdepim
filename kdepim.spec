%ifnarch s390 s390x
%global _with_pilot_link 1
%endif

Name: kdepim
Summary: PIM (Personal Information Manager) applications
Epoch: 6
Version: 4.3.4
Release: 5%{?dist}

License: GPLv2
Group: Applications/Productivity
URL: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# fix libqgpgme-link
Patch0:  kdepim-4.1.80-libqgpgme-link-fix.patch

# http://bugzilla.redhat.com/show_bug.cgi?id=496988
Patch1:  kdepim-4.3.1-kmail-saveAttachments.patch

# upstream patches (4.3 branch):
Patch100: kdepim-4.3.5.patch

Provides: kdepim4 = %{version}-%{release}

Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


BuildRequires: akonadi-devel
BuildRequires: bison flex
BuildRequires: boost-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: desktop-file-utils
BuildRequires: gpgme-devel
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: kdelibs-experimental-devel
BuildRequires: libassuan-devel
BuildRequires: libical-devel
BuildRequires: libXpm-devel libXScrnSaver-devel
BuildRequires: libxslt-devel
%if 0%{?_with_pilot_link:1}
BuildRequires: pilot-link-devel >= 0.12
%endif
BuildRequires: python-devel
BuildRequires: soprano-devel
BuildRequires: qca2-devel
BuildRequires: zlib-devel

%description
%{summary}, including:
* akregator: feed aggregator
* kmail: email client
* knode: newsreader
* knotes: sticky notes for the desktop
* kontact: integrated PIM management
* korganizer: journal, appointments, events, todos
%{?_with_pilot_link:* kpilot: HotSync® software for Palm OS® devices}


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Provides: kdepim4-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: kdelibs4-devel

%description devel
%{summary}.
Install %{name}-devel if you want to write or compile %{name} plugins.


%package libs
Summary: %{name} runtime libraries
Group:   System Environment/Libraries
Requires: kdelibs4%{?_isa} >= %{version}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
%{summary}.


%prep
%setup -q

%patch0 -p1 -b .libqgpgme-link-fix
%patch1 -p0 -b .kmail-saveAttachments

# 4.3 upstream patches
%patch100 -p1 -b .kde435


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# make symlinks relative
mkdir -p %{buildroot}%{_docdir}/HTML/en/common
pushd %{buildroot}%{_docdir}/HTML/en
for i in *; do
   if [ -d $i -a -L $i/common ]; then
      rm -f $i/common
      ln -nfs ../common $i
   fi
done
popd


%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README README.Kolab COPYING
%{_kde4_bindir}/*
%if 0%{?_with_pilot_link:1}
%{_kde4_libdir}/libkpilot_*.so
%endif
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/strigi/*.so
%{_kde4_datadir}/applications/kde4/*.desktop
%{_kde4_appsdir}/akregator/
%{_kde4_appsdir}/kaddressbook/
%{_kde4_appsdir}/kalarm/
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/kdepimwidgets/
%{_kde4_appsdir}/kjots/
%{_kde4_appsdir}/kleopatra/
%{_kde4_appsdir}/kmail/
%{_kde4_appsdir}/kmailcvt/
%{_kde4_appsdir}/knode/
%{_kde4_appsdir}/knotes/
%{_kde4_appsdir}/konsolekalendar/
%{_kde4_appsdir}/kontact/
%{_kde4_appsdir}/kontactsummary/
%{_kde4_appsdir}/korgac/
%{_kde4_appsdir}/korganizer/
%if 0%{?_with_pilot_link:1}
%{_kde4_appsdir}/kpilot/
%endif
%{_kde4_appsdir}/ktimetracker/
%{_kde4_appsdir}/kwatchgnupg/
%{_kde4_appsdir}/libkdepim/
%{_kde4_appsdir}/libkleopatra/
%{_datadir}/dbus-1/interfaces/*.xml
%{_kde4_datadir}/autostart/*
%{_kde4_datadir}/config/*rc
%{_kde4_datadir}/config.kcfg/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_docdir}/HTML/en/*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*
%{_kde4_libdir}/kde4/plugins/designer/*.so

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/*
%{_kde4_libdir}/lib*.so
%if 0%{?_with_pilot_link:1}
%exclude %{_kde4_libdir}/libkpilot_*.so
%endif


%changelog
* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 6:4.3.4-5
- rebuilt against qt 4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 6:4.3.4-4
- backport 4.3.5 fixes

* Mon Jan 04 2010 Than Ngo <than@redhat.com> - 6:4.3.4-3
- drop BR on gnokii-devel

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Fri Nov 27 2009 Than Ngo <than@redhat.com> - 4.3.3-3
- fix build issue on s390

* Fri Nov 13 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rhel cleanup, fix conditional for RHEL

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Fri Oct 30 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.2-2
- unbreak ktimetracker (#532055, kde#209570, patch from upstream)

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Thu Sep 24 2009 Than Ngo <than@redhat.com> - 4.3.1-6
- rhel cleanup

* Wed Sep 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-5
- respin ldap crasher patch (kdebug:206024, rhbz#524870)

* Tue Sep 15 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.1-4
- fix crash when autocompleting LDAP address (kdebug:206024)

* Mon Sep 14 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.1-3
- fix KMail issues losing messages when renaming folder with disconnected IMAP

* Tue Sep 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- rebuild (gnokii)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Tue Aug 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-4
- kmail: upstream fix for custom font settings (#kdebug#178402)

* Tue Aug 11 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0-3
- fix kmail default save dir regression (#496988)

* Sat Aug 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-2
- -libs: move designer plugins here
- %%check: desktop-file-validate
- don't own %%{_kde4_appsdir}/kconf_update/

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3 

* Sat Jul 11 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Tue Jul 07 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.95-2
- Requires: kdepim-runtime (< F-12)

* Mon Jun 29 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.2.90-1
- KDE 4.3 Beta 2

* Fri May 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.85-2
- fix meeting-organizer icon conflict with oxygen-icons
- -libs: (re)add dep on kdelibs4

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Mon Apr 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-4
- drop extraneous BR's, including libmal-devel (not currently used)

* Mon Apr 06 2009 Than Ngo <than@redhat.com> - 4.2.2-3
- apply upstream patch to fix crash in korganizer

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 09 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.1-3
- upstream korganizer-view patch

* Wed Mar 04 2009 Than Ngo <than@redhat.com> - 4.2.1-2
- upstream patch, speed up folder syncing

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Than Ngo <than@redhat.com> - 4.2.0-2
- upstream patch, fix data corruption problems in KPilot

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Thu Jan 15 2009 Rex Dieter <rdieter@fedoraproject.org> 4.1.96-3
- move libkpilot_*.so -devel -> main pkg

* Thu Jan 15 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.96-2
- reenable BR pilot-link-devel, add missing BR libmal-devel (for KPilot)

* Wed Jan 07 2009 Than Ngo <than@redhat.com> 4.1.96-1
- 4.2rc1

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Fri Nov 28 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-3
- kdepim-4.1.80-libqgpgme-link-fix.patch
  fix libqgpgme linking errors

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast
- kdepim-4.1.2-kabcdistlistupdater.patch upstreamed

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Sun Oct 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.2-4
- add missing BR soprano-devel

* Tue Oct 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.2-3
- add converter for old kabc distribution lists (#464622)

* Tue Oct 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.2-2
- rebuild for new gnokii

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Thu Jul 24 2008 Than Ngo <than@redhat.com> 4.1.0-2
- respun

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Sun Jul 13 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-3
- fix conflict with oxygen-icon-theme

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.83-3
- -devel: move designer plugin here

* Tue Jun 24 2008 Than Ngo <than@redhat.com> 4.0.83-2
- respun

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Wed May 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-2
- put unversioned libkpilot_conduit_base.so in -libs instead of -devel (#448395)

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Mon May 19 2008 Rex Dieter <rdieter@fedoraproject.org> 6:4.0.72-1
- first stab at kdepim4

* Fri Apr 11 2008 Rex Dieter <rdieter@fedoraproject.org> 6:3.5.9-9
- omit multilib upgrade hacks (see also #441222)

* Tue Apr 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.9-8
- add Requires: kdebase3-pim-ioslaves (#441541)

* Tue Apr 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.9-7
- fix gnokii detection (thanks to Dirk Müller)

* Wed Feb 27 2008 Rex Dieter <rdieter@fedoraproject.org> 6:3.5.9-6
- "Enterprise headers" makes impossible to select text in
  first paragraph of body (kde#151150)

* Mon Feb 18 2008 Than Ngo <than@redhat.com> 6:3.5.9-5
- backport upstream patch to fix kmail crash on startup

* Fri Feb 15 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.9-3
- backport upstream fix for kde#127696 from enterprise branch

* Fri Feb 15 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.9-2
- update opensync03 patch

* Thu Feb 14 2008 Rex Dieter <rdieter@fedoraproject.org> 6:3.5.9-1
- kde-3.5.9

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.8-17.20080109.ent
- rebuild for GCC 4.3

* Mon Jan 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.8-16.20080109.ent
- add patch from kitchensync-OpenSync0.30API branch to build KitchenSync again (F9+)

* Wed Jan 09 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-15.20080109.ent
- 20080109 snapshot (sync with F-7/8 branches)

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-14.20071204.ent
- omit kpalmdoc.png icons too (f9+)

* Fri Dec 28 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.5.8-13.20071204.ent
- rebuild for new libopensync

* Wed Dec 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-12.20071204.ent
- omit crystalsvg icons (f9+)
- kdepim_3.5.6.enterprise.0.20071204.744693

* Thu Nov 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-10.20071129.ent
- kdepim-enterprise branch 20071129 snapshot, r742984

* Thu Nov 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-9.20071127.ent
- omit "compacting mbox..." patch for now (doesn't apply)

* Wed Nov 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-8.20071127.ent
- include/reference kdepim-enterprise-svn_checkout.sh

* Mon Nov 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.8-7.20071127.ent
- kdepim-enterprise branch 20071127 snapshot, r742277 (rh#401391, kde#152553)

* Thu Nov 22 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:3.5.8-6.20071013.ent
- rebuild for new pilot-link

* Tue Nov 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-5.20071013.ent
- compacting mbox shows empty folder (kde#146967, rh#352391)

* Wed Oct 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-4.20071013.ent
- -libs: Obsoletes: %%name ... to help out multilib upgrades

* Sun Oct 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-3.20071013.ent
- -libs: %%post/%%postun /sbin/ldconfig
- -libs conditional (f8+)

* Sun Oct 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-2.20071013.ent
- -libs subpkg (to be more multilib friendly)

* Sat Oct 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-1.20071013.ent
- kdepim-enterprise branch 20071013 snapshot, r724979

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-10.20070926.ent
- xdg-open patch

* Wed Sep 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-9.20070926.ent
- kdepim-enterprise branch 20070926 snapshot (r717374)

* Thu Sep 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-8.20070920.714749.ent
- kdepim-enterprise branch 20070920 snapshot (r714749)

* Mon Sep 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-8
- drop OnlyShowIn=KDE munging
- update %%description
- tidy up

* Mon Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-7
- templates for forwarding do not work with inline mails (kde#140549)

* Mon Aug 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-6
- License: GPLv2
- Provides: kdepim3(-devel)
- (Build)Requires: kdelibs3(-devel)

* Tue Jun 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-3
- +Requires(hint): spambayes (#238650)

* Wed Jun 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.7-2
- +BR: libopensync-devel (#244939)

* Wed Jun 13 2007 Than Ngo <than@redhat.com> - 6:3.5.7-1.fc7
- bump release version

* Wed Jun 06 2007 Than Ngo <than@redhat.com> -  6:3.5.7-0.1.fc7
- 3.5.7

* Thu May 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.5.6-7
- +BR: gpgme-devel gnokii-devel libmal-devel
- +Requires: pinentry-gui
- drop unused/deprecated patches
- revert to kinder/gentler scriptlets
- sanitize .la files a bit

* Mon Mar 26 2007 Than Ngo <than@redhat.com> - 3.5.6-4.fc7
- upstream patches

* Mon Mar 05 2007 Than Ngo <than@redhat.com> 3.5.6-3.fc7
- cleanup specfile

* Thu Feb 08 2007 Than Ngo <than@redhat.com> - 6:3.5.6-2.fc7
- apply upstream patch to fix a debugging leftover which logs
  passwords clear text

* Tue Feb 06 2007 Than Ngo <than@redhat.com> - 6:3.5.6-1.fc7
- 3.5.6

* Wed Nov 29 2006 Karsten Hopp <karsten@redhat.com> 3.5.5-1.fc7
- rebuild with new pilot-link libs
- fix automake version check

* Fri Nov 10 2006 Than Ngo <than@redhat.com> 6:3.5.5-0.2.fc6
- apply upstream patch to fix bz#215081 (kde#135513)

* Thu Oct 26 2006 Than Ngo <than@redhat.com> 6:3.5.5-0.1
- 3.5.5

* Thu Sep 14 2006 Than Ngo <than@redhat.com> 6:3.5.4-5
- apply upstream patches
   fix 98545, kmail does not remember pop3 passwords
   add default values for font sizes
   fix #133792, do not double-count days during weekly-summarized report
   remove a duplicated holiday
   fix #134200, always initialize mLineHeight and mFirstColumnWidth
   fix #126975, Refuse to LOGIN when hasCapability("LOGINDISABLED")
   fix #134702, Kontact crashes when moving mail between imap folders
   fix #126060, Kmail crash when IMAP mailbox modified externally

* Tue Sep 12 2006 Than Ngo <than@redhat.com> 6:3.5.4-4
- apply upstream patches
   fix #133846, fix for the tooltip crash

* Mon Sep 04 2006 Than Ngo <than@redhat.com> 6:3.5.4-3
- apply upstream patches
   fix kde#116607, crash in slotCheckQueuedFolders() on application exit

* Tue Aug 15 2006 Than Ngo <than@redhat.com> 6:3.5.4-2
- apply patch to fix crash when right clicking in an encapsulated email message, kde#131067

* Thu Aug 10 2006 Than Ngo <than@redhat.com> 6:3.5.4-1
- apply upstream patches,
   - Kmail crashes on startup, kde#132008
   - Cannot send to addresses containing an ampersand (&), kde#117882

* Mon Jul 24 2006 Than Ngo <than@redhat.com> 6:3.5.4-0.pre1
- prerelease of 3.5.4 (from the first-cut tag)

* Thu Jul 20 2006 Than Ngo <than@redhat.com> 6:3.5.3-8
- apply upstream pacthes,
  fix crash on logout when only a message pane is shown kde#192416

* Mon Jul 17 2006 Petr Rockai <prockai@redhat.com> 6:3.5.3-7
- fix compilation with new g++ (see patch kdepim-3.5.3-gcc-4.1.1-8)

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 6:3.5.3-6
- rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.3-5.1
- rebuild

* Sat Jul 08 2006 Than Ngo <than@redhat.com> 6:3.5.3-5
- fix #136533, crypto/certificate manager support

* Thu Jul 06 2006 Than Ngo <than@redhat.com> 6:3.5.3-4
- apply upstream patches,
   fix bugs: 110487, 118112, 119112, 121384, 127210, 130303

* Tue Jun 27 2006 Than Ngo <than@redhat.com> 6:3.5.3-3
- fix #196741, BR: libXpm-devel libXScrnSaver-devel
- apply upstream patches

* Mon Jun 19 2006 Than Ngo <than@redhat.com> 6:3.5.3-2
- BR: cyrus-sasl-devel, #195500

* Fri Jun 02 2006 Than Ngo <than@redhat.com> 6:3.5.3-1
- update to 3.5.3

* Wed May 03 2006 Than Ngo <than@redhat.com> 6:3.5.2-2
- fix #190491, korganizer crashes whenever New Event selected
- fix crash from proko2
- possibly fix crash while selecting mail in mail header view
- fix #122571, kmail doesn't remember "fallback character encoding" setting
- fix #126571, kmail crashes when pressing "Send again..." in drafts folder
- fix syntax error in /usr/bin/kmail_clamav.sh

* Wed Mar 29 2006 Than Ngo <than@redhat.com> 6:3.5.2-1
- update to 3.5.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6:3.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Than Ngo <than@redhat.com> 6:3.5.1-1
- update to 3.5.1
- get rid of kdepim-3.5.0-kmail-113730.patch, which included in new upstream

* Mon Dec 12 2005 Than Ngo <than@redhat.com> 6:3.5.0-1
- apply patch to fix crash when applying pipe through filters

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Than Ngo <than@redhat.com> 6:3.5.0-0.1.rc2
- 3.5 rc2

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 6:3.4.92-3
- apply patch to fix gcc4 build problem

* Wed Oct 26 2005 Than Ngo <than@redhat.com> 6:3.4.92-2
- apply patch to fix undefined symbol in indexlib

* Mon Oct 24 2005 Than Ngo <than@redhat.com> 6:3.4.92-1
- update to 3.5 beta 2

* Thu Sep 29 2005 Than Ngo <than@redhat.com> 6:3.4.91-1
- update to KDE 3.5 beta1

* Wed Sep 21 2005 Than Ngo <than@redhat.com> 6:3.4.2-4
- fix uic build problem

* Tue Aug 30 2005 Than Ngo <than@redhat.com> 6:3.4.2-3
- rebuilt

* Mon Aug 15 2005 Than Ngo <than@redhat.com> 6:3.4.2-2
- apply patch to fix kpilot crash

* Tue Aug 02 2005 Than Ngo <than@redhat.com> 6:3.4.2-1
- update 3.4.2
- apply patch to fix kmail bug, kde#109003

* Mon Jul 04 2005 Than Ngo <than@redhat.com> 6:3.4.1-2
- fix uninitialized variable warning #162311, #162312

* Mon Jun 27 2005 Than Ngo <than@redhat.com> 6:3.4.1-1
- add kdepim-kpilot-fix.diff
- update to 3.4.1
- remove kdepim-3.4.0-long.patch, it's included in new upstream

* Wed Mar 23 2005 Than Ngo <than@redhat.com> 6:3.4.0-4
- add lockdev support patch in kandy from Peter Rockai #84143
- add missing kandy icons #141165

* Mon Mar 21 2005 Than Ngo <than@redhat.com> 6:3.4.0-3
- cleanup build dependencies #151673

* Fri Mar 18 2005 Than Ngo <than@redhat.com> 6:3.4.0-2
- fix broken dependencies on kdepim-devel #151508

* Thu Mar 17 2005 Than Ngo <than@redhat.com> 6:3.4.0-1
- 3.4.0 release

* Sun Mar 13 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.4
- rebuilt against pilot-link-0.12

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.3
- rebuilt against gcc-4.0.0-0.31

* Tue Mar 01 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.2
- fix casting issue

* Mon Feb 28 2005 Than Ngo <than@redhat.com> 6:3.4.0-0.rc1.1
- KDE 3.4.0 rc1

* Wed Feb 16 2005 Than Ngo <than@redhat.com> 6:3.3.92-0.1
- KDE-3.4 Beta2

* Mon Feb 14 2005 Than Ngo <than@redhat.com> 6:3.3.2-0.3
- apply Steve patch to fix buffer problem

* Sat Dec 04 2004 Than Ngo <than@redhat.com> 3.3.2-0.2
- add CVS patch to fix kmail crash when deleting mails in a folder, #141457

* Fri Dec 03 2004 Than Ngo <than@redhat.com> 3.3.2-0.1
- update to 3.3.2
- get rid of the kdepim-3.3.1-cvs.patch, kdepim-3.3.0-holiday.patch,
  both are included in 3.3.2

* Tue Nov 16 2004 Than Ngo <than@redhat.com> 6:3.3.1-3
- add several fixes from CVS

* Sat Oct 16 2004 Than Ngo <than@redhat.com> 6:3.3.1-2
- rebuilt for rhel

* Wed Oct 13 2004 Than Ngo <than@redhat.com> 6:3.3.1-1
- update to KDE 3.3.1

* Mon Oct 04 2004 Than Ngo <than@redhat.com> 6:3.3.0-2
- fix korganizer crash on startup #134458

* Fri Aug 20 2004 Than Ngo <than@redhat.com> 3.3.0-1
- update to 3.3.0 release

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 3.3.0-0.1.rc2
- update to 3.3.0 rc2

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 3.3.0-0.1.rc1
- update to 3.3.0 rc1

* Wed Aug 04 2004 Than Ngo <than@redhat.com> 6:3.2.92-1
- update to KDE 3.3 Beta 2

* Sat Jul 03 2004 Than Ngo <than@redhat.com> 6:3.2.91-1
- update to KDE 3.3 Beta 1

* Sun Jun 20 2004 Than Ngo <than@redhat.com> 6:3.2.3-1
- update to 3.2.3

* Thu May 06 2004 Than Ngo <than@redhat.com> 6:3.2.2-2
- cleanup KDE/GNOME menu

* Wed Apr 14 2004 Than Ngo <than@redhat.com> 6:3.2.2-1
- update to 3.2.2

* Mon Mar 22 2004 Than Ngo <than@redhat.com> 6:3.2.1-4
- fix conflict problem by update, #118709

* Fri Mar 19 2004 Karsten Hopp <karsten@redhat.de> 3.2.1-3
- add Obsoletes: kmail

* Sun Mar 14 2004 Karsten Hopp <karsten@redhat.de> 3.2.1-2
- add Provide: kmail

* Sun Mar 07 2004 Than Ngo <than@redhat.com> 6:3.2.1-1
- 3.2.1 release

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 01 2004 Than Ngo <than@redhat.com> 3.2.0-1.5
- add Buildrequires on libart_lgpl-devel #115183

* Tue Feb 24 2004 Than Ngo <than@redhat.com> 6:3.2.0-1.4
- some critical bugs in kmail, #116080

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 6:3.2.0-0.3
- 3.2.0 release
- built with qt 3.3.0
- add patch file from Stable branch, fix some critical bugs in kmail

* Wed Jan 21 2004 Than Ngo <than@redhat.com> 6:3.1.95-0.1
- KDE 3.2 RC1

* Thu Dec 11 2003 Than Ngo <than@redhat.com> 6:3.1.94-0.2
- fixed file list

* Mon Dec 01 2003 Than Ngo <than@redhat.com> 6:3.1.94-0.1
- KDE 3.2 Beta2

* Thu Nov 27 2003 Than Ngo <than@redhat.com> 6:3.1.93-0.2
- get rid of rpath

* Thu Nov 13 2003 Than Ngo <than@redhat.com> 6:3.1.93-0.1
- KDE 3.2 Beta1
- cleanup

* Tue Sep 30 2003 Than Ngo <than@redhat.com> 6:3.1.4-1
- 3.1.4

* Wed Aug 13 2003 Than Ngo <than@redhat.com> 6:3.1.3-3
- fix build problem with gcc 3.3

* Mon Aug 11 2003 Than Ngo <than@redhat.com> 6:3.1.3-2
- rebuilt

* Sat Aug 09 2003 Than Ngo <than@redhat.com> 6:3.1.3-1
- 3.1.3

* Wed Jun 25 2003 Than Ngo <than@redhat.com> 3.1.2-5
- rebuilt

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 6:3.1.2-4.1
- added epoch to versioned requires where needed
- built for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Than Ngo <than@redhat.com> 3.1.2-3
- dependencies issue

* Wed May 14 2003 Than Ngo <than@redhat.com> 3.1.2-1
- 3.1.2

* Wed Apr 23 2003 Than Ngo <than@redhat.com> 3.1.1-2
- enable libtool

* Thu Mar 20 2003 Than Ngo <than@redhat.com> 3.1.1-1
- 3.1.1

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Fri Feb 21 2003 Than Ngo <than@redhat.com> 3.1-4
- get rid of gcc path from dependency_libs

* Tue Feb 11 2003 Than Ngo <than@redhat.com> 3.1-3
- add missing build dependency, #84027

* Sat Feb  1 2003 Than Ngo <than@redhat.com> 3.1-2
- fix segfault #83194

* Tue Jan 28 2003 Than Ngo <than@redhat.com> 3.1-1
- 3.1 release
- cleanup specfile

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 6:3.1-0.3
- rebuild

* Tue Jan 14 2003 Thomas Woerner <twoerner@redhat.com> 3.1-0.2
- rc6
- removed size_t check
- exclude ia64

* Fri Nov 29 2002 Than Ngo <than@redhat.com> 3.1-0.1
- get rid of sub packages

* Mon Nov 25 2002 Than Ngo <than@redhat.com> 3.1-0.0
- update to 3.1 rc4
- remove a patch file, which is now in new upstream

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 3.0.5-1
- update to 3.0.5

* Wed Nov  6 2002 Than Ngo <than@redhat.com> 3.0.4-2
- fix some build problems

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 3.0.4-1
- 3.0.4

* Sun Oct  6 2002 Than Ngo <than@redhat.com> 3.0.3-4
- Fixed holiday plugin (bug #64750, #63438)
- Added more buildrequires/equires (bug #56282,#73996)

* Mon Sep  2 2002 Than Ngo <than@redhat.com> 3.0.3-3
- Added missing icons

* Thu Aug 22 2002 Than Ngo <than@redhat.com> 3.0.3-2
- rebuild against new pilot-link

* Mon Aug 12 2002 Than Ngo <than@redhat.com> 3.0.3-1
- 3.0.3
- Fixed a bug in clock applet

* Tue Aug  6 2002 Than Ngo <than@redhat.com> 3.0.2-4
- build against pilot-link-0.11.2
- desktop files issue

* Tue Jul 23 2002 Than Ngo <than@redhat.com> 3.0.2-3
- Added fix to build against qt 3.0.5
- build using gcc-3.2-0.1

* Sat Jul 20 2002 Than Ngo <than@redhat.com> 3.0.2-2
- fix desktop files issue
- rebuild against new pilot-link

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 3.0.1-1
- 3.0.1
- fixed bug #67303

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-3
- Rename libraries

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-2
- Fix #61901

* Fri Mar 29 2002 Than Ngo <than@redhat.com> 3.0.0-1
- final

* Tue Jan 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020122.1
- Update
- Fix build on ia64

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.2-0.cvs20010726.1
- Update, fixes korganizer (#50006)

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to get rid of abbrowser (moved to kdebase)

* Thu Feb 22 2001 Than Ngo <than@redhat.com>
- add missing ldconfig in %post anf %postun again
- clean up specfile

* Wed Feb 21 2001 Than Ngo <than@redhat.com>
- 2.1-respin
- fix dangling symlink
- remove excludearch ia64, some hacks to build on ia64

* Tue Feb 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1

* Mon Feb  5 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update

* Tue Jan 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update

* Wed Dec 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to CVS
- Enable building kpilot
- Obsolete kpilot
- Don't exclude ia64, use -O0 on ia64
- Disable building kpilot on ia64 (compiler breakage)

* Mon Oct 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.0 final

* Wed Oct  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.0

* Sun Oct  1 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new CVS
- fix installation of fonts

* Sat Sep 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new CVS snapshot
- fix up spec file

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- get rid of the 3d-screensavers package - now that qt-GL is part of qt,
  there's no need to keep them separate to avoid the dependency.

* Mon Aug 21 2000 Than Ngo <than@redhat.com>
- fix gnome-session so that KDE2 can be started from gdm
- pam/kde2 instead pam/kde to avoid problem with KDE1
- don't requires qt-GL, It's now in qt

* Sun Aug 20 2000 Than Ngo <than@redhat.com>
- fix dependency problem with KDE1 so that KDE1 and KDE2 can be installed
  at the same time
- add missing ldconfig in %post anf %postun
- fix for reading config files in /etc/X11/xdm, add Xsession to requires

* Tue Aug  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix keytable in konsole (Bug #15682)

* Sun Aug  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild, now that kdelibs2 works on alpha
- use the same ugly hack to get kdebase to compile
- remove ksysguard on alpha (even more compiler problems)

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot (fixed libGL detection in CVS)

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move to /usr/lib/kde2
- new snapshot

* Sun Jul 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the --xdmdir arg to be correct (oops)

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- move kdm config files from /usr/config to /etc/X11 by forcing xdmdir

* Fri Jul 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- some fixes to spec file

* Tue Jul 18 2000 Than Ngo <than@redhat.de>
- rebuilt against glibc-2.1.92-14, gcc-2.96-40

* Sun Jul 16 2000 Than Ngo <than@redhat.de>
- use new snapshot
- disable Motif

* Tue Jul 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- use gcc 2.96
- new snapshot

* Sun Jul  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Epoch 3
- Update to current
- Use egcs++

* Fri Jun 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update (I put the fixes directly to CVS rather than collecting them
  in the spec)

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- remove man2html; we get that from man
- new snapshot

* Tue Jun 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- ExcludeArch ia64 for now
- remove gnome .desktop file, we get it from gnome-core now.

* Wed Apr  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- remove dependency on xpm (now in XFree86)

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- move it to /usr, where it belongs

* Sat Dec 25 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Build the OpenGL screensavers, and move them to a separate package
- Improve the spec file (BuildPrereqs etc.)

* Thu Dec 16 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- remove patch #3 (obsoleted by kwin)

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.de>
- 2.0 CVS snapshot
- fix compilation

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- clean up files in /tmp from startkde
- mark doc files as such

* Tue Sep 21 1999 Preston Brown <pbrown@redhat.com>
- start autorun if present in startkde
- check for configured soundcard before running sound services

* Mon Sep 20 1999 Preston Brown <pbrown@redhat.com>
- made kdelnks display Name property if they are of type Link

* Thu Sep 16 1999 Preston Brown <pbrown@redhat.com>
- moved png handling here (from kdelibs)
- changed low color icon directory name to locolor

* Tue Sep 14 1999 Preston Brown <pbrown@redhat.com>
- added optional session management to logout dialog
- include GNOME menus

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- added link to /etc/X11/applnk, .directory file
- included lowcolor icon sub-package
- enable .desktop file access

* Fri Sep 10 1999 Preston Brown <pbrown@redhat.com>
- customized startkde script to set up user environment if not present.
- mention kthememgr in description.

* Wed Sep 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.1.2 release
- kvt is back
- kde icon included
- linux console fonts included

* Thu Jul 15 1999 Preston Brown <pbrown@redhat.com>
- PAM console logout problem solved.

* Mon Jul 12 1999 Preston Brown <pbrown@redhat.com>
- now includes screensaver password security fix

* Fri Jun 11 1999 Preston Brown <pbrown@redhat.com>
- snapshot, includes kde 1.1.1 + fixes
- kvt removed for security reasons.  It is a steaming pile of...

* Mon Apr 19 1999 Preston Brown <pbrown@redhat.com>
- last snapshot before release

* Fri Apr 16 1999 Preston Brown <pbrown@redhat.com>
- today's snapshot makes kfm a bit nicer and some other fixes
- moved default rc files to kdesupport

* Thu Apr 15 1999 Preston Brown <pbrown@redhat.com>
- SUID bit removed from konsole_grantpty -- not needed w/glibc 2.1

* Wed Apr 14 1999 Preston Brown <pbrown@redhat.com>
- built with today's snapshot -- had to rebuild to fix pam problems.

* Tue Apr 13 1999 Preston Brown <pbrown@redhat.com>
- new snapshot fixes mimetype video/x-flic problem

* Mon Apr 12 1999 Preston Brown <pbrown@redhat.com>
- latest stable snapshot

* Fri Apr 09 1999 Preston Brown <pbrown@redhat.com>
- removed bell.xpm (used to be in fvwm2-icons, don't want installer to see
- this previous connection and autoselect kdebase for upgrade).

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- moved gdm patch

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- added gdm session control file

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- added pam-console stuff to kde pam file

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgraded to KDE 1.1 final.

* Tue Jan 19 1999 Preston Brown <pbrown@redhat.com>
- updated macros for RPM 3.0, removed red hat logo.

* Tue Jan 05 1999 Preston Brown <pbrown@redhat.com>
- re-merged from Duncan Haldane's stuff
