import sys
import numpy
fuelname = sys.argv[1]
modedata=numpy.loadtxt('10gmode.py',delimiter=',',comments='[',unpack=False);
fueldata=numpy.loadtxt(fuelname,delimiter=',',comments='[',unpack=False);
print 'dataset={}'
print 'dataset[\'Energy Groups\']=10'
print 'dataset[\'Materials\']={}'
print 'c5g7_dataset=dataset[\'Materials\']'
print 'c5g7_dataset[\'UO2\']={}'
print 'c5g7_dataset[\'Water\']={}'

print 'c5g7_dataset[\'UO2\'][\'Total XS\']=['
print ', '.join(map(str,fueldata[0]))
print ']'

print 'c5g7_dataset[\'UO2\'][\'Absorption XS\']=['
print ', '.join(map(str,fueldata[1]))
print ']'

ggxs = fueldata[2:12]
print 'c5g7_dataset[\'UO2\'][\'Scattering XS\']=['
print ', '.join(map(str,ggxs.ravel()))
print ']'

print 'c5g7_dataset[\'UO2\'][\'Fission XS\']=['
print ', '.join(map(str,fueldata[12]))
print ']'

print 'c5g7_dataset[\'UO2\'][\'Nu Fission XS\']=['
print ', '.join(map(str,fueldata[13]))
print ']'

print 'c5g7_dataset[\'UO2\'][\'Chi\']=['
print ', '.join(map(str,fueldata[14]))
print ']'



print 'c5g7_dataset[\'Water\'][\'Total XS\']=['
print ', '.join(map(str,modedata[0]))
print ']'

print 'c5g7_dataset[\'Water\'][\'Absorption XS\']=['
print ', '.join(map(str,modedata[1]))
print ']'

ggxs = modedata[2:12]
print 'c5g7_dataset[\'Water\'][\'Scattering XS\']=['
print ', '.join(map(str,ggxs.ravel()))
print ']'

print 'c5g7_dataset[\'Water\'][\'Fission XS\']=['
print ', '.join(map(str,modedata[12]))
print ']'

print 'c5g7_dataset[\'Water\'][\'Nu Fission XS\']=['
print ', '.join(map(str,modedata[13]))
print ']'

print 'c5g7_dataset[\'Water\'][\'Chi\']=['
print ', '.join(map(str,modedata[14]))
print ']'



