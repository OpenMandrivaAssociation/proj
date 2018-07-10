Summary:	Cartographic projection software
Name:		proj
Version:	5.1.0
Release:	2
License:	MIT
Group:		Sciences/Geosciences
Url:		http://proj4.org/
Source0:	http://download.osgeo.org/proj/proj-%{version}.tar.gz
Source1:	http://download.osgeo.org/proj/proj-datumgrid-1.7.tar.gz
Patch0:		remove_include.patch
Provides:	proj4

%description
Cartographic projection software and libraries.

%files
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/proj

#-------------------------------------------------------------------------

%define major 13
%define oldlibname %mklibname %{name} 12
%define libname %mklibname %{name} %{major}

%package -n %{libname}
Summary:	Cartographic projection software - Libraries
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Cartographic projection software and libraries.

%files -n %{libname}
%{_libdir}/libproj.so.%{major}*

#-------------------------------------------------------------------------

%define devname %mklibname -d %{name}

%package -n %{devname}
Summary:	Cartographic projection software - Development files
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Cartographic projection development files.

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/proj.pc

#-------------------------------------------------------------------------

%prep
%setup -D -q
%patch0 -p0
find . -name "*.c" -exec chmod 644 {} \;
pushd nad
tar xf %{SOURCE1}
popd

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_includedir}
install -m644 src/projects.h %{buildroot}%{_includedir}/

