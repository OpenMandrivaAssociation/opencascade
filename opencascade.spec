%define major	11
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

# based on opencascade 6.8.0
%define occtag	6.9.1

# tpaviot-oce version 0.7.0
%define ocegit	0.18.1

Name:		opencascade
Group:		Sciences/Physics
Version:	%{occtag}.%{ocegit}
Release:	2
Summary:	3D modeling & numerical simulation
License:	LGPLv2 with exceptions
URL:		https://github.com/tpaviot/oce
Source0:	https://github.com/tpaviot/oce/archive/OCE-%{ocegit}.tar.gz
BuildRequires:	mesa-common-devel
BuildRequires:  glew-devel
BuildRequires:  pkgconfig(glu)
BuildRequires:	pkgconfig(xmuu)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	cmake
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
Requires:	pdksh
Requires:	tcl
Requires:	tix
Requires:	tk

%description
Open CASCADE Technology is software development platform freely available
in open source. It includes components for 3D surface and solid modeling,
visualization, data exchange and rapid application development.

Open CASCADE Technology can be best applied in development of numerical
simulation software including CAD/CAM/CAE, AEC and GIS, as well as PDM
applications.

The Technology exists from the mid 1990-s and has already been used by
numerous commercial clients belonging to different domains from software
edition to heavy industry.

%files
%doc LICENSE_LGPL_21.txt OCCT_LGPL_EXCEPTION.txt
%{_datadir}/%{name}

#-----------------------------------------------------------------------
%package	-n %{libname}
Summary:	3D modeling & numerical simulation
Group:		System/Libraries
Obsoletes:	%{libname} < %{EVRD}

%description	-n %{libname}
Open CASCADE Technology is software development platform freely available
in open source. It includes components for 3D surface and solid modeling,
visualization, data exchange and rapid application development.

Open CASCADE Technology can be best applied in development of numerical
simulation software including CAD/CAM/CAE, AEC and GIS, as well as PDM
applications.

The Technology exists from the mid 1990-s and has already been used by
numerous commercial clients belonging to different domains from software
edition to heavy industry.

%files		-n %{libname}
%{_libdir}/lib*.so.%{major}
%{_libdir}/lib*.so.%{major}.*

#-----------------------------------------------------------------------
%package	-n %{devname}
Summary:	3D modeling & numerical simulation
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description	-n %{devname}
Open CASCADE Technology is software development platform freely available
in open source. It includes components for 3D surface and solid modeling,
visualization, data exchange and rapid application development.

Open CASCADE Technology can be best applied in development of numerical
simulation software including CAD/CAM/CAE, AEC and GIS, as well as PDM
applications.

The Technology exists from the mid 1990-s and has already been used by
numerous commercial clients belonging to different domains from software
edition to heavy industry.

%files		-n %{devname}
%{_libdir}/lib*.so
%{_includedir}/%{name}
%{_datadir}/cmake/Modules/*.cmake

#-----------------------------------------------------------------------
%prep
%setup -qn oce-OCE-%{ocegit}
%apply_patches

#-----------------------------------------------------------------------
%build
%cmake -DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DOCE_INSTALL_PREFIX=%{_prefix} \
	-DOCE_INSTALL_INCLUDE_DIR=%{_includedir}/%{name} \
	-DOCE_INSTALL_LIB_DIR=%{_libdir} \
	-DOCE_INSTALL_DATA_DIR=%{_datadir}/%{name} \
	-DOCE_INSTALL_SCRIPT_DIR=%{_sysconfdir}/profile.d \
	-DOCE_INSTALL_CMAKE_DATA_DIR=share/cmake/Modules
perl -pi -e 's|/usr//usr|/usr|;' build_inc/oce-config.h
%make



#-----------------------------------------------------------------------
%install
perl -pi -e 's|/usr//usr|/usr|;' build/env.sh build/env.csh
%makeinstall_std -C build

# adjust environment/directories to avoid (too much) script patching
ln -sf %{_libdir} %{buildroot}%{_datadir}/%{name}/lib
ln -sf %{_includedir}/%{name} %{buildroot}%{_datadir}/%{name}/inc
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/lin
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/Linux
