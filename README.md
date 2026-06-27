## A Simple JIGSAW-based Workflow for MPAS-Atmosphere

This repository accompanies the "Generating meshes for MPAS-Atmosphere" mini-tutorial, presented at the 2026 MPAS/WRF Users Workshop.

### Prerequisites

This repository includes a `build.sh` script that clones, builds, and installs everything you need (both JIGSAW and the `mkgrid` program). The module commands in the script are tailored for NCAR's Derecho system, so adjust them to match your environment if you are building elsewhere.

Running
```
./build.sh
```
will:

1. Clone the sources into a `src/` directory:
   - `src/jigsaw` &larr; [JIGSAW](https://github.com/dengwirda/jigsaw)
   - `src/mkgrid` &larr; [mpas_jigsaw_tutorial](https://github.com/mgduda/mpas_jigsaw_tutorial) (provides `mkgrid.c`)
2. Configure and build JIGSAW with CMake, installing it into a top-level `build/` directory (executables in `build/bin`, libraries in `build/lib`).
3. Compile the `mkgrid` program — which derives MPAS's required mesh geometry and connectivity information from the generating points and their triangulation — into `build/bin/mkgrid`.

`mkgrid` requires an MPI implementation (OpenMPI and MPICH are common options) plus the [PnetCDF library](https://parallel-netcdf.github.io/). On Derecho the `cc` compiler wrapper is used so that the MPI (cray-mpich) include/link flags PnetCDF depends on are added automatically; elsewhere you may need to compile with `mpicc` and point at your PnetCDF installation.

After the script finishes, both `jigsaw` and `mkgrid` will be available in `build/bin`. Add this directory to your `PATH` so the workflow steps below can find them:
```
export PATH="$PWD/build/bin:$PATH"
```

Additionally, you'll also need a Python environment with at least the `numpy` and `netCDF4` packages. If you don't already have a suitable environemnt, setting up a Python virtual environment may be an easiest:
```
python -m venv mpas_mesh
source mpas_mesh/bin/activate
pip install --upgrade pip
pip install numpy netCDF4
```

### Generating your first variable-resolution mesh with JIGSAW + MKGRID

Generating a variable-resolution mesh with a 12-km circular refinement region centered at 38 N, 95 W, relaxing to 60-km grid spacing over a distance of 1600 km is accomplished with the following steps.

1. Run the `create_hfun.py` script to generate an `HFUN.msh` file
2. Run `jigsaw`, specifying `MESH.jig` as its command-line argument, to produce a `MESH.msh` file
3. Run `convert_jigsaw.py` to produce `SaveVertices` and `SaveTriangles` files from the `MESH.msh` file
4. Run `create_density.py` to produce a `SaveDensity` file
5. Copy the `hfun.py` file to `SaveCode`
6. Run `mkgrid`, specifying `12000.0` as its command-line argument, to produce `grid.nc` and `graph.info` files
