%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%{name}-devel
%define docname	%{name}-doc

Name:		opencascade
Group:		Sciences/Physics
Version:	6.3
Release:	%mkrel 1
Summary:	3D modeling & numerical simulation
License:	LGPL with differences
URL:		http://www.opencascade.org/
Source0:	OpenCASCADE_src.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	GL-devel
BuildRequires:	X11-devel
BuildRequires:	java-rpmbuild
BuildRequires:	tcl-devel
BuildRequires:	tk-devel

Patch0:		underlink.patch
Patch1:		format.patch
Patch2:		tcl8.6.patch
Patch3:		open.patch
Patch4:		destdir.patch

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
%{_bindir}/*
%dir %{_usrsrc}/%{name}
%{_usrsrc}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

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
Requires:	lib%{name} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

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
%{_libdir}/lib*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

#-----------------------------------------------------------------------
%prep
%setup -q -n OpenCASCADE6.3.0/ros

%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p2
%patch4 -p2
autoreconf -ifs

#-----------------------------------------------------------------------
%build
%configure --with-java-include=/usr/lib/jvm/java-rpmbuild/include
%make

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
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
