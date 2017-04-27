import numpy as np
from PIL import Image
import csv
import sys



def read_sls(loc):
	f=open(loc, 'r')
	reader = csv.reader(f,delimiter=" ")
	data=[]	
	rownum = 0
	for row in reader:
		if rownum == 0:
			header =row
		elif rownum ==1:
			pass

		else:
			data.append(row)
	
		rownum+=1
	f.close()
	return header, data


def scan_header(header):
	#will count detectors and find elements
	ref=['O','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','El', 'Fe_L']
	el_dict={}
						

	#for st in header:
	#	for el in ref:
	#		if el in st:
	#			if el in el_dict.keys():
	#				old = el_dict[el]
	#				old.append(header.index(st)) #append new detctor index
	#				el_dict[el]=old
	#			else: #intiate keys
	#				el_dict[el]=[header.index(st)]

	for st in header:
		if st!='row' and st!='column':
			if st in el_dict.keys():
				old = el_dict[st]
				old.append(header.index(st)) #append new detctor index
				el_dict[st]=old
			else: #intiate keys
				el_dict[st]=[header.index(st)]

	return el_dict

def create_array(header,data,detector_element):
	#makes an array filled with values from the detector and element
	#detector_element should be in the header as string
	x_i=header.index('row')
	y_i =header.index("column")
	e_i = header.index(detector_element)
	point_value = {}
	lx=[]
	ly=[]
	l = range(len(data)-1)
	for row in l:
		point_value[float(data[row][x_i]),float(data[row][y_i])] = float(data[row][e_i])
		lx.append(float(data[row][x_i]))
		ly.append(float(data[row][y_i]))
	
	sx = list(set(lx))#no duplicates and sorted
	sy= list(set(ly)) #no duplicates and sorted
	sx.sort()
	sy.sort#(reverse=True)    #####WATCH! REVERSE TO DEAL WITH NEGATIVE NUMBERS########
	x_dict={}
	y_dict={}
	for i in range(len(sx)):
		x_dict[sx[i]]=i
	for i in range(len(sy)):
		y_dict[sy[i]]=i

	
	array = np.zeros((len(sx),len(sy)))
	for tup in point_value.iterkeys():
		array[x_dict[tup[0]],y_dict[tup[1]]] = point_value[tup]
		
	
	
	
	delx = (max(lx)-min(lx))/float(len(sx))
	dely = (max(ly)-min(ly))/float(len(sy))
	
	print delx
	print dely
	
	
	return array,delx,dely

def summ(row,indis):
	s=0
	for e_i in indis:
		s+=float(row[e_i])
	return s


def create_array_sum(header,data,list_of_indi):
	#list_of_inidi should be the list of cols that each detector is in
	#for a certain el

	x_i=header.index('row')
	y_i =header.index('column')
	point_value = {}
	lx=[]
	ly=[]
	l = range(len(data))
	for row in l:
		point_value[float(data[row][x_i]),float(data[row][y_i])] =summ(data[row],list_of_indi)
		lx.append(float(data[row][x_i]))
		ly.append(float(data[row][y_i]))
	
	sx = list(set(lx))#no duplicates and sorted
	sy= list(set(ly)) #no duplicates and sorted
	sx.sort()
	sy.sort(reverse=True)    #####WATCH! REVERSE TO DEAL WITH NEGATIVE NUMBERS########
	x_dict={}
	y_dict={}
	for i in range(len(sx)):
		x_dict[sx[i]]=i
	for i in range(len(sy)):
		y_dict[sy[i]]=i

	
	array = np.zeros((len(sx),len(sy)))
	for tup in point_value.iterkeys():
		array[x_dict[tup[0]],y_dict[tup[1]]] = point_value[tup]
		
	
	
	
	delx = (max(lx)-min(lx))/float(len(sx))
	dely = (max(ly)-min(ly))/float(len(sy))
	
	#print delx
	#print dely
	
	
	return array, delx,dely


class sls:
	def __init__(self,loc):
		#loc is the locations of the data
		self.loc=loc
		h,d = read_sls(loc)
		self.header = h
		self.data=d
		dic = scan_header(h)
		self.elements=dic.keys()
		self.el_dict = dic
		  
	def get_array(self,el): #will get summed array
		#el has to be in self.el
		dic= self.el_dict
		indis = dic[el]
		ar,delx,dely = create_array(self.header,self.data,el) ##TEST
		return ar,delx,dely
	
	def print_all(self): #will save all elements
		for el in self.elements:
			ar,delx,dely = self.get_array(el)
			i =Image.fromarray(np.transpose(ar)) #transpose to get to image coords
			i.save("{0}.tif".format(el))
		f=open("sls_reconstruct.log", 'w')
		f.write("pixel x (mm)={0} \npixel y (mm)={1}".format(dely,delx))
		f.close()
	
if __name__ == "__main__":
	DATA_DIR = "./2016_1210_092826_new_data_type.dat"

	#DATA_DIR = sys.argv[0]
	h,d=read_sls(DATA_DIR)
	#ar=create_array_sum(h,d,[193,194,195,196])
	
	#ar=create_array(h,d,"D1_PKa_corr") +create_array(h,d,"D2_PKa_corr")+create_array(h,d,"D3_PKa_corr")+create_array(h,d,"D4_PKa_corr")   
	#i=Image.fromarray(np.transpose(ar))
	#i.save("test1.tif")
	
	data = sls(DATA_DIR)
	data.print_all()

			
	

