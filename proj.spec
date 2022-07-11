%define major 25
%define lastversionedlibname %mklibname %{name} 22
%define oldlibname %mklibname %{name} 19
%define olderlibname %mklibname %{name} 15
%define evenolderlibname %mklibname %{name} 12
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}

Summary:	Cartographic projection software
Name:		proj
Version:	9.0.1
Release:	1
License:	MIT
Group:		Sciences/Geosciences
Url:		http://proj4.org/
Source0:	https://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:	https://download.osgeo.org/%{name}/%{name}-data-1.9.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	sqlite-tools
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	sqlite-tools

Requires:	%{name}-data = %{version}-%{release}

Provides:	proj4

%description
Cartographic projection software and libraries.

%files
%doc AUTHORS COPYING ChangeLog README
%doc %{_docdir}/%{name}/NEWS
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_mandir}/man1/*

#-------------------------------------------------------------------------

%package data
Summary:	Proj data files
BuildArch:	noarch

%description data
Proj arch independent data files.
	
%files data
%license %{_docdir}/%{name}/COPYING
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/CH
%{_datadir}/%{name}/GL27
%{_datadir}/%{name}/ITRF2000
%{_datadir}/%{name}/ITRF2008
%{_datadir}/%{name}/ITRF2014
%{_datadir}/%{name}/nad.lst
%{_datadir}/%{name}/nad27
%{_datadir}/%{name}/nad83
%{_datadir}/%{name}/other.extra
%{_datadir}/%{name}/%{name}.db
%{_datadir}/%{name}/%{name}.db-shm
%{_datadir}/%{name}/%{name}.db-wal
%{_datadir}/%{name}/%{name}.ini
%{_datadir}/%{name}/world
%{_datadir}/%{name}/README.DATA
%{_datadir}/%{name}/copyright_and_licenses.csv
%{_datadir}/%{name}/deformation_model.schema.json
%{_datadir}/%{name}/projjson.schema.json
%{_datadir}/%{name}/triangulation.schema.json

#-------------------------------------------------------------------------

%package -n %{libname}
Summary:	Cartographic projection software - Libraries
Group:		System/Libraries
%rename %{lastversionedlibname}
%rename %{oldlibname}
%rename %{olderlibname}
%rename %{evenolderlibname}

%description -n %{libname}
Cartographic projection software and libraries.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

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
%{_includedir}/%{name}/*.hpp
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}
%{_libdir}/cmake/%{name}4

#-------------------------------------------------------------------------

%define data_subpkg(c:n:e:s:) \
%define countrycode %{-c:%{-c*}}%{!-c:%{error:Country code not defined}} \
%define countryname %{-n:%{-n*}}%{!-n:%{error:Country name not defined}} \
%define extrafile %{-e:%{_datadir}/%{name}/%{-e*}} \
%define wildcard %{!-s:%{_datadir}/%{name}/%{countrycode}_*} \
\
%package data-%{countrycode}\
Summary:      %{countryname} datum grids for Proj\
BuildArch:    noarch\
# See README.DATA \
License:      CC-BY and MIT and BSD and Public Domain \
Requires:     proj-data = %{version}-%{release} \
Supplements:  proj\
\
%description data-%{countrycode}\
%{countryname} datum grids for Proj.\
\
%files data-%{countrycode}\
%{wildcard}\
%{extrafile}

%data_subpkg -c at -n Austria
%data_subpkg -c au -n Australia
%data_subpkg -c be -n Belgium
%data_subpkg -c br -n Brasil
%data_subpkg -c ca -n Canada
%data_subpkg -c ch -n Switzerland
%data_subpkg -c de -n Germany
%data_subpkg -c dk -n Denmark -e DK
%data_subpkg -c es -n Spain
%data_subpkg -c eur -n %{quote:Nordic + Baltic} -e NKG
%data_subpkg -c fi -n Finland
%data_subpkg -c fo -n %{quote:Faroe Island} -e FO -s 1
%data_subpkg -c fr -n France
%data_subpkg -c is -n Island -e ISL
%data_subpkg -c jp -n Japan
%data_subpkg -c mx -n Mexico
%data_subpkg -c no -n Norway
%data_subpkg -c nl -n Netherlands
%data_subpkg -c nc -n %{quote:New Caledonia}
%data_subpkg -c nz -n %{quote:New Zealand}
%data_subpkg -c pl -n Poland
%data_subpkg -c pt -n Portugal
%data_subpkg -c se -n Sweden
%data_subpkg -c sk -n Slovakia
%data_subpkg -c uk -n %{quote:United Kingdom}
%data_subpkg -c us -n %{quote:United States}
%data_subpkg -c za -n %{quote:South Africa}

#-------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DUSE_EXTERNAL_GTEST:BOOL=ON \
	-DENABLE_IPO:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# omdv sqlite forced to use WAL journal for db files
# and beacuse the fyle-system at runtime will be
# read-only we should prodive -shm and -wal file now,
# even if they are empty. More info at
# https://sqlite.org/wal.html#read_only_databases
touch %{buildroot}%{_datadir}/%{name}/%{name}.db{-shm,-wal}

# data
install -dm 0755 %{buildroot}%{_datadir}/%{name}
tar -xf %{SOURCE1} --directory %{buildroot}%{_datadir}/%{name}

%check
# nkg test requires internet connection
# defmode test fails on znver1 arch
pushd build/test
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ctest -- -E nkg -E defmode
popd

