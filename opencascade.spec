%define major	%(echo %{version} |cut -d. -f1)
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define occtag %(echo %version | tr . _)

# Enabe this in order to use git snapshot
%define _from_git 0

%if %_from_git
%define commit	80ffc5f84dae96de6ed093d3e5d2466a9e368b27
%define shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

Name:		opencascade
Group:		Sciences/Physics
Version:	7.6.0
Release:	1
Epoch:		1
Summary:	3D modeling & numerical simulation
License:	LGPLv2.1 with exceptions
# Also look at
# https://github.com/tpaviot/oce
# for a Community Edition -- but as of
# 7.6.0, it has fallen too far behind
# upstream to still be useful
URL:		https://opencascade.org/
%if %_from_git
# Source cannot be downloaded directly from git so download from from an address like the following:
# https://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=%{commit};sf=tgz
# then rename as %{name}-%{version}.tgz
Source0:	http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=80ffc5f84dae96de6ed093d3e5d2466a9e368b27;sf=tgz#/opencascade-%{version}.tar.gz
%else
Source0:	https://dev.opencascade.org/system/files/occt/OCC_%{version}_release/opencascade-%{version}.tgz
%endif
Patch2:		opencascade-7.6.0-set-env-correctly.patch
Patch3:		opencascade-cmake.patch
Patch4:		oce-7.5.0-clang.patch
# (upstream)
Patch100:	opencascade-7.5.0-fix_tbb.patch
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
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:  pkgconfig(tbb)
BuildRequires:  pkgconfig(xi)

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
%{_bindir}/*.sh
%{_bindir}/DRAW*

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
%{_libdir}/cmake/%{name}/*.cmake

#-----------------------------------------------------------------------

%prep
%if %_from_git
%autosetup -p1 -n occt-%{shortcommit}
%else
%autosetup -p1
%endif

%build
# FIXME as of 7.5.0, clang 13.0.0, fails to build with clang
export CC=gcc
export CXX=g++
%cmake \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DUSE_TBB:BOOL=ON \
	-DUSE_VTK:BOOL=ON \
	-DINSTALL_VTK:BOOL=False \
	-D3RDPARTY_VTK_LIBRARY_DIR:PATH=%{_libdir} \
	-D3RDPARTY_VTK_INCLUDE_DIR:PATH=%{_includedir} \
	-D3RDPARTY_VTK_INCLUDE_DIR=%{_includedir}/vtk \
	-DINSTALL_DIR=%{buildroot}%{_prefix} \
	-DINSTALL_DIR_LIB=%{_lib} \
	-DINSTALL_DIR_CMAKE=%{_lib}/cmake/%{name} \
	-G Ninja
%ninja_build

%install
ninja install -C build

# Draw binary should not be versioned.
mv %{buildroot}%{_bindir}/DRAWEXE-%{version} \
   %{buildroot}%{_bindir}/DRAWEXE

# Remove buildroot references from the launcher script
sed -i -e 's,%{buildroot},,g' %{buildroot}%{_bindir}/env.sh

# And ignore release/debug/... build identifier, that's a Windoze thing
sed -i -e 's,\[ "$1" == "i" \],true,g' %{buildroot}%{_bindir}/custom_*.sh
cd %{buildroot}%{_bindir}
[ -e custom.sh ] || ln -s custom_*.sh custom.sh
