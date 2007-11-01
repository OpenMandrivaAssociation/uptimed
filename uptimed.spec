%define	name	uptimed
%define	version	0.3.12
%define rel	1
%define	release	%mkrel %rel

%define	major	0
%define	libname	%mklibname %{name} %{major}

Summary:	A daemon to record and keep track of system uptimes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://podgorny.cz/moin/Uptimed
Source0:	http://podgorny.cz/uptimed/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Patch0:		uptimed-0.3.7-makefile.patch
BuildRequires:	automake1.9
Requires(post):	rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Uptimed is an uptime record daemon keeping track of the highest 
uptimes the system ever had. Instead of using a pid file to 
keep sessions apart from each other, it uses the system boot 
time. 

Uptimed has the ability to inform you of records and milestones 
though syslog and e-mail, and comes with a console front end to 
parse the records, which can also easily be used to show your 
records on your Web page.

%package -n	%{libname}
Summary:	Generic libraries need by uptimed
Group:		System/Libraries
Provides:	lib%{name} = %{version}

%description -n	%{libname}
Generic libraries needed by uptimed.

%package -n	%{libname}-devel
Summary:	Generic libraries need by uptimed
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
Development files for uptimed.

%prep
%setup -q
%patch0 -p0 -b .makefile
cp -a %SOURCE1 .

# this was faster, and easier...
touch NEWS

%build
aclocal-1.9
automake-1.9
%configure2_5x
%make

%install
rm -rf %{buldroot}
%makeinstall_std 

install -m755 uptimed.init -D %{buildroot}%{_initrddir}/uptimed
mv %{buildroot}%{_sysconfdir}/uptimed.conf-dist %{buildroot}%{_sysconfdir}/uptimed.conf

%post
install -m 755 -d %{_var}/spool/uptimed
%_post_service uptimed

%post -n %{libname} -p /sbin/ldconfig

%preun
%_preun_service uptimed

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS CREDITS ChangeLog INSTALL.cgi INSTALL.upgrade README TODO sample-cgi/
%config(noreplace) %{_sysconfdir}/uptimed.conf
%{_initrddir}/uptimed
%{_sbindir}/uptimed
%{_bindir}/uprecords
%{_mandir}/*/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libuptimed.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libuptimed.so
%{_libdir}/libuptimed.a
%{_libdir}/libuptimed.la
