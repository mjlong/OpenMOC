from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options
import sys



###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
num_azim=int(sys.argv[4])
track_spacing=float(sys.argv[5]);
tolerance = 1.0E-6#options.getTolerance()
max_iters = 500#options.getMaxIterations()

log.set_log_level('NORMAL')

xsname = sys.argv[1]

###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize(xsname)

uo2_id = materials['UO21'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circle = Circle(x=0.0, y=0.0, radius=0.4096)
left = XPlane(x=-1.26)
right = XPlane(x=1.26)
top = YPlane(y=1.26)
bottom = YPlane(y=-1.26)

left.setBoundaryType(REFLECTIVE)
right.setBoundaryType(REFLECTIVE)
top.setBoundaryType(REFLECTIVE)
bottom.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []
cells.append(CellBasic(universe=1, material=uo2_id,rings=int(sys.argv[2]), sectors=int(sys.argv[3])))
cells.append(CellBasic(universe=1, material=water_id))

cells.append(CellBasic(universe=2, material=water_id))
cells.append(CellBasic(universe=2, material=water_id))

cells.append(CellFill(universe=0, universe_fill=3))

cells[0].addSurface(halfspace=-1, surface=circle)
cells[1].addSurface(halfspace=+1, surface=circle)
cells[2].addSurface(halfspace=-1, surface=circle)
cells[3].addSurface(halfspace=+1, surface=circle)

cells[4].addSurface(halfspace=+1, surface=left)
cells[4].addSurface(halfspace=-1, surface=right)
cells[4].addSurface(halfspace=+1, surface=bottom)
cells[4].addSurface(halfspace=-1, surface=top)


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple pin cell lattice...')

lattice = Lattice(id=3, width_x=1.26, width_y=1.26)
lattice.setLatticeCells([[1,1],[2,1]])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
geometry.addLattice(lattice)

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

solver = CPUSolver(geometry, track_generator)
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
plotter.plot_fluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7,8,9,10])

log.py_printf('TITLE', 'Finished')

