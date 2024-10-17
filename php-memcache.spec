%define modname memcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A43_%{modname}.ini

%define snapshot 4991c2f
%define snapshot_full 4991c2fff22d00dc81014cc92d2da7077ef4bc86
Summary:	Memcached extension for php
Name:		php-%{modname}
Version:	3.0.9
Release:	0.2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/memcache
Source0:	http://pecl.php.net/get/%{modname}-%{version}-%{snapshot}.tar.gz
Source1:	%{modname}.ini
Requires:	memcached
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	zlib-devel
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Memcached is a caching daemon designed especially for dynamic web applications
to decrease database load by storing objects in memory. This extension allows
you to work with memcached through handy OO and procedural interfaces.

%prep

%setup -q -n pecl-%{modname}-%{snapshot_full}

cp %{SOURCE1} %{inifile}

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

ln -s %{_usrsrc}/php-devel/extensions ext

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \
    --with-zlib-dir=%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS README example.php package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Fri May 04 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-7mdv2012.0
+ Revision: 795877
- bump release
- fix build

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-6
+ Revision: 795475
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-5
+ Revision: 761267
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-4
+ Revision: 696443
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-3
+ Revision: 695433
- rebuilt for php-5.3.7

* Thu Jun 09 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-2
+ Revision: 683462
- bump release (svn loss?)
- 3.0.6

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-6
+ Revision: 646660
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-5mdv2011.0
+ Revision: 629834
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-4mdv2011.0
+ Revision: 628161
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-3mdv2011.0
+ Revision: 600507
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-2mdv2011.0
+ Revision: 588845
- rebuild

* Mon Oct 04 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.5-1mdv2011.0
+ Revision: 582941
- 3.0.5

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-9mdv2010.1
+ Revision: 514573
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-8mdv2010.1
+ Revision: 485404
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-7mdv2010.1
+ Revision: 468187
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-6mdv2010.0
+ Revision: 451291
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 3.0.4-5mdv2010.0
+ Revision: 397555
- Rebuild

* Sun Jul 05 2009 Colin Guthrie <cguthrie@mandriva.org> 3.0.4-4mdv2010.0
+ Revision: 392646
- Rebuild for new PHP

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-3mdv2010.0
+ Revision: 377006
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-2mdv2009.1
+ Revision: 346518
- rebuilt for php-5.2.9

* Tue Feb 24 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.4-1mdv2009.1
+ Revision: 344554
- 3.0.4

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.3-2mdv2009.1
+ Revision: 341777
- rebuilt against php-5.2.9RC2

* Tue Jan 13 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.3-1mdv2009.1
+ Revision: 329195
- 3.0.3

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-3mdv2009.1
+ Revision: 321875
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-2mdv2009.1
+ Revision: 310287
- rebuilt against php-5.2.7

* Sun Sep 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-1mdv2009.0
+ Revision: 284661
- 3.0.2

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-4mdv2009.0
+ Revision: 238412
- rebuild

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-3mdv2009.0
+ Revision: 229681
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-2mdv2009.0
+ Revision: 200250
- rebuilt for php-5.2.6

* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-1mdv2008.1
+ Revision: 163167
- 3.0.1

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-2mdv2008.1
+ Revision: 162110
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 27 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-1mdv2008.1
+ Revision: 113371
- 3.0.0

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-2mdv2008.1
+ Revision: 107686
- restart apache if needed

* Thu Nov 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.1-1mdv2008.1
+ Revision: 104604
- 2.2.1

* Thu Sep 27 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-1mdv2008.1
+ Revision: 93254
- 2.2.0

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-5mdv2008.0
+ Revision: 77560
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-4mdv2008.0
+ Revision: 39508
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-3mdv2008.0
+ Revision: 33862
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-2mdv2008.0
+ Revision: 21341
- rebuilt against new upstream version (5.2.2)

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.2-1mdv2008.0
+ Revision: 14504
- 2.1.2


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-3mdv2007.0
+ Revision: 117599
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2007.0
+ Revision: 78087
- rebuilt for php-5.2.0
- Import php-memcache

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1
- 2.1.0

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.4-3
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.4-2mdk
- rebuild

* Thu May 18 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.4-1mdk
- 2.0.4

* Wed May 17 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.3-1mdk
- 2.0.3

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-3mdk
- rebuilt for php-5.1.4

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-2mdk
- rebuilt for php-5.1.3

* Wed Feb 01 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-1mdk
- 2.0.1

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-2mdk
- rebuilt against php-5.1.2

* Sun Jan 08 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-1mdk
- initial Mandriva package

