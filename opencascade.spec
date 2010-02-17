%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

Name:		opencascade
Group:		Sciences/Physics
Version:	6.3
Release:	%mkrel 2
Summary:	3D modeling & numerical simulation
License:	LGPL with differences
URL:		http://www.opencascade.org/
Source0:	OpenCASCADE_src.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	GL-devel
BuildRequires:	X11-devel
BuildRequires:	bison flex
BuildRequires:	java-rpmbuild
BuildRequires:	qt4-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel

Requires:	pdksh
Requires:	tcl
Requires:	tix
Requires:	tk

Patch0:		underlink.patch
Patch1:		format.patch
Patch2:		tcl8.6.patch
Patch3:		open.patch
Patch4:		destdir.patch
Patch5:		environ.patch
Patch6:		for-user-test-build.patch

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

The platform is provided by the Company bearing the same name Open CASCADE S.A.
For its clients the Company offers custom development and technical support
services. For more information on the Company please visit www.opencascade.com

%files
%defattr(-,root,root)
%dir %{_usrsrc}/%{name}
%{_usrsrc}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*

#-----------------------------------------------------------------------
%package	-n %{libname}
Summary:	3D modeling & numerical simulation
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

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

The platform is provided by the Company bearing the same name Open CASCADE S.A.
For its clients the Company offers custom development and technical support
services. For more information on the Company please visit www.opencascade.com

%files		-n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

#-----------------------------------------------------------------------
%package	-n %{devname}
Summary:	3D modeling & numerical simulation
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
# Renamed from opencascade-devel to libopencascade-devel
# (but only in cooker, not in any official distro)
Obsoletes:	%{name}-devel < %{version}-%{release}

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

The platform is provided by the Company bearing the same name Open CASCADE S.A.
For its clients the Company offers custom development and technical support
services. For more information on the Company please visit www.opencascade.com

%files		-n %{devname}
%defattr(-,root,root)
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

#-----------------------------------------------------------------------
%prep
%setup -q -n OpenCASCADE6.3.0

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
pushd ros
    autoreconf -ifs
popd

#-----------------------------------------------------------------------
%build
pushd ros
    %configure --with-java-include=/usr/lib/jvm/java-rpmbuild/include
popd
%make

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
pushd ros
    %makeinstall_std
    find %{buildroot}%{_includedir}/%{name} -type f | xargs chmod -x
    mkdir -p %{buildroot}%{_datadir}/%{name}/data
    cp -f ../LICENSE  %{buildroot}%{_datadir}/%{name}
    cp -far ../data/{csfdb,iges,images,occ,step,stl,vrml} %{buildroot}%{_datadir}/%{name}/data
    cp -far ../samples %{buildroot}%{_datadir}/%{name}
    mkdir -p %{buildroot}%{_docdir}/%{name}
    cp -far ../doc/* %{buildroot}%{_docdir}/%{name}
    ln -sf %{_docdir}/%{name} %{buildroot}%{_datadir}/%{name}/doc
    find %{buildroot}%{_datadir}/%{name} -type f | xargs chmod -x
    find %{buildroot}%{_usrsrc}/%{name} -type f | xargs chmod -x
    chmod +x %{buildroot}%{_usrsrc}/%{name}/env_DRAW.sh
    chmod +x %{buildroot}%{_usrsrc}/%{name}/WOKsite/*.csh

    # adjust environment/directories to avoid (too much) script patching
    ln -sf %{_usrsrc}/%{name} %{buildroot}%{_datadir}/%{name}/src
    ln -sf %{_libdir} %{buildroot}%{_datadir}/%{name}/lib
    mkdir -p %{buildroot}%{_datadir}/%{name}/bin
    mv -f %{buildroot}%{_bindir}/* %{buildroot}%{_datadir}/%{name}/bin

    # install java
    #non functional, so, don't "force" install
    #mkdir -p %{buildroot}%{_usrsrc}/%{name}/jcas
    #install -m 644 src/jcas/* %{buildroot}%{_usrsrc}/%{name}/jcas
popd
