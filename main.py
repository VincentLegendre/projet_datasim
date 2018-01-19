from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import dicom
import os
import numpy
import matplotlib
from matplotlib import pyplot as plt
#matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from backend_kivyagg import FigureCanvasKivyAgg

path_dicom='./images_dicom/'
lstFilesDCM = [path_dicom+'AI_OPTIM_CARTO.MR.POMMES_AI_FRUIT.0017.0001.2013.07.25.13.09.42.796875.5885010.dcm']
# Get ref file
RefDs = dicom.read_file(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
	# read the file
	ds = dicom.read_file(filenameDCM)
	# store the raw image data
	ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array  

plt.figure(dpi=200)
plt.axes().set_aspect('equal', 'datalim')
plt.set_cmap(plt.gray())
plt.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, 0]))

class ShowDicomApp(App):
	def build(self):
		box = BoxLayout()
		box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		return box   

if __name__ == '__main__':
	ShowDicomApp().run()