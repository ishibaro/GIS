#!/usr/bin/env python
# coding: utf-8
#This script needs GRASS 6.4 to run and Python
#Run this script from command line
 
############################################################################
#
# MODULE:           Wind Direction versus Aspect Surface Generator
#                   version beta 15 febrero 2014
# AUTHOR(S):        Israel Hinojosa Baliño  
#                   AntropoSIG CIESAS
# PURPOSE:      Create a raster file to detect the incidence of wind (wind direction) over an specific surface (aspect)
#               This tool detects leewards and windwards over a surface
#               Crea un archivo raster para detectar la incidencia de viento (dirección del viento) sobre una
#               superficie determinada (aspecto). Esta herramienta detecta los sotavento y barloventos en una superficie
# ACKNOWLEDGEMENTS: Maite Vallejo Allende. (Instituto Nacional de Cardiología, Ignacio Chávez, México) 
# COPYRIGHT:        (C) 2014 by AntropoSIG - CIESAS & Israel Hinojosa Baliño
#                   This program is free software under the GNU General 
#                   Public License (>=v2). Read the file COPYING that 
#                   comes with GRASS for details.
#
#############################################################################
#
# DESCRIPTION    Esta herramienta detecta los sotaventos y barloventos en una superficie
#                This tool detects leewards and windwards over a surface
#                0 Wind runs in the same direction of surface (leeward)
#                0 equivale a que la cara de la superficie apunta la misma dirección del viento (sotavento).
#                1 significa que el ángulo de incidencia del viento con respecto a la cara es paralelo.
#                1 the angle of incidence of the wind according to the surface is paralel
#                2 quiere decir que el viento incide en la cara en ángulos de entre 30 y 60°, o sea oblicuamente.
#                2 wind impacts on the surface in angles between 30 and 60 degrees, that is obliquely
#                3 significa que el ángulo de incidencia del viento contra
#               la pared es alrededor de 90°, osea, perpendicularmente (barlovento)
#                3 wind impacts on the surface in angles close to 90 or 90 degrees,
#                that is perpendicularly (winward).
#
#
 
import os
import sys
grass_install_tree=os.getenv('GISBASE')
sys.path.append(grass_install_tree+os.sep+'etc'+os.sep+'python')
import grass.script as grass
 
 
rasterWind=raw_input("Name of wind map: ")
 
#check twice if name of DEM or DTM (raster file) exists, otherwise return error
filex=grass.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        rasterWind=raw_input("Raster file with the name"+" "+"<"+ rasterWind +">"+" "+"does not exist. Another try? : ")
filex=grass.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        rasterWind=raw_input("Seriously"+" "+"<"+ rasterWind +">"+" "+"does not exist. Please choose another name: ")
filex=grass.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        grass.fatal(_("You have to check your files before using this script. Bye!!!"))
 
rasterAspect=raw_input("Name of aspect map: ")
 
#check twice if name of DEM or DTM (raster file) exists, otherwise return error
filey=grass.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        rasterAspect=raw_input("Raster file with the name"+" "+"<"+ rasterAspect +">"+" "+"does not exist. Another try? : ")
filey=grass.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        rasterAspect=raw_input("Seriously"+" "+"<"+ rasterAspect +">"+" "+"does not exist. Please choose another name: ")
filey=grass.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        grass.fatal(_("You have to check your files before using this script. Bye!!!"))
 
 
#Reclassify Aspect map
rFileA = r"reclassFileA"
reclassA="rasterAspect_reclass"
print 'Reclassifiying'+' '+ rasterAspect +' '+'map'+' '+'into'+' '+'8'+' '+'regions'
grass.run_command('r.reclass', overwrite=True, input=rasterAspect, output=reclassA, rules=rFileA)
 
#Reclassify Wind map
rFileW = r"reclassFileW"
reclassW="rasterWind_reclass"
print 'Reclassifiying'+' '+ rasterWind +' '+'map'+' '+'into'+' '+'8'+' '+'regions'
grass.run_command('r.reclass', overwrite=True, input=rasterWind, output=reclassW, rules=rFileW)
 
#Both maps are mixed with a simple sum
print 'Adding'+' '+ rasterWind +' '+'to'+' '+ rasterAspect
output="WindPLUSAspect"
grass.mapcalc("$output = $reclassW + $reclassA", output=output, reclassW=reclassW, reclassA=reclassA)
 
#Reclassify new map with specific rules of azimuth contraposition
rFileVS = r"reclassFileVS"
windVSaspect="windVSaspect_reclass"
print 'Reclassifiying'+' '+ output +' '+'map'+' '+'into'+' '+'3'+' '+'categories'
grass.run_command('r.reclass', overwrite=True, input=output, output=windVSaspect, rules=rFileVS)
print 'DONE!'
