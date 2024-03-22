#!/usr/bin/env python3
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
# raw_input() deprecated now in python 3

### version 0.2 for grass 8 (tested on 8.3)
### standalone version. Please modify you GRASS data settings!
### also notice that you might need to change your PATHs.
### the environs.bat file is needed! Also take a look on it
 
import os
import sys
import subprocess
from pathlib import Path

# define GRASS data settings (adapt to your needs)
gisdb = Path(r'D:\Documentos\Archivo_GRASS_R')
location = "ciudadDeMexico"
mapset = "pm25"


# path to the GRASS GIS launch script
# we assume that the GRASS GIS start script is available and on PATH
# query GRASS itself for its GISBASE
# (with fixes for specific platforms)
# needs to be edited by the user
executable = "grass"
if sys.platform.startswith("win"):
    # MS Windows
    #executable = r"C:\Program Files\AppJ\QGIS 3.28.14\bin\grass83.bat"
    # uncomment when using standalone WinGRASS installer
    executable = r'C:\Program Files\AppJ\QGIS 3.28.14\bin\grass83.bat'
    # this can be skipped if GRASS executable is added to PATH
elif sys.platform == "darwin":
    # Mac OS X
    version = "8.3"
    executable = f"/Applications/GRASS-{version}.app/Contents/Resources/bin/grass"

# query GRASS GIS itself for its Python package path
grass_cmd = [executable, "--config", "python_path"]
process = subprocess.run(grass_cmd, check=True, text=True, stdout=subprocess.PIPE)

# define GRASS-Python environment
sys.path.append(process.stdout.strip())
#
qgis_folder = Path(r'C:\Program Files\AppJ\QGIS 3.28.14')
# define bin path QGIS
qgis_dlls = os.path.join(qgis_folder, "bin")
sys.path.append(qgis_dlls)

# import (some) GRASS Python bindings
import grass.script as gs
import grass.script.setup as gsetup

# launch session
session = gs.setup.init(gisdb, location, mapset)

# example calls
gs.message("Current GRASS GIS 8 environment:")
print(gs.gisenv())

# gs.message("Available raster maps:")
# for rast in gs.list_strings(type="raster"):
#      print(rast)

# # gs.message("Available vector maps:")
# # for vect in gs.list_strings(type="vector"):
# #     print(vect)

rasterWind=input("Name of wind map: ")

#check twice if name of DEM or DTM (raster file) exists, otherwise return error
filex=gs.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        rasterWind=input("Raster file with the name"+" "+"<"+ rasterWind +">"+" "+"does not exist. Another try? : ")
filex=gs.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        rasterWind=input("Seriously"+" "+"<"+ rasterWind +">"+" "+"does not exist. Please choose another name: ")
filex=gs.find_file(rasterWind, element='cell')
if not filex['fullname'] != '':
        gs.fatal(_("You have to check your files before using this script. Bye!!!"))

rasterAspect=input("Name of aspect map: ")
 
#check twice if name of DEM or DTM (raster file) exists, otherwise return error
filey=gs.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        rasterAspect=input("Raster file with the name"+" "+"<"+ rasterAspect +">"+" "+"does not exist. Another try? : ")
filey=gs.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        rasterAspect=input("Seriously"+" "+"<"+ rasterAspect +">"+" "+"does not exist. Please choose another name: ")
filey=gs.find_file(rasterAspect, element='cell')
if not filey['fullname'] != '':
        gs.fatal(_("You have to check your files before using this script. Bye!!!"))

#Reclassify Aspect map
rFileA = r"rFileAspect.txt"
reclassA="rasterAspect_reclass"
print ('Reclassifiying'+' '+ rasterAspect +' '+'map'+' '+'into'+' '+'8'+' '+'regions')
gs.run_command('r.reclass', overwrite=True, input=rasterAspect, output=reclassA, rules=rFileA)
 
#Reclassify Wind map
rFileW = r"rFileWind.txt"
reclassW="rasterWind_reclass"
print ('Reclassifiying'+' '+ rasterWind +' '+'map'+' '+'into'+' '+'8'+' '+'regions')
gs.run_command('r.reclass', overwrite=True, input=rasterWind, output=reclassW, rules=rFileW)
 
#Both maps are mixed with a simple sum
print ('Adding'+' '+ rasterWind +' '+'to'+' '+ rasterAspect)
output="WindPLUSAspect"
gs.mapcalc("$output = $reclassW + $reclassA", overwrite=True, output=output, reclassW=reclassW, reclassA=reclassA)
 
#Reclassify new map with specific rules of azimuth contraposition
rFileVS = r"rFileVS.txt"
windVSaspect="windVSaspect_reclass"
print ('Reclassifiying'+' '+ output +' '+'map'+' '+'into'+' '+'3'+' '+'categories')
gs.run_command('r.reclass', overwrite=True, input=output, output=windVSaspect, rules=rFileVS)
print ('DONE!')

# verify result
print ('Verifying resuls with r.category...')
print ('\n',r'New map has the following categories>','\n')
gs.run_command('r.category', map="windVSaspect_reclass")

# clean up at the end
session.finish()
