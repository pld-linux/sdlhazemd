%define		file_version	%(echo %{version} | tr -d .)
Summary:	SDL fork of MAME
Summary(pl.UTF-8):	Emulator MAME wykorzystujący SDL
Name:		sdlhazemd
Version:	0.14a
Release:	1
License:	BSD-like
Group:		X11/Applications/Games
Source0:	http://rbelmont.mameworld.info/%{name}%{file_version}.zip
# Source0-md5:	a5eab921f2fcd4fb4d04b9dd7f0d9177
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-duplicate_options.patch
URL:		http://rbelmont.mameworld.info
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	zlib-devel
Suggests:	gmameui
Obsoletes:	sdlmame
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SDLHAZEMD is meant to be a replacement for the MIA xmame but has no
connection with it otherwise. It has been separately developed from
base MAME, the popular Multiple Arcade Machine Emulator that supports
hundreds of machine chipsets with thousands of games from back in the
70s till today.

%description -l pl.UTF-8
SDLHAZEMD ma być zamiennikiem dla MIA xmame, jednak nie ma z nim nic
wspólnego. Był on rozwijany odzielnie w oparciu o oryginalny emulator
MAME, obsługujący setki układów komputerowych z tysiącami gier od lat
70. po dziś dzień.

%prep
%setup -q -n %{name}%{file_version}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's/NAME = $(TARGET)/NAME = %{name}/' \
	-e 's/^BUILD_EXPAT/# &/' \
	-e 's/^BUILD_ZLIB/# &/' \
	makefile

%build
%{__make} \
%ifarch arm ppc ppc64 s390 s390x sparc sparcv9 sparc64
	BIGENDIAN=1 \
%endif
%ifarch %{x8664} alpha ia64 ppc64 s390x sparc64
	PTR64=1 \
%endif
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install sdlhazemd $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc SDLHAZEMD.txt docs/{config,license,mame,newvideo}.txt
%attr(755,root,root) %{_bindir}/sdlhazemd
