%define gittag	ga384024
%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

# based on opencascade 6.5.1
%define occtag	6.5.1

# tpaviot-oce version 0.7.0
%define ocegit	0.7.0

Name:		opencascade
Group:		Sciences/Physics
Epoch:		0
Version:	%{occtag}.%{ocegit}
Release:	1
Summary:	3D modeling & numerical simulation
License:	LGPL with differences
URL:		https://github.com/tpaviot/oce
# https://github.com/tpaviot/oce/tarball/OCE-0.7.0
Source0:	tpaviot-oce-OCE-0.7.0-0-ga384024.tar.gz
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(x11)
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
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/%{name}
%{_datadir}/cmake/Modules/*.cmake

#-----------------------------------------------------------------------
%prep
%setup -qn tpaviot-oce-a384024

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
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
perl -pi -e 's|/usr//usr|/usr|;' build/env.sh build/env.csh
%makeinstall_std -C build

# adjust environment/directories to avoid (too much) script patching
ln -sf %{_libdir} %{buildroot}%{_datadir}/%{name}/lib
ln -sf %{_includedir}/%{name} %{buildroot}%{_datadir}/%{name}/inc
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/lin
ln -sf %{_datadir}/%{name} %{buildroot}%{_datadir}/%{name}/Linux


%changelog
* Thu Nov 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 0:6.5.1.0.7.0-1
+ Revision: 731433
- Update to newest release.

  + Funda Wang <fwang@mandriva.org>
    - fix requires on epoch
    - update file list
    - add more br
    - turn to community edition

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 6.3-7mdv2011.0
+ Revision: 613531
- rebuild

* Sat Mar 20 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-6mdv2010.1
+ Revision: 525364
+ rebuild (emptylog)

* Tue Feb 23 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-5mdv2010.1
+ Revision: 510407
+ rebuild (emptylog)

* Fri Feb 19 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-4mdv2010.1
+ Revision: 508427
+ rebuild (emptylog)

* Thu Feb 18 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-3mdv2010.1
+ Revision: 507809
+ rebuild (emptylog)

* Wed Feb 17 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-2mdv2010.1
+ Revision: 507303
+ rebuild (emptylog)

* Thu Feb 11 2010 Paulo Andrade <pcpa@mandriva.com.br> 6.3-1mdv2010.1
+ Revision: 504363
- Import opencascade 6.3.
- opencascade

