%define major 0
%define libname %mklibname %{name} %{major}

Name: proj
Version: 4.6.1
Release: %mkrel 1
Summary: Cartographic projection software
Source0: ftp://ftp.remotesensing.org/pub/proj/%{name}-%{version}.tar.gz
Source1: ftp://ftp.remotesensing.org/pub/proj/proj-datumgrid-1.4.tar.gz
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
%define develname %mklibname -d %name
%package -n %{develname}
Summary: Cartographic projection software - Development files
Group: Development/Other
License: MIT
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Obsoletes: %{_lib}proj0-devel < %{version}-%{release}

%description -n %{develname}
Cartographic projection development files.

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.la

#-------------------------------------------------------------------------
%define sdevelname %mklibname -d -s %name
%package -n %sdevelname
Summary: Cartographic projection software - Development files
Group: Development/Other
License: MIT
Provides: %name-static-devel = %{version}-%{release}
Requires: %{develname} = %{version}-%{release}
Requires: %{libname} = %version-%release
Obsoletes: %{_lib}proj0-static-devel < %{version}-%{release}

%description -n %{sdevelname}
Cartographic projection development files (static).

%files -n %{sdevelname}
%defattr (-,root,root)
%{_libdir}/*.a

#-------------------------------------------------------------------------

%prep
%setup -D -q
tar xfz %{SOURCE1} -C nad

%build
%configure2_5x
%make

%install
rm -rf %buildroot
%makeinstall_std

%clean
rm -rf %buildroot  


