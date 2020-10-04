#!/usr/bin/env python
#cvaSamplesGen
#Create random points, calculate viewsheds per random sample and patch the results into a file.
#Viewshed sizes in (n) number of points and (n) number of samples Generator ver. 1.0
#Israel Hinojosa Balino (UCL)
#This script use r.cva by Mark Lake (UCL)
#This script needs GRASS 6.4 to run and Python
#Run this script from command line

import os
import sys
grass_install_tree=os.getenv('GISBASE')
sys.path.append(grass_install_tree+os.sep+'etc'+os.sep+'python')
import grass.script as grass

raster=raw_input("Name of initial raster to calculate random points: ")

#check twice if name of DEM or DTM (raster file) exists, otherwise return error
filex=grass.find_file(raster, element='cell')
if not filex['fullname'] != '':
        raster=raw_input("Raster file with the name"+" "+"<"+ raster +">"+" "+"does not exist. Another try? : ")
filex=grass.find_file(raster, element='cell')
if not filex['fullname'] != '':
        raster=raw_input("Seriously"+" "+"<"+ raster +">"+" "+"does not exist. Please choose another name: ")
filex=grass.find_file(raster, element='cell')
if not filex['fullname'] != '':
        grass.fatal(_("You have to check your files before using this script. Bye!!!"))

file=raw_input("Name of the output vector file: ")

#check twice if name of previous output file exists, otherwise return error
filey=grass.find_file(file, element='vector')
if filey['fullname'] != '':
        file=raw_input("A file named"+" "+"<"+ file +">"+" "+"exists. Please choose another name: ")
filey=grass.find_file(file, element='vector')
if filey['fullname'] != '':
        file=raw_input("Seriously"+" "+"<"+ file +">"+" "+"exist. Please choose another name: ")
filey=grass.find_file(file, element='vector')
if filey['fullname'] != '':
        grass.fatal(_("You have to choose another name. Bye!"))

#customization
max=int(raw_input("Number of samples: ") )
maxR=int(raw_input("Number of random points: ") )
maxDist=int(raw_input("Maximum distance (in metres) from viewing point (refer to r.cva): ") )

#Create empty file, attach a table and add columns with the proper names and types
grass.run_command('v.edit', map=file, type='line', tool='create')
grass.run_command('v.db.addtable', map=file)
grass.run_command('v.db.addcol', map=file, columns="value DOUBLE PRECISION,vsize INT,sample INT")

#generate random points and calculate viewsheds
i=1
while i <= max:
        print i
        namerandom="randomV" +str(i)
        nameRandomCVA= "randomCVA"+str(i)
        sampleNo=i
        print 'Generating'+' '+'random'+' '+'numbers'+' '+'for'+' '+ namerandom
        i=i+1
        grass.run_command('r.random', overwrite='True', input=raster, vector_output=namerandom, n=maxR)
        print 'Calculating'+' '+'viewsheds'+' '+'for'+' '+ nameRandomCVA
        grass.run_command('r.cva', 'o', input=raster, output=nameRandomCVA, sites=namerandom, obs_elev='1.7', target_elev='0.0', max_dist=maxDist, seed='1', sample='10.0',type='sites',curvc='0.0' )

#Add column to attach Viewshed sizes and perform a spatial query to extract the values from raster to vector
        print 'Spatial'+' '+'query'+' '+'for'+' '+ nameRandomCVA
        grass.run_command('v.db.addcol', map=namerandom, layer='1', columns='vsize INT')
        grass.run_command('v.what.rast', vector=namerandom, raster=nameRandomCVA, layer='1', column='vsize')

#Add another column to attach the sample number
        print 'Adding'+' '+'column'+' '+'for'+' '+'sample'+' '+'numbers'+' '+'in'+' '+ namerandom
        grass.run_command('v.db.addcol', map=namerandom, layer='1', columns='sample INT')
        grass.run_command('v.db.update', map=namerandom, layer='1', column='sample', value=sampleNo)

#Append sample to pre-existing samples
        print 'Patching'+' '+'original'+' '+'vector'+' '+'with'+' '+ namerandom
        grass.run_command('v.patch', 'ae',overwrite='True', input=namerandom, output=file)

#Clean dataset from temporal files
        print 'Deleting'+' '+'supporting'+' '+'files'+' '+':'+' '+ namerandom +' '+'and'+' '+ nameRandomCVA
        grass.run_command('g.remove', vect=namerandom, rast=nameRandomCVA)
        print 'DONE!'

#export to ascii with coordinates
        print 'Generating ASCII file with headers and coordinates'
        grass.run_command('v.out.ascii', input=file, output='samples.txt', dp=10, columns='vsize,sample')
        print 'DONE!'
