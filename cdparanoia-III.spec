# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	Utility to copy digital audio cd's
Name:		cdparanoia-III
Version:	10.2
Release:	13
Epoch:		1
License:	GPL
Group:		Applications/Sound
Source0:	http://downloads.xiph.org/releases/cdparanoia/%{name}-%{version}.src.tgz
# Source0-md5:	b304bbe8ab63373924a744eac9ebc652
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-gcc4.patch
URL:		http://www.xiph.org/paranoia/
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cdparanoia (Paranoia III) reads digital audio directly from a CD, then
writes the data to a file or pipe in WAV, AIFC or raw 16 bit linear
PCM format. Cdparanoia's strength lies in its ability to handle a
variety of hardware, including inexpensive drives prone to
misalignment, frame jitter and loss of streaming during atomic reads.
Cdparanoia is also good at reading and repairing data from damaged
CDs.

%package libs
Summary:	Libraries of CD Paranoia program
Group:		Libraries

%description libs
This package contains libraries of CD Paranoia program.

%package devel
Summary:	Header files for CD Paranoia libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
This package contains header files for CD Paranoia libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f %{_datadir}/automake/config.guess configure.guess
cp -f %{_datadir}/automake/config.sub configure.sub
%{__aclocal}
%{__autoconf}
%configure \
	--disable-static
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man1,%{_includedir}}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/cdparanoia
%{_mandir}/man?/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcdda_interface.so.0
%attr(755,root,root) %ghost %{_libdir}/libcdda_paranoia.so.0
%attr(755,root,root) %{_libdir}/libcdda_interface.so.*.*.*
%attr(755,root,root) %{_libdir}/libcdda_paranoia.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdda_interface.so
%attr(755,root,root) %{_libdir}/libcdda_paranoia.so
%{_includedir}/*.h

