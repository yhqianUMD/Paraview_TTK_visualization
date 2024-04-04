# Display a TIN in Paraview
Here are the steps to display a TIN in Paraview:
1. convert the TIN file (.tri or .off) to the format file; the triangle is in type "7".
2. use the Filters to generate scalar data based on the elevation value. Specifically, go to 'Filters->Alphabetical->Calculator'; in the Calculator filter properties, set the 'Result Array Name' as 'Elevation', and set the 'Expression' with 'coordsZ'; click 'Apply'.
3. customize the 'Color by' in the 'Properties' panel.
4. click 'Apply' to visualize the changes.

# Display the Forman gradient in Paraview
Here are the steps to display the Forman gradient in Paraview:
1. load the Forman gradient VTK file.
2. click 'Filters->Alphabetical->Glyph'
3. in the 'Properties', go to 'Masking' and then 'Glyph Mode', select the Glyph Mode as 'All Points'
Note: when displaying a VTK file, we can also show a VTK file as 'surface with edge' by changing the 'Representation' attribute in the 'Properties' panel.

# Display the critical points in Paraview
Here are the steps to display the critical points in Paraview:
1. load the critical points VTK file.
2. click 'Representation->Point Gaussian'
3. click 'Coloring -> critical'
4. in 'Point Gaussian', set the 'Gaussian Radius'
   
# Changing the background color
Remember to change the background color to white (in the 'Properties' panel) when displaying a VTK file.

# Changing the order in which one is rendered on top
This goal can be achieved by translating one of the planes a bit (probably in the z direction of the "Transforming -> Translation" attribute) so they are not rendered directly on top of each other.
Please refer to this link for more details: https://discourse.paraview.org/t/render-z-order-for-image-data/10432
