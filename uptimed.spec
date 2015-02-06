%define _disable_ld_no_undefined 1

%define	major 0
%define	libname	%mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A daemon to record and keep track of system uptimes
Name:		uptimed
Version:	0.3.17
Release:	3
License:	GPLv2+
Group:		Monitoring
URL:		http://podgorny.cz/moin/Uptimed
Source0:	http://podgorny.cz/uptimed/releases/%{name}-%{version}.tar.bz2
Source2:	%{name}.init.systemd
Patch0:		uptimed-makefile.patch
Patch1:		uptimed-systemd.patch

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
#%patch0 -p0 -b .makefile
%patch1 -p1 -b .systemd
cp -a %{SOURCE2} ./etc/uptimed.service.in

# this was faster, and easier...
touch NEWS

%build
./bootstrap.sh
autoreconf -i
%configure --disable-static
%make

%install
%makeinstall_std 

mkdir -p %{buildroot}/var/spool/%{name}
install -m755 etc/uptimed.service -D %{buildroot}/lib/systemd/system/%{name}.service
mv %{buildroot}%{_sysconfdir}/uptimed.conf-dist %{buildroot}%{_sysconfdir}/uptimed.conf

%post
systemd-tmpfiles --create
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc AUTHORS CREDITS ChangeLog INSTALL.cgi INSTALL.upgrade README TODO sample-cgi/
%config(noreplace) %{_sysconfdir}/uptimed.conf
/lib/systemd/system/%{name}.service
%{_sbindir}/uptimed
%dir /var/spool/uptimed
%{_bindir}/uprecords
%{_mandir}/*/*

%files -n %{libname}
%{_libdir}/libuptimed.so.%{major}*

%files -n %{develname}
%{_libdir}/libuptimed.so
