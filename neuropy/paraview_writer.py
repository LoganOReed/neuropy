import numpy

import graph
import solver

def vtu_write(filename,axon,t,tid):

	if axon: neuron = graph.neuron
	else: neuron = graph.neuronNoAxon

	f = open(filename,'w')
	f.write('<?xml version="1.0"?>')
	f.close()

	f = open(filename,'a')
	f.write('\n<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">')
	f.write('\n<Time timestep="' + str(t) + '"/>')
	f.write('\n<UnstructuredGrid>')

	f.write('\n<FieldData>')
	f.write('\n<DataArray type="Float64" Name="TimeValue" NumberOfTuples="1" format="ascii" RangeMin="'+str(t)+'" RangeMax="'+str(t)+'">')
	f.write('\n'+str(t))
	f.write('\n</DataArray>')
	f.write('\n</FieldData>')
	
	f.write('\n<Piece NumberOfPoints="' + str(len(neuron.nid)) + '" NumberOfCells="' + str(len(neuron.nid)-1) + '">')
	
	f.write('\n<Points>')
	f.write('\n<DataArray type="Float32" NumberOfComponents="3" format="ascii">')
	coord_string = []
	for i in range(len(neuron.coord)):
		coord_string.append([str(x) for x in neuron.coord[i]])
	coord_string = [x for xs in coord_string for x in xs]
	coord_string = ' '.join(coord_string)
	f.write('\n' + coord_string)
	f.write('\n</DataArray>')
	f.write('\n</Points>')

	f.write('\n<Cells>')
	
	f.write('\n<DataArray type="Int32" Name="connectivity" format="ascii">')
	edge_string = str(neuron.pid[1]) + ' ' + str(neuron.nid[1])
	for i in range(2,len(neuron.pid)):
		edge_string += ' ' + str(neuron.pid[i]) + ' ' + str(neuron.nid[i])
	f.write('\n' + edge_string)
	f.write('\n</DataArray>')

	f.write('\n<DataArray type="Int32" Name="offsets" format="ascii">')
	offset_string = '2'
	for i in range(4,2*len(neuron.nid),2):
		offset_string += ' ' + str(i)

	f.write('\n' + offset_string)
	f.write('\n</DataArray>')

	f.write('\n<DataArray type="Int8" Name="types" format="ascii">')
	type_string = '3'
	for i in range(1,len(neuron.nid)):
		type_string += ' 3'

	f.write('\n' + type_string)
	f.write('\n</DataArray>')

	f.write('\n</Cells>')
	
	f.write('\n<PointData>')

	f.write('\n<DataArray type="Float32" Name="CYT" NumberOfComponents="1" format="ascii">')
	cyt_string = str(solver.sol.C[0,tid])
	for i in range(1,len(neuron.nid)):
		cyt_string += ' ' + str(solver.sol.C[i,tid])
	f.write('\n' + cyt_string)
	f.write('\n</DataArray>')

	f.write('\n<DataArray type="Float32" Name="ER" NumberOfComponents="1" format="ascii">')
	er_string = str(solver.sol.CE[0,tid])
	for i in range(1,len(neuron.nid)):
		er_string += ' ' + str(solver.sol.CE[i,tid])
	f.write('\n' + er_string)
	f.write('\n</DataArray>')

	f.write('\n<DataArray type="Float32" Name="VOLTAGE" NumberOfComponents="1" format="ascii">')
	volt_string = str(solver.V[0,tid]*1e3)
	for i in range(1,len(neuron.nid)):
		volt_string += ' ' + str(solver.V[i,tid]*1e3)
	f.write('\n' + volt_string)
	f.write('\n</DataArray>')

	f.write('\n<DataArray type="Float32" Name="RADIUS" NumberOfComponents="1" format="ascii">')
	radius_string = str(neuron.radius[0]*1e5)
	for i in range(1,len(neuron.nid)):
		radius_string += ' ' + str(neuron.radius[i]*1e5)
	f.write('\n' + radius_string)
	f.write('\n</DataArray>')

	f.write('\n</PointData>')
	f.write('\n</Piece>')
	f.write('\n</UnstructuredGrid>')
	f.write('\n</VTKFile>')

	f.close()
