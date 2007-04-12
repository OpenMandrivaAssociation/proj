%define name proj
%define version 4.4.9
%define release %mkrel 2

%define major 0
%define libname %mklibname %{name} %{major}
%define libname_orig %mklibname %name

Summary: Cartographic projection software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.remotesensing.org/pub/proj/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.remotesensing.org/pub/proj/proj-nad27-1.1.tar.bz2
License: MIT
URL: http://www.remotesensing.org/proj/
Group: Sciences/Geosciences
Buildroot: %{_tmppath}/%{name}-buildroot

%description
Cartographic projection software and libraries.

%package -n %{libname}
Summary: Cartographic projection software - Libraries
Group: System/Libraries
License: MIT

%description -n %{libname}
Cartographic projection software and libraries.

%package -n %{libname}-devel
Summary: Cartographic projection software - Development files
Group: Development/Other
License: MIT
Provides: %{libname_orig}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Obsoletes: %{libname_orig}-devel
Requires: %{libname} = %{version}-%{release}

%description -n %{libname}-devel
Cartographic projection development files.

%package -n %{libname}-static-devel
Summary: Cartographic projection software - Development files
Group: Development/Other
License: MIT
Provides: %{libname_orig}-static-devel = %{version}-%{release}
Provides: lib%{libname_orig}-static-devel = %{version}-%{release}
Obsoletes: %{libname_orig}-static-devel
Requires: %{libname} = %version-%release

%description -n %{libname}-static-devel
Cartographic projection development files (static).

%prep
rm -rf $RPM_BUILD_ROOT

%setup -D -q
tar xjf %{SOURCE1} -C nad

%configure

%build
%make

%install
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT  

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr (-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/proj
%doc AUTHORS COPYING ChangeLog README

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.la

%files -n %{libname}-static-devel
%defattr (-,root,root)
%{_libdir}/*.a

