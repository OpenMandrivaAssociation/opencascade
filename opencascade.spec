%define major	7
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

# based on opencascade 6.8.0
%define version 7.5.0
%define occtag %(echo %version | tr . _)

Name:		opencascade
Group:		Sciences/Physics
Version:	%{version}
Release:	1
Summary:	3D modeling & numerical simulation
License:	LGPLv2 with exceptions
URL:		https://github.com/tpaviot/oce
Source0:	https://github.com/tpaviot/oce/archive/upstream/V%{occtag}/%{name}-%{version}.tar.gz
Patch1:		opencascade-fix_externlib.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires: 	ninja
BuildRequires:	bison
BuildRequires:  cmake(Qt5)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5Xml)
BuildRequires:  cmake(Qt5Sql)
BuildRequires:  cmake(vtk)
BuildRequires:	flex
BuildRequires:	hdf5-devel
BuildRequires:	mesa-common-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xmuu)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:  pkgconfig(tbb)
BuildRequires:  pkgconfig(xi)

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
#%{_bindir}/*.sh
#%{_bindir}/DRAW*

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
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/cmake/%{name}

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n oce-upstream-V%{occtag}

%build
export DESTDIR="%{buildroot}"
%cmake \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DOCE_INSTALL_PREFIX=%{_prefix} \
	-DOCE_INSTALL_INCLUDE_DIR=%{_includedir}/%{name} \
	-DOCE_INSTALL_LIB_DIR=%{_libdir} \
	-DOCE_INSTALL_DATA_DIR=%{_datadir}/%{name} \
	-DOCE_INSTALL_SCRIPT_DIR=%{_sysconfdir}/profile.d \
	-DUSE_TBB:BOOL=ON \
	-DUSE_VTK:BOOL=ON \
	-DINSTALL_VTK:BOOL=False \
	-D3RDPARTY_VTK_LIBRARY_DIR:PATH=%{_libdir} \
	-D3RDPARTY_VTK_INCLUDE_DIR:PATH=%{_includedir} \
	-D3RDPARTY_VTK_INCLUDE_DIR=%{_includedir}/vtk \
	-DINSTALL_DIR_LIB=%{_lib} \
	-DINSTALL_DIR_CMAKE=%{_lib}/cmake/%{name} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# adjust environment/directories to avoid (too much) script patching
ln -sf %{_libdir} %{buildroot}%{_datadir}/%{name}/lib
ln -sf %{_includedir}/%{name} %{buildroot}%{_datadir}/%{name}/inc
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/lin
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/Linux

