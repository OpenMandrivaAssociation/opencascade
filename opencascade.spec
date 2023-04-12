#define _disable_ld_no_undefined 1

%define major	%(echo %{version} |cut -d. -f1)
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define occtag %(echo %version | tr . _)

# Enabe this in order to use git snapshot
%define _from_git 1

%if %_from_git
%define commit ffce0d66bbaafe3a95984d0e61804c201b9995d2
%define shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

%bcond_with	draco
%bcond_without	eigen
%bcond_without	freeimage
%bcond_without	freetype
%bcond_with	fffmpeg
%bcond_with	openvr
%bcond_without	rapidjson
%bcond_without	tbb
%bcond_without	tk
%bcond_without	vtk

Name:		opencascade
Group:		Sciences/Physics
Version:	7.7.1
Release:	1
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
Source0:	http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=%{commit};sf=tgz#/opencascade-%{version}.tar.gz
%else
Source0:	https://dev.opencascade.org/system/files/occt/OCC_%{version}_release/opencascade-%{version}.tgz
%endif
Patch2:		opencascade-7.6.0-set-env-correctly.patch
Patch3:		opencascade-cmake.patch
Patch4:		oce-7.5.0-clang.patch
Patch5:		opencascade-tbb.patch
# (upstream)
#Patch100:	opencascade-7.5.0-fix_tbb.patch
# (ROSA)
Patch101:	opencascade-vtk9.2.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires: 	ninja
BuildRequires:	bison
%if %{with rapidjson}
BuildRequires:  cmake(rapidjson)
%endif
BuildRequires:  cmake(Qt5)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5Xml)
BuildRequires:  cmake(Qt5Sql)
%if %{with vtk}
BuildRequires:  cmake(vtk)
%endif
%if %{with eigen}
BuildRequires:	eigen-devel
%endif
%if %{with ffmpeg}
BuildRequires:	ffmpeg-devel
%endif
BuildRequires:	flex
%if %{with freeimage}
BuildRequires:	freeimage-devel
%endif
BuildRequires:	hdf5-devel
BuildRequires:	mesa-common-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xmuu)
%if %{with freeimage}
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
%endif
BuildRequires:	pkgconfig(ftgl)
%if %{with tk}
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
%endif
%if %{with tbb}
BuildRequires:  pkgconfig(tbb)
%endif
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
# FIXME: BUILD_RELEASE_DISABLE_EXCEPTIONS=OFF is needed by FreeCAD
# https://github.com/FreeCAD/FreeCAD/issues/6200
%cmake -Wno-dev \
	-DCMAKE_VERBOSE_MAKEFILE:BOOL=OFF \
	-DBUILD_RELEASE_DISABLE_EXCEPTIONS:BOOL=OFF \
	-DUSE_DRACO:BOOL=%{?with_draco:ON}%{!?with_draco:OFF} \
	-DUSE_EIGEN:BOOL=%{?with_eigen:ON}%{!?with_eigen:OFF} \
	-DUSE_FREEIMAGE:BOOL=%{?with_freeimage:ON}%{!?with_freeimage:OFF} \
	-DUSE_FREETYPE:BOOL=%{?with_freetype:ON}%{!?with_freetype:OFF} \
	-DUSE_FFMPEG:BOOL=%{?with_ffmpeg:ON}%{!?with_ffmpeg:OFF} \
	-DUSE_OPENVR:BOOL=%{?with_openvr:ON}%{!?with_openvr:OFF} \
	-DUSE_RAPIDJSON:BOOL=%{?with_rapidjson:ON}%{!?with_rapidjson:OFF} \
	-DUSE_TBB:BOOL=%{?with_tbb:ON}%{!?with_tbb:OFF} \
	-DUSE_TK:BOOL=%{?with_tk:ON}%{!?with_tk:OFF} \
	-DUSE_VTK:BOOL=%{?with_vtk:ON}%{!?with_vtk:OFF} \
	-DINSTALL_VTK:BOOL=False \
	-D3RDPARTY_VTK_LIBRARY_DIR:PATH=%{_libdir} \
	-D3RDPARTY_VTK_INCLUDE_DIR:PATH=%{_includedir}/vtk \
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
