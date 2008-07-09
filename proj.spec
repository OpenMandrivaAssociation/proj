%define major 0
%define libname %mklibname %{name} %{major}
%define libname_orig %mklibname %name

Name: proj
Version: 4.6.0
Release: %mkrel 2
Summary: Cartographic projection software
Source0: ftp://ftp.remotesensing.org/pub/proj/%{name}-%{version}.tar.gz
Source1: ftp://ftp.remotesensing.org/pub/proj/proj-datumgrid-1.3.tar.gz
License: MIT
URL: http://trac.osgeo.org/proj/
Group: Sciences/Geosciences
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Cartographic projection software and libraries.

%files
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/proj

#-------------------------------------------------------------------------

%package -n %{libname}
Summary: Cartographic projection software - Libraries
Group: System/Libraries
License: MIT

%description -n %{libname}
Cartographic projection software and libraries.

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*

#-------------------------------------------------------------------------

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

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.la

#-------------------------------------------------------------------------

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

%files -n %{libname}-static-devel
%defattr (-,root,root)
%{_libdir}/*.a

#-------------------------------------------------------------------------

%prep
rm -rf %buildroot

%setup -D -q
tar xfz %{SOURCE1} -C nad

%configure

%build
%make

%install
%makeinstall

%clean
rm -rf %buildroot  


