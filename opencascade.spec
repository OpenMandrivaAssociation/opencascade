%define gittag	gbc55d69
%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

Name:		opencascade
Group:		Sciences/Physics
Epoch:		0
Version:	0.3.0
Release:	1
Summary:	3D modeling & numerical simulation
License:	LGPL with differences
URL:		https://github.com/tpaviot/oce
Source0:	https://download.github.com/tpaviot-oce-OCE-%{version}-0-%{gittag}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libxmu-devel
BuildRequires:	libx11-devel
BuildRequires:	freetype2-devel
BuildRequires:	ftgl-devel
BuildRequires:	bison flex
BuildRequires:	cmake
BuildRequires:	tcl-devel
BuildRequires:	tk-devel

Requires:	pdksh
Requires:	tcl
Requires:	tix
Requires:	tk
Patch0:		OCE-0.3.0-link.patch
Patch1:		OCE-0.3.0-str.patch

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
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_datadir}/%{name}

#-----------------------------------------------------------------------
%package	-n %{libname}
Summary:	3D modeling & numerical simulation
Group:		System/Libraries

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
%defattr(-,root,root)
%{_libdir}/lib*.so.*

#-----------------------------------------------------------------------
%package	-n %{devname}
Summary:	3D modeling & numerical simulation
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

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
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/%{name}
%{_datadir}/cmake/Modules/*.cmake

#-----------------------------------------------------------------------
%prep
%setup -qn tpaviot-oce-c74e688
%patch0 -p0
%patch1 -p0

#-----------------------------------------------------------------------
%build
%cmake -DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DOCE_INSTALL_PREFIX=%{_prefix} \
	-DOCE_INSTALL_INCLUDE_DIR=%{_includedir}/%{name} \
	-DOCE_INSTALL_LIB_DIR=%{_libdir} \
	-DOCE_INSTALL_DATA_DIR=%{_datadir}/%{name} \
	-DOCE_INSTALL_SCRIPT_DIR=%{_sysconfdir}/profile.d \
	-DOCE_INSTALL_CMAKE_DATA_DIR=share/cmake/Modules
%make

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
%makeinstall_std -C build
