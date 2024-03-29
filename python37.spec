Name:           python37
Version:        3.7.12
Release:        24
License:        Python-2.0
Summary:        The Python Programming Language
Url:            http://www.python.org
Group:          devel/python
Source0:        https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tar.xz
Source1:        constcompat.patch
Patch1:         0001-Fix-python-path-for-linux.patch
Patch2:         0002-Skip-tests-TODO-fix-skips.patch
Patch3:         0003-Use-pybench-to-optimize-python.patch
Patch4:         0004-Add-avx2-and-avx512-support.patch
Patch5:         0005-Build-avx2-and-avx512-versions-of-the-math-library.patch
Patch6:         0006-Add-pybench-for-pgo-optimization.patch
Patch7:         0007-pythonrun.c-telemetry-patch.patch
Patch8:         0008-test_socket.py-remove-testPeek-test.test_socket.RDST.patch

BuildRequires:  bzip2
BuildRequires:  db
BuildRequires:  grep
BuildRequires:  bzip2-dev
BuildRequires:  xz-dev
BuildRequires:  gdbm-dev
BuildRequires:  readline-dev
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  sqlite-autoconf
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  ncurses-dev
BuildRequires:  expat-dev
BuildRequires:  libffi-dev
BuildRequires:  procps-ng-bin
BuildRequires:  netbase
BuildRequires:  pip
BuildRequires:  pkgconfig(libnsl)
Requires: python37-core
Requires: python37-lib
Requires: usrbinpython

%define keepstatic 1
%global __arch_install_post %{nil}

%description
The Python Programming Language.

%package lib
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description lib
The Python Programming Language.
%package staticdev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description staticdev
The Python Programming Language.

%package core
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python
Requires:       setuptools-python3
Requires:       setuptools-bin

%description core
The Python Programming Language.

%package dev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel
Requires:       python37-lib
Requires:       python37-core
Requires:       usrbinpython

%description dev
The Python Programming Language.

%prep
%setup -q -n Python-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

pushd ..
cp -a Python-%{version} Python-avx2
cd Python-avx2
popd

%build
%define python_configure_flags  --with-threads --with-pymalloc  --without-cxx-main --with-signal-module --enable-ipv6=yes  --libdir=/usr/lib  ac_cv_header_bluetooth_bluetooth_h=no  ac_cv_header_bluetooth_h=no  --with-system-ffi --with-system-expat --with-lto=8 --with-computed-gotos

export LANG=C.UTF-8
export CFLAGS="$CFLAGS -O3"
%configure %python_configure_flags --enable-shared
make %{?_smp_mflags}

pushd ../Python-avx2
export CFLAGS="$CFLAGS -march=haswell -mfma  "
export CXXFLAGS="$CXXFLAGS -march=haswell -mfma"
%configure %python_configure_flags --enable-shared --bindir=/usr/bin/haswell
make %{?_smp_mflags}
popd

%install

pushd ../Python-avx2
%make_install
mkdir -p %{buildroot}/usr/lib64/haswell
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/haswell/
rm -rf %{buildroot}/usr/lib/*
rm -rf %{buildroot}/usr/bin/*
popd


%make_install
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/

# --enable-optimizations does not work with --enable-shared
# https://bugs.python.org/issue29712
pushd ../Python-avx2
make clean
%configure %python_configure_flags --enable-optimizations
make profile-opt %{?_smp_mflags}
popd

make clean
%configure %python_configure_flags --enable-optimizations
make profile-opt %{?_smp_mflags}
%make_install
# static library archives need to be writable for strip to work
install -m 0755 %{buildroot}/usr/lib/libpython3.7m.a %{buildroot}/usr/lib64/
rm -f %{buildroot}/usr/lib/libpython3.7m.a
pushd %{buildroot}/usr/include/python3.7m
cat %{SOURCE1} | patch -p0
popd

#check
#export LANG=C
#LD_LIBRARY_PATH=`pwd` ./python -Wd -E -tt  Lib/test/regrtest.py -v -x test_asyncio test_uuid test_subprocess || :


%files

%files lib
/usr/lib64/haswell/libpython3.7m.so.1.0
/usr/lib64/libpython3.7m.so.1.0

%files staticdev
/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu/libpython3.7m.a
/usr/lib64/libpython3.7m.a

%files core
%exclude /usr/bin/2to3
/usr/bin/2to3-3.7
%exclude /usr/bin/pip3
%exclude /usr/bin/easy_install-3.7
%exclude /usr/bin/pip3.7
%exclude /usr/bin/idle3
%exclude /usr/bin/idle3.7
%exclude /usr/bin/pydoc3
/usr/bin/pydoc3.7
%exclude /usr/bin/python3
%exclude /usr/bin/python3-config
/usr/bin/python3.7
/usr/bin/python3.7-config
/usr/bin/python3.7m
/usr/bin/python3.7m-config
%exclude /usr/bin/pyvenv
/usr/bin/pyvenv-3.7
/usr/lib/python3.7
%exclude /usr/lib/python3.7/config-3.7m-x86_64-linux-gnu/libpython3.7m.a
%exclude /usr/lib/python3.7/distutils/command/*.exe
%exclude /usr/lib/python3.7/test/
%exclude /usr/lib/python3.7/tkinter
%exclude /usr/lib/python3.7/ensurepip/_bundled/pip-*-py2.py3-none-any.whl
%exclude /usr/share/man/

%files dev
/usr/include/python3.7m/*.h
/usr/include/python3.7m/internal/*.h
/usr/lib64/haswell/libpython3.7m.so
/usr/lib64/libpython3.7m.so
%exclude /usr/lib64/libpython3.so
/usr/lib64/pkgconfig/python-3.7.pc
/usr/lib64/pkgconfig/python-3.7m.pc
%exclude /usr/lib64/pkgconfig/python3.pc
