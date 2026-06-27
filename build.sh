#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/src"
BUILD="$ROOT/build"

mkdir -p "$SRC"
[ -d "$SRC/jigsaw" ] || git clone https://github.com/dengwirda/jigsaw.git "$SRC/jigsaw"
[ -d "$SRC/mkgrid" ] || git clone https://github.com/mgduda/mpas_jigsaw_tutorial.git "$SRC/mkgrid"

module load cmake

mkdir -p "$SRC/jigsaw/build"
cd "$SRC/jigsaw/build"
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$BUILD"
make -j 4 install

module --force purge
module load ncarenv/24.12
module load craype/2.7.31
module load gcc/12.4.0
module load ncarcompilers/1.0.0
module load cray-mpich/8.1.29
module load parallel-netcdf/1.14.0
module load netcdf/4.9.2

mkdir -p "$BUILD/bin"

cc "$SRC/mkgrid/mkgrid.c" -o "$BUILD/bin/mkgrid" \
  -I"$NCAR_INC_PARALLEL_NETCDF" \
  -L"$NCAR_LDFLAGS_PARALLEL_NETCDF" \
  -lpnetcdf -lm

echo "Done. Executables installed in: $BUILD/bin"