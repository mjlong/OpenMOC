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
#track_spacing = options.getTrackSpacing()
#num_azim = options.getNumAzimAngles()
num_azim=64
track_spacing=0.01;
tolerance = 1.0E-6#options.getTolerance()
max_iters = 500#options.getMaxIterations()

log.set_log_level('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize(sys.argv[1])#../c5g7-materials.py')

uo2_id = materials['UO2'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circle = Circle(x=0.0, y=0.0, radius=0.4096)
circle1 = Circle(x=0.0, y=0.0, radius=0.4096/2)
scale=1
left = XPlane(x=-0.63*scale)
right = XPlane(x=0.63*scale)
top = YPlane(y=0.63*scale)
bottom = YPlane(y=-0.63*scale)
horizontal = YPlane(y=0.)
vertical   = XPlane(x=0.)

left.setBoundaryType(REFLECTIVE)
right.setBoundaryType(REFLECTIVE)
top.setBoundaryType(REFLECTIVE)
bottom.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []
#cells.append(CellBasic(universe=1, material=uo2_id,rings=1,sectors=4))
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=uo2_id))

cells.append(CellBasic(universe=1, material=water_id))
cells.append(CellFill(universe=0, universe_fill=2))

#fuel
cells[0].addSurface(halfspace=-1, surface=circle)   
cells[0].addSurface(halfspace=+1, surface=vertical)   
cells[0].addSurface(halfspace=+1, surface=horizontal)   

cells[1].addSurface(halfspace=-1, surface=circle)   
cells[1].addSurface(halfspace=-1, surface=vertical)   
cells[1].addSurface(halfspace=+1, surface=horizontal)   

cells[2].addSurface(halfspace=-1, surface=circle)   
cells[2].addSurface(halfspace=-1, surface=vertical)   
cells[2].addSurface(halfspace=-1, surface=horizontal)   

cells[3].addSurface(halfspace=-1, surface=circle)   
cells[3].addSurface(halfspace=+1, surface=vertical)   
cells[3].addSurface(halfspace=-1, surface=horizontal)   

nfr=4 #num of fuel region
#moderator
cells[nfr].addSurface(halfspace=+1, surface=circle)
#universe=0
cells[nfr+1].addSurface(halfspace=+1, surface=left)
cells[nfr+1].addSurface(halfspace=-1, surface=right)
cells[nfr+1].addSurface(halfspace=+1, surface=bottom)
cells[nfr+1].addSurface(halfspace=-1, surface=top)


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple pin cell lattice...')

lattice = Lattice(id=2, width_x=1.26*scale, width_y=1.26*scale)
lattice.setLatticeCells([[1]])


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
plotter.plot_cells(geometry, gridsize=500)
#plotter.plot_flat_source_regions(geometry, gridsize=500)
#plotter.plot_fluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
