###//%define _disable_ld_no_undefined 1
%define	name	uptimed
%define	version	0.3.16
%define	release	%mkrel 1

%define	major 0
%define	libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A daemon to record and keep track of system uptimes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Monitoring
URL:		http://podgorny.cz/moin/Uptimed
Source0:	http://podgorny.cz/uptimed/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Patch0:		uptimed-makefile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
Uptimed is an uptime record daemon keeping track of the highest 
uptimes the system ever had. Instead of using a pid file to 
keep sessions apart from each other, it uses the system boot 
time. 

Uptimed has the ability to inform you of records and milestones 
though syslog and e-mail, and comes with a console front end to 
parse the records, which can also easily be used to show your 
records on your Web page.

%package -n %{libname}
Summary:	Generic libraries need by uptimed
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Generic libraries needed by uptimed.

%package -n %{develname}
Summary:	Generic libraries need by uptimed
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{develname}
Development files for uptimed.

%prep
%setup -q
%patch0 -p0 -b .makefile
cp -a %{SOURCE1} .

# this was faster, and easier...
touch NEWS

%build
./bootstrap.sh

%configure --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std 

install -m755 uptimed.init -D %{buildroot}%{_initrddir}/uptimed
mv %{buildroot}%{_sysconfdir}/uptimed.conf-dist %{buildroot}%{_sysconfdir}/uptimed.conf

%post
install -m 755 -d %{_var}/spool/uptimed
%_post_service uptimed

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%preun
%_preun_service uptimed

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libuptimed.so
%{_libdir}/libuptimed.la
