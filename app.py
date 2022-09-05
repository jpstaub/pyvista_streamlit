# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 20:16:24 2022

@author: admin

https://discuss.streamlit.io/t/include-an-existing-html-file-in-streamlit-app/5655/3
"""

import streamlit as st
import streamlit.components.v1 as components

# generate: python modules to generate html file for display
import pyvista as pv
from pyvista import examples

import numpy as np

import os

st.header("test large visualization")

# def uploader_cb():
#     print("Dummy callback for file uploader")

# # define: file variables with streamlit
# htmlFile = st.file_uploader("html file for display", type = 'html', on_change = uploader_cb())
# if htmlFile is None:
#     st.stop()

# # small mesh example    
# mesh = examples.load_uniform()
# pl = pv.Plotter(shape=(1,2))
# _ = pl.add_mesh(mesh, scalars='Spatial Point Data', show_edges=True)
# pl.subplot(0,1)
# _ = pl.add_mesh(mesh, scalars='Spatial Cell Data', show_edges=True)

# # large mesh example https://docs.pyvista.org/examples/00-load/terrain-mesh.html?highlight=terrain
###############################################################################
# Download a gridded topography surface (DEM)
dem = examples.download_crater_topo()
# dem

###############################################################################
# Now let's subsample and extract an area of interest to make this example
# simple (also the DEM we just load is pretty big).
# Since the DEM we loaded is a :class:`pyvista.UniformGrid` mesh, we can use
# the :func:`pyvista.UniformGridFilters.extract_subset` filter:
subset = dem.extract_subset((500, 900, 400, 800, 0, 0), (5, 5, 1))
# subset.plot(cpos="xy")


###############################################################################
# Now that we have a region of interest for our terrain following mesh, lets
# make a 3D surface of that DEM:
terrain = subset.warp_by_scalar()
# terrain

###############################################################################
# terrain.plot()


###############################################################################
# And now we have a 3D structured surface of the terrain! We can now extend
# that structured surface into a 3D mesh to form a terrain following grid.
# To do this, we first our cell spacings in the z-direction (these start
# from the terrain surface). Then we repeat the XYZ structured coordinates
# of the terrain mesh and decrease each Z level by our Z cell spacing.
# Once we have those structured coordinates, we can create a
# :class:`pyvista.StructuredGrid`.

z_cells = np.array([25] * 5 + [35] * 3 + [50] * 2 + [75, 100])

xx = np.repeat(terrain.x, len(z_cells), axis=-1)
yy = np.repeat(terrain.y, len(z_cells), axis=-1)
zz = np.repeat(terrain.z, len(z_cells), axis=-1) - np.cumsum(z_cells).reshape((1, 1, -1))

mesh = pv.StructuredGrid(xx, yy, zz)
mesh["Elevation"] = zz.ravel(order="F")
mesh

###############################################################################
cpos = [
    (1826736.796308761, 5655837.275274233, 4676.8405505181745),
    (1821066.1790519988, 5649248.765538796, 943.0995128226014),
    (-0.2797856225380979, -0.27966946337594883, 0.9184252809434081),
]

# mesh.plot(show_edges=True, lighting=False, cpos=cpos)

pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, lighting=False)
pl.camera_position = cpos
# plotter.show()

pv.start_xvfb()
# if os.path.exists('vtkjs.html'):
#     os.remove('vtkjs.html')
pl.export_html('vtkjs.html', backend='panel')
htmlFile = open('vtkjs.html', 'r', encoding='utf-8')
    
# # display: show html file
# source_code = htmlFile.getvalue().decode('utf-8')
# components.html(source_code, height=1000)

# st.text(htmlFile.getvalue().decode('utf-8'))

# display: show html file
source_code = htmlFile.read()
components.html(source_code, width=800, height=400)