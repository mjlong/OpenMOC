from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()

log.set_log_level('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../c5g7-materials.h5')

uo2_id = materials['UO2'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circles = []
planes = []
planes.append(XPlane(x=-2.0))
planes.append(XPlane(x=2.0))
planes.append(YPlane(y=-2.0))
planes.append(YPlane(y=2.0))
circles.append(Circle(x=0.0, y=0.0, radius=0.4))
circles.append(Circle(x=0.0, y=0.0, radius=0.3))
circles.append(Circle(x=0.0, y=0.0, radius=0.2))
for plane in planes: plane.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=water_id))
cells.append(CellBasic(universe=2, material=uo2_id))
cells.append(CellBasic(universe=2, material=water_id))
cells.append(CellBasic(universe=3, material=uo2_id))
cells.append(CellBasic(universe=3, material=water_id))
cells.append(CellFill(universe=5, universe_fill=4))
cells.append(CellFill(universe=0, universe_fill=6))

cells[0].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[0])
cells[2].addSurface(halfspace=-1, surface=circles[1])
cells[3].addSurface(halfspace=+1, surface=circles[1])
cells[4].addSurface(halfspace=-1, surface=circles[2])
cells[5].addSurface(halfspace=+1, surface=circles[2])

cells[7].addSurface(halfspace=+1, surface=planes[0])
cells[7].addSurface(halfspace=-1, surface=planes[1])
cells[7].addSurface(halfspace=+1, surface=planes[2])
cells[7].addSurface(halfspace=-1, surface=planes[3])


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating 16 x 16 lattice...')

# 2x2 assembly
assembly = Lattice(id=4, width_x=1.0, width_y=1.0)
assembly.setLatticeCells([[1, 2], [1, 3]])

# 2x2 core
core = Lattice(id=6, width_x=2.0, width_y=2.0)
core.setLatticeCells([[5, 5], [5, 5]])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
geometry.addLattice(assembly)
geometry.addLattice(core)

geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = ThreadPrivateSolver(geometry, track_generator)
solver.setNumThreads(num_threads)
solver.setSourceConvergenceThreshold(tolerance)
solver.convergeSource(max_iters)
solver.printTimerReport()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

#plotter.plot_tracks(track_generator)
#plotter.plot_segments(track_generator)
#plotter.plot_materials(geometry, gridsize=500)
#plotter.plot_cells(geometry, gridsize=500)
#plotter.plot_flat_source_regions(geometry, gridsize=500)
#plotter.plot_fluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
