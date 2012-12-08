%define modname timezonedb
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A60_%{modname}.ini

# (tpg) define release here
%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

Summary:	Timezone Database to be used with PHP's date and time functions
Name:		php-%{modname}
Version:	2012.5
Release:	%{release}
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/timezonedb/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	A60_timezonedb.ini
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	file
Epoch:		3

%description
This extension is a drop-in replacement for the builtin timezone database that
comes with PHP. You should only install this extension in case you need to get
a later version of the timezone database than the one that ships with PHP.

The data that this extension uses comes from the "Olson" database, which is
located at ftp://elsie.nci.nih.gov/pub/.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
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

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 3:2012.3-2mdv2012.0
+ Revision: 794920
- rebuild for php-5.4.x

* Mon Apr 02 2012 Oden Eriksson <oeriksson@mandriva.com> 3:2012.3-1
+ Revision: 788780
- 2012.3

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 3:2011.14-2
+ Revision: 761124
- rebuild
- 2011.14

* Wed Aug 31 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.9-1
+ Revision: 697570
- 2011.9 (2011i)

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.8-3
+ Revision: 696376
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.8-2
+ Revision: 695321
- rebuilt for php-5.3.7

* Mon Jun 27 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.8-1
+ Revision: 687519
- 2011.8

* Sun May 01 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.7-1
+ Revision: 661148
- 2011.7 (2011g)
- S1: added the date section with instructions how to set date.timezone

* Mon Apr 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.5-1
+ Revision: 650138
- 2011.5 (2011e)

* Wed Mar 23 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.4-1
+ Revision: 647818
- 2011.4 (2011d)

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.3-2
+ Revision: 646560
- rebuilt for php-5.3.6

* Sun Mar 13 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.3-1
+ Revision: 644267
- 2011.3 (2011c)

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 3:2011.2-2
+ Revision: 640416
- rebuild

* Wed Feb 16 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.2-1
+ Revision: 638028
- 2011.2

* Sat Feb 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2011.1-1
+ Revision: 636135
- 2011.1

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2010.15-5mdv2011.0
+ Revision: 629748
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 3:2010.15-4mdv2011.0
+ Revision: 628054
- ensure it's built without automake1.7

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.15-3mdv2011.0
+ Revision: 607170
- rebuild

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.15-2mdv2011.0
+ Revision: 600186
- rebuild

* Wed Nov 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.15-1mdv2011.0
+ Revision: 592815
- 2010.15 (2010o)

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.13-2mdv2011.0
+ Revision: 588725
- rebuild

* Mon Oct 04 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.13-1mdv2011.0
+ Revision: 582872
- 2010.13
- added backporting macros for updates

* Thu Sep 16 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.12-1mdv2011.0
+ Revision: 578880
- 2010.12

* Thu Apr 29 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.9-1mdv2010.1
+ Revision: 540802
- 2010.9 (2010i)

* Tue Mar 30 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.7.1-1mdv2010.1
+ Revision: 529178
- 2010.7.1 (2010g)

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.3-3mdv2010.1
+ Revision: 518813
- remove stray directory

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.3-2mdv2010.1
+ Revision: 514692
- rebuilt for php-5.3.2

* Wed Mar 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.3-1mdv2010.1
+ Revision: 513851
- 2010.3 (2010c)

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.2-2mdv2010.1
+ Revision: 509094
- rebuild

* Tue Jan 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.2-1mdv2010.1
+ Revision: 496744
- 2010.2

* Sun Jan 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2010.1-1mdv2010.1
+ Revision: 495521
- 2010.1

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 3:2009.21-1mdv2010.1
+ Revision: 485299
- 2009.21
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.18-2mdv2010.1
+ Revision: 468094
- rebuilt against php-5.3.1

* Wed Nov 11 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.18-1mdv2010.1
+ Revision: 464624
- 2009.18 (2009r)

* Fri Nov 06 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.17-1mdv2010.1
+ Revision: 461167
- 2009.17

* Tue Oct 27 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.16-1mdv2010.0
+ Revision: 459537
- 2009.16 (2009p)

* Wed Oct 14 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.14-1mdv2010.0
+ Revision: 457247
- 2009.14

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.13-2mdv2010.0
+ Revision: 451224
- rebuild

* Fri Sep 11 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.13-1mdv2010.0
+ Revision: 438271
- 2009.13

* Wed Aug 19 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.12-1mdv2010.0
+ Revision: 418103
- 2009.12

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 3:2009.10-2mdv2010.0
+ Revision: 397622
- Rebuild

* Tue Jul 14 2009 Oden Eriksson <oeriksson@mandriva.com> 3:2009.10-1mdv2010.0
+ Revision: 395956
- 2009.10

* Wed Jan 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2007.11-1mdv2008.1
+ Revision: 140482
- 2007.11

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.10-1mdv2008.1
+ Revision: 114573
- 2007.10

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.9-2mdv2008.1
+ Revision: 107579
- restart apache if needed

* Mon Nov 05 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.9-1mdv2008.1
+ Revision: 106010
- 2007.9

* Sat Oct 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.8-1mdv2008.1
+ Revision: 97905
- 2007.8

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.5-4mdv2008.0
+ Revision: 77464
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.5-3mdv2008.0
+ Revision: 64308
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.5-2mdv2008.0
+ Revision: 39391
- use distro conditional -fstack-protector

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.5-1mdv2008.0
+ Revision: 14495
- 2007.5


* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.3-1mdv2007.0
+ Revision: 134199
- Import php-timezonedb

* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2007.3-1mdv2007.1
- initial Mandriva package

