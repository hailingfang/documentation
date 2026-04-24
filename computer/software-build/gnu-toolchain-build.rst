Build GNU Toolchain on Linux
==========================================

Objective:

To build GNU toolchain on an old Linux system.

The Conponents of GNU toolchain refered in this article:


.. code:: shell
    
    #step 0
    export TARGET=aarch64-linux-gnu
    export PREFIX=$HOME/gnu-toolchain
    export SYSROOT=$PREFIX/$TARGET
    export PATH=$PREFIX/bin:$PATH
    mkdir $SYSROOT
    cd $SYSROOT
    mkdir -p usr/include usr/lib usr/bin
    ln -s usr/lib usr/lib64
    ln -s usr/* .
    cd -

    #step 1
    wget https://ftp.gnu.org/gnu/binutils/binutils-2.42.tar.xz
    tar xf binutils-2.42.tar.xz
    mkdir build-binutils && cd build-binutils

    ../binutils-2.42/configure \
      --target=$TARGET \
      --prefix=$PREFIX \
      --with-sysroot=$SYSROOT \
      --disable-nls \
      --disable-werror \
      --disable-multilib

    make -j$(nproc)
    make install
    cd ..

    #step 2
    wget https://ftp.gnu.org/gnu/gcc/gcc-13.3.0/gcc-13.3.0.tar.xz
    tar xf gcc-13.3.0.tar.xz
    cd gcc-13.3.0
    ./contrib/download_prerequisites
    cd ..
    mkdir build-gcc-stage1 && cd build-gcc-stage1

    ../gcc-13.3.0/configure \
    --with-pkgversion=fhl-build \
    --target=$TARGET \
    --prefix=$PREFIX \
    --with-sysroot=$SYSROOT \
    --with-build-sysroot=$SYSROOT \
    --with-native-system-header-dir=/usr/include \
    --disable-nls \
    --disable-multilib \
    --enable-languages=c \
    --without-headers

    make all-gcc -j$(nproc)
    make install-gcc
    cd ..

    #step 3
    wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.10.50.tar.xz
    tar xf linux-3.10.50.tar.xz
    cd linux-3.10.50
    make ARCH=arm64 INSTALL_HDR_PATH=$SYSROOT/usr headers_install
    cd ..

    #step 4
    wget https://ftp.gnu.org/gnu/glibc/glibc-2.39.tar.xz
    tar xf glibc/glibc-2.39.tar.xz
    mkdir build-glibc && cd build-glibc
    ../glibc-2.39/configure \
    --host=$TARGET \
    --prefix=/usr \
    --with-headers=$SYSROOT/usr/include \
    --disable-multilib

    make install-bootstrap-headers=yes install-headers DESTDIR=$SYSROOT

    make -j$(nproc) csu/subdir_lib
    install csu/crt1.o csu/crti.o csu/crtn.o $SYSROOT/usr/lib
    $TARGET-gcc -nostdlib -nostartfiles -shared -x c /dev/null -o $SYSROOT/usr/lib/libc.so
    touch $SYSROOT/usr/include/gnu/stubs.h
    cd ..

    #step 5
    cd build-gcc-stage1
    make all-target-libgcc -j$(nproc)
    make install-target-libgcc
    cd ..

    #step 6
    cd build-glibc
    make -j$(nproc)
    make install DESTDIR=$SYSROOT
    cd ..

    #step 7
    mkdir build-gcc-final && cd build-gcc-final

    ../gcc-13.3.0/configure \
    --target=$TARGET \
    --prefix=$PREFIX \
    --with-sysroot=$SYSROOT \
    --with-build-sysroot=$SYSROOT \
    --with-native-system-header-dir=/usr/include \
    --disable-nls \
    --disable-multilib \
    --enable-languages=c,c++

    make -j$(nproc)
    make install
    cd ..