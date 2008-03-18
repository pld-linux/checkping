Summary:	CheckPing
Name:		checkping
Version:	0.4
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/checkping/%{name}-%{version}.tar.gz
# Source0-md5:	79b61771893779a47c70de4814e6d66f
URL:		http://sourceforge.net/projects/checkping/
Requires:	php(gd)
Requires:	php(mysql)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/%{name}
%define		_appdir			%{_datadir}/%{name}

%description
Keep your eye on unlimited number of machines using CheckPing.
Timeouts, ping times, live graphs and notification via
mail/SMS/pager/etc.

%prep
%setup -q

%{__sed} -i -e "
s,HOMEDIR='/path/to/checkping-0.4',HOMEDIR='%{_sysconfdir}',
s,DBUSER='root',DBUSER='mysql',
s,DBPASS='mysecretpass',DBPASS='',
s,ERRORMAIL='cal6@spam.ee',ERRORMAIL='root@localhost',
" checkping.sh

%{__sed} -i -e "
s/'root'/'mysql'/
s/'mysecretpass'/''/
" connect.php

%{__sed} -n '3,/^##/p' checkping.sh > README

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_appdir}}
install checkping.sh $RPM_BUILD_ROOT%{_bindir}/checkping
touch $RPM_BUILD_ROOT%{_sysconfdir}/iplist.txt
cp -a *.php $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/checkping
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/iplist.txt
%{_appdir}
