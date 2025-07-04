# -*- coding: utf-8 -*-
"""
Created on Fri May 20 17:00:01 2022

@author: Deh
"""

import os;
import matplotlib.pyplot as plt;
import sys;
import re;
import numpy as np;

from osgeo import ogr;
from osgeo import osr;
from osgeo import gdal;
from osgeo import gdalconst;
import pyproj;
import geopandas
# import tifffile as tiff

shapefilename = r'..\Grade de 1 hectare por bloco (54 blocos).shp';
shapefile_semicircle = 'semicircle.shp';
shapefile_pilots = 'pilot.shp';
shapefile_grid = 'grid.shp';
shapefile_gridcenter = 'grid_center_pts.shp';

#Get Spatial Reference of GeoTiff image
imgdir = r'H:\Agrientech\Embrapa-Cotton\Indices1';
imgfilename = os.path.join(imgdir,'GLI.tif');
gdal_ds = gdal.Open(imgfilename);
proj = gdal_ds.GetProjectionRef();
sR = gdal_ds.GetSpatialRef();
ulx, xres, xskew, uly, yskew, yres = gdal_ds.GetGeoTransform();
gdal_ds = None;

# gg = ogr.Open(shapefilename,1)
# layer = gg.GetLayerByIndex(0);
# Loop over all features
# for feature in layer:
#     val = feature.GetField('FID');
#     break;

#Get Shapfile Driver
driver = ogr.GetDriverByName("ESRI Shapefile");


#Create Semicircle Shapefile
outds = driver.CreateDataSource(shapefile_semicircle);
layer_semicircle = outds.CreateLayer(shapefile_semicircle.replace('.shp',''), sR);
semicircle = ogr.Geometry(ogr.wkbLinearRing);
semicircle_pts = np.genfromtxt('semicircle.txt', delimiter='\t');
for i in range(semicircle_pts.shape[0]):
    semicircle.AddPoint_2D(semicircle_pts[i,0], semicircle_pts[i,1]);
poly = ogr.Geometry(ogr.wkbPolygon);
poly.AddGeometry(semicircle);
poly.CloseRings();
feature = ogr.Feature(layer_semicircle.GetLayerDefn());
feature.SetGeometry(poly);
layer_semicircle.CreateFeature(feature);
layer_semicircle.SyncToDisk();
feature = None;
layer_semicircle = None;
outds = None;
del semicircle_pts;

#Create Pilots
outds = driver.CreateDataSource(shapefile_pilots);
layer_Pilot = outds.CreateLayer(shapefile_semicircle.replace('.shp',''), sR);
field_id = ogr.FieldDefn('FID', ogr.OFTInteger);
layer_Pilot.CreateField(field_id);

#Piloto 1
pilot1 = ogr.Geometry(ogr.wkbLinearRing);
pilot1_pts = np.genfromtxt('piloto1.txt', delimiter='\t');
for i in range(pilot1_pts.shape[0]):
    pilot1.AddPoint_2D(pilot1_pts[i,0], pilot1_pts[i,1]);
pilot1poly = ogr.Geometry(ogr.wkbPolygon);
pilot1poly.AddGeometry(pilot1);
pilot1poly.CloseRings();
feature = ogr.Feature(layer_Pilot.GetLayerDefn());
feature.SetGeometry(pilot1poly);
feature.SetField('FID',1);
layer_Pilot.CreateFeature(feature);
layer_Pilot.SyncToDisk()
feature = None;

#Piloto 2
pilot2 = ogr.Geometry(ogr.wkbLinearRing);
pilot2_pts = np.genfromtxt('piloto2.txt', delimiter='\t');
for i in range(pilot2_pts.shape[0]):
    pilot2.AddPoint_2D(pilot2_pts[i,0], pilot2_pts[i,1]);
pilot2poly = ogr.Geometry(ogr.wkbPolygon);
pilot2poly.AddGeometry(pilot2);
pilot2poly.CloseRings();

feature = ogr.Feature(layer_Pilot.GetLayerDefn());
feature.SetGeometry(pilot2poly);
feature.SetField('FID',2);
layer_Pilot.CreateFeature(feature);
layer_Pilot.SyncToDisk()
feature = None;
layer_Pilot = None;
outds = None;
del pilot1_pts;
del pilot2_pts;

#Create Grid and Center Blocks
outds = driver.CreateDataSource(shapefile_grid);
layer_grid = outds.CreateLayer(shapefile_grid.replace('.shp',''), sR);

outds0 = driver.CreateDataSource(shapefile_gridcenter);
layer_gridcenter = outds0.CreateLayer(shapefile_gridcenter.replace('.shp',''), sR);

field_id = ogr.FieldDefn('FID', ogr.OFTInteger);
layer_grid.CreateField(field_id);
layer_gridcenter.CreateField(field_id);

# gg = ogr.Open(shapefilename)
# layer = gg.GetLayerByIndex(0);
grid_pts = np.genfromtxt('grid.txt', delimiter='\t');

blockID = 1;
for i in range(0,int(grid_pts.shape[0]),4):
    poly = grid_pts[i:(i+4)];
    block_pts = ogr.Geometry(ogr.wkbLinearRing);
    # block = feat.geometry();
    for k in range(poly.shape[0]):
        block_pts.AddPoint_2D(poly[k,0],poly[k,1]);
    block_poly = ogr.Geometry(ogr.wkbPolygon);
    block_poly.AddGeometry(block_pts);
    block_poly.CloseRings();
    center_block = block_poly.Centroid();
    
    feature0 = ogr.Feature(layer_gridcenter.GetLayerDefn());
    feature0.SetGeometry(center_block);
    feature0.SetField('FID',blockID);
    layer_gridcenter.CreateFeature(feature0);
    
    # ring = poly.GetGeometryRef(0);
    # for i in range(ring.GetPointCount()-1):
    #     block_pts.AddPoint_2D(ring.GetX(i),ring.GetY(i));
        
    feature1 = ogr.Feature(layer_grid.GetLayerDefn());
    feature1.SetGeometry(block_poly);
    feature1.SetField('FID',blockID);
    layer_grid.CreateFeature(feature1);
    
    blockID  = blockID + 1;
    feature0.Destroy()
    feature1.Destroy();
    feature1 = None;
    feature0 = None;
    
# gg = None;
layer_grid.SyncToDisk()
layer_grid = None;
layer_gridcenter.SyncToDisk()
layer_gridcenter = None;
outds = None;
outds0 = None;
 
# import geopandas as gp
# from pyproj import CRS
# # 1) Open Shapefile
# shp = gp.read_file(shapefile_grid);
# print(shp.shape);
# print(shp.head());
# # 2) Convert LAt/Lon to UTM zone
# # crs = CRS.from_string('+proj=utm +zone=21 +south');
# # shp.to_crs(crs,inplace=True);
# # print(shp.head());
# # 3) Plot Shapefile
# shp.plot();
# # 4) Write Shapefile
# # shp.to_file('PONTOS_CONVERTIDOS.shp');