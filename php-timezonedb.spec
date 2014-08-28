%define modname timezonedb
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A60_%{modname}.ini

Summary:	Timezone Database to be used with PHP's date and time functions
Name:		php-%{modname}
Epoch:		3
Version:	2014.6
Release:	1
Group:		Development/PHP
License:	PHP License
Url:		http://pecl.php.net/package/timezonedb/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	A60_timezonedb.ini
BuildRequires:	file
BuildRequires:	php-devel >= 3:5.5.0

%description
This extension is a drop-in replacement for the builtin timezone database that
comes with PHP. You should only install this extension in case you need to get
a later version of the timezone database than the one that ships with PHP.

The data that this extension uses comes from the "Olson" database, which is
located at ftp://elsie.nci.nih.gov/pub/.

%prep
%setup -qn %{modname}-%{version}
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
%configure2_5x \
	--with-libdir=%{_lib} \
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
%doc CREDITS package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

