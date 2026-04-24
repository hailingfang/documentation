Build GNU Toolchain on Linux
==========================================

Objective:

To build GNU toolchain on an old Linux system.

The Conponents of GNU toolchain refered in this article:

Binutilty()


.. code:: shell
    
    #step 0

    export TARGET=aarch64-linux-gnu
    export PREFIX=$HOME/gnu-toolchain
    export SYSROOT=$PREFIX/$TARGET
    export PATH=$PREFIX/bin:$PATH

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

    
