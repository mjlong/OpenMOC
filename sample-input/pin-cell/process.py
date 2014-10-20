import sys
import numpy

print 'dataset={}'
print 'dataset[\'Energy Groups\']=10'
print 'dataset[\'Materials\']={}'
print 'c5g7_dataset=dataset[\'Materials\']'

fuelname = sys.argv[1]
nfr = int(sys.argv[2])
modedata=numpy.loadtxt('10gmode.py',delimiter=',',comments='[',unpack=False);
fueldata=numpy.loadtxt(fuelname,delimiter=',',comments='[',unpack=False);
matname=[]
for i in range(nfr):
  matname.append('\'UO2'+str(i+1)+'\'')

  print 'c5g7_dataset['+matname[i]+']={}'
  
  print 'c5g7_dataset['+matname[i]+'][\'Total XS\']=['
  print ', '.join(map(str,fueldata[0+i*15]))
  print ']'
  
  print 'c5g7_dataset['+matname[i]+'][\'Absorption XS\']=['
  print ', '.join(map(str,fueldata[1+i*15]))
  print ']'
  
  ggxs = fueldata[2+i*15:12+i*15]
  print 'c5g7_dataset['+matname[i]+'][\'Scattering XS\']=['
  print ', '.join(map(str,ggxs.ravel()))
  print ']'
  
  print 'c5g7_dataset['+matname[i]+'][\'Fission XS\']=['
  print ', '.join(map(str,fueldata[12+i*15]))
  print ']'
  
  print 'c5g7_dataset['+matname[i]+'][\'Nu Fission XS\']=['
  print ', '.join(map(str,fueldata[13+i*15]))
  print ']'
  
  print 'c5g7_dataset['+matname[i]+'][\'Chi\']=['
  print ', '.join(map(str,fueldata[14+i*15]))
  print ']'



print 'c5g7_dataset[\'Water\']={}'

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



