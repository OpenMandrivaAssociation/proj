# Bogus debugsource list
#global _empty_manifest_terminate_build 0

%define major 22
%define oldlibname %mklibname %{name} 19
%define olderlibname %mklibname %{name} 15
%define evenolderlibname %mklibname %{name} 12
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Cartographic projection software
Name:		proj
Version:	8.2.1
Release:	1
License:	MIT
Group:		Sciences/Geosciences
Url:		http://proj4.org/
Source0:	https://download.osgeo.org/proj/proj-%{version}.tar.gz
Source1:	https://download.osgeo.org/proj/proj-datumgrid-1.8.zip
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	sqlite-tools

Provides:	proj4

%description
Cartographic projection software and libraries.

%files
%doc AUTHORS COPYING ChangeLog README
%doc %{_docdir}/proj/NEWS
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/proj

#-------------------------------------------------------------------------

%package -n %{libname}
Summary:	Cartographic projection software - Libraries
Group:		System/Libraries
%rename %{oldlibname}
%rename %{olderlibname}
%rename %{evenolderlibname}

%description -n %{libname}
Cartographic projection software and libraries.

%files -n %{libname}
%{_libdir}/libproj.so.%{major}*

#-------------------------------------------------------------------------

%package -n %{devname}
Summary:	Cartographic projection software - Development files
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Cartographic projection development files.

%files -n %{devname}
%{_includedir}/*.h
%{_includedir}/proj/*.hpp
%{_libdir}/*.so
%{_libdir}/pkgconfig/proj.pc
%{_libdir}/cmake/proj
%{_libdir}/cmake/proj4

#-------------------------------------------------------------------------

%prep
%autosetup -D
#find . -name "*.c" -exec chmod 644 {} \;

pushd data
tar xf %{SOURCE1}
popd

%build
%cmake \
	-DUSE_EXTERNAL_GTEST:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
