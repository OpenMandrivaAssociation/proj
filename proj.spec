Name: proj
Version: 4.8.0
Release: 3
Summary: Cartographic projection software
Source0: ftp://ftp.remotesensing.org/pub/proj/%{name}-%{version}.tar.gz
Source1: ftp://ftp.remotesensing.org/pub/proj/proj-datumgrid-1.5.zip
License: MIT
URL: http://trac.osgeo.org/proj/
Group: Sciences/Geosciences
Provides: proj4
Patch0:	remove_include.patch

%description
Cartographic projection software and libraries.

%files
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/proj

#-------------------------------------------------------------------------

%define major 0
%define libname %mklibname %{name} %{major}

%package -n %{libname}
Summary: Cartographic projection software - Libraries
Group: System/Libraries
License: MIT

%description -n %{libname}
Cartographic projection software and libraries.

%files -n %{libname}
%{_libdir}/*.so.%{major}*

#-------------------------------------------------------------------------

%define develname %mklibname -d %name

%package -n %{develname}
Summary: Cartographic projection software - Development files
Group: Development/Other
Provides: %{name}-devel = %{version}
Provides: proj4-devel = %{version}
Provides: libproj4-devel = %{version}
Requires: %{libname} = %{version}
Obsoletes: %{mklibname -d proj 0}

%description -n %{develname}
Cartographic projection development files.

%files -n %{develname}
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/proj.pc

#-------------------------------------------------------------------------

%define sdevelname %mklibname -d -s %name

%package -n %sdevelname
Summary: Cartographic projection software - Development files
Group: Development/Other
Provides: %name-static-devel = %{version}
Provides: proj4-static-devel = %{version}
Provides: libproj4-static-devel = %{version}
Requires: %{develname} = %{version}
Requires: %{libname} = %version-%release
Obsoletes: %{mklibname -d -s proj 0}

%description -n %{sdevelname}
Cartographic projection development files (static).

%files -n %{sdevelname}
%{_libdir}/*.a

#-------------------------------------------------------------------------

%prep
%setup -D -q
%patch0 -p0
find . -name "*.c" -exec chmod 644 {} \;
pushd nad
unzip -qqo %{SOURCE1}
popd

%build
%configure2_5x
%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_includedir}
install -m644 src/projects.h %{buildroot}%{_includedir}/

