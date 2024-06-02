from __future__ import annotations
import pprint
from dataclasses import dataclass
import zipfile
import json
import xmlschema
from lxml import etree
from io import StringIO, BytesIO
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from vedo import Mesh, show


@dataclass
class Geom2d:
    """Stores the 1D geometries by name, refinement and a description. Inflations are attached to the 1D geometries as a list of Geom2ds"""
    name: str
    inflation: str
    description: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data.get('name'),
            inflation = data.get('inflation'),
            description = data.get('description')
        )




@dataclass
class Geom1d:
    """Stores the 1D geometries by name, refinement and a description. Inflations are attached to the 1D geometries as a list of Geom2ds"""
    name: str
    refinement: str
    description: str
    inflations: list[Geom2d]

    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data.get('name'),
            refinement = data.get('refinement'),
            description = data.get('description'),
            inflations = [Geom2d.from_dict(x) for x in data.get('inflations')]
                )



@dataclass
class Geometry:
    """Stores 1D and associated 2D geoms, as well as additional metadata"""
    geom1d: list[Geom1d]
    ARCHIVE: str
    STRAIN: str
    SPECIES: str

    @classmethod
    def from_dict(cls, data):
        return cls(
        geom1d = [Geom1d.from_dict(x) for x in data.get('geom1d')],
        ARCHIVE = data.get('ARCHIVE'),
        STRAIN = data.get('STRAIN'),
        SPECIES = data.get('SPECIES')
        )


class VrnReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.geometry = self.load()

    def load(self):
        with zipfile.ZipFile(f"{self.fileName}", 'r') as archive:
            file = archive.read('MetaInfo.json')
            geometry = Geometry.from_dict(json.loads(file))
            return geometry

    def list(self):
        output = f"Geometries contained in .vrn archive ({self.fileName}): "
        i = 0
        for g1d in self.geometry.geom1d:
            output += f"\n#{i} 1D geometry: {g1d.name} with refinement {g1d.refinement} ({g1d.description})."
            i += 1
        return output

    def listRefinements(self):
        options = []
        for g1d in self.geometry.geom1d:
            options.append(g1d.refinement)
        return options


    def readUGXRaw(self, meshName):
        with zipfile.ZipFile(f"{self.fileName}", 'r') as archive:
            file = archive.read(meshName)
            return file

    def getMesh1dName(self, refinement = 0):
        for g1d in self.geometry.geom1d:
            if g1d.refinement == str(refinement):
                return g1d.name


    def getMesh2dName(self, inflation = 1.0, refinement = 0):
        for g1d in self.geometry.geom1d:
            if g1d.refinement == str(refinement):
                for g2d in g1d.inflations:
                    if g2d.inflation == str(inflation):
                        return g2d.name


    def readUGX(self, fileName):
        XSD_SCHEMA_PATH = "data/ugx.xsd"
        MAPPING_FIELDS = 7
        schema = etree.XMLSchema(etree.parse(XSD_SCHEMA_PATH))

        g = nx.DiGraph()

        vertices = []
        neighbors = []
        edges = []
        triangles = []
        diameters = []
        normals = []
        mappings = []


        with zipfile.ZipFile(f"{self.fileName}", 'r') as archive:
            f = archive.read(fileName)
        context = etree.iterparse(BytesIO(f))
        for action, elem in context:
            if(elem is not None):
                if(elem.tag == "vertices"):
                    if elem.get("coords") != '3' and elem.get("coords") != None:
                        print(f"Only dim. 3 is supported but recieved a {elem.get("coords")}")
                    if elem.xpath("@coords='3'"):
                        indices = elem.text.split(' ')
                        size = len(indices) / 3
                        for i in range(int(size)):
                            vertices.append((indices[i*3], indices[i*3 + 1],indices[i*3 + 2]) )
                        # pprint.pp(vertices)

                

                if(elem.tag == "edges"):
                    indices = elem.text.split(' ')
                    size = len(indices) / 2
                    for i in range(int(size)):
                        edges.append((indices[i*2], indices[i*2 + 1]))
                        # I'll use networkx to calculate these instead
                        # neighbors[vertices[indices[i*2]]] = vertices[indices[i*2 + 1]]
                        # pprint.pp(vertices)

                    # NOTE: Look at index unity thing and see if i need it
                
                if(elem.tag == "triangles"):
                    triangles = elem.text.split(' ')
                

                if(elem.tag == "vertex_attachment"):
                    name = elem.xpath("@name")
                    if name[0] == "diameter":
                        diameter = elem.xpath("@type")
                        if diameter[0] == "double":
                            accessors = elem.text.split(' ')
                            for n in accessors:
                                diameters.append(n)
                    
                    if name[0] == "npNormals":
                        npm = elem.xpath("@type")
                        if npm[0] == "vector3":
                            accessors = elem.text.split(' ')
                            for i in range(int(len(accessors) / 3)):
                                normals.append([accessors[i*3], accessors[i*3 + 1], accessors[i*3 + 2]])


                    if name[0] == "synapses":
                        print("WARNING: synapses aren't currently implemented")
                

                    if name[0] == "npMapping":
                        mapping = elem.text.split(' ')
                        size = len(mapping) / MAPPING_FIELDS
                        if len(mapping) % MAPPING_FIELDS != 0:
                            print("Mapping vertex npMapping isn't in the correct format")

                        for i in range(int(size)):
                            mappings.append([[mapping[i * MAPPING_FIELDS], mapping[i * MAPPING_FIELDS + 1], mapping[i * MAPPING_FIELDS + 2]],
                                             [mapping[i * MAPPING_FIELDS], mapping[i * MAPPING_FIELDS + 1], mapping[i * MAPPING_FIELDS + 2]],
                                             mapping[i*MAPPING_FIELDS + 6]])


                    if name[0] == "subset_handler":
                        print("WARNING: subset_handler not implemented yet")

            
        # pprint.pp(f"mappings: {mappings}")
        pprint.pp(f"normals: {normals}")
        # pprint.pp(f"diameters: {diameters}")
        pprint.pp(f"triangles: {triangles}")

        grouped_tris = []
        for i in range(int(len(triangles) / 3)):
            grouped_tris.append((int(triangles[i*3]), int(triangles[i*3+1]), int(triangles[i*3+2])))

        # pprint.pp(f"neighbors: {neighbors}")
        # pprint.pp(f"edges: {edges}")
        # pprint.pp(f"verts: {vertices}")

        nodes = []
        for i in range(len(vertices)):
            nodes.append((str(i), {"x": vertices[i][0],"y": vertices[i][1],"z": vertices[i][2]}))


        v = vertices
        c = grouped_tris

        mesh = Mesh([v, c])

        mesh.backcolor('violet').linecolor('tomato').linewidth(2)

        # Print the points and faces of the mesh as numpy arrays
        print('vertices:', mesh.vertices)
        print('faces   :', mesh.cells)

# Show the mesh, vertex labels, and docstring
        show(mesh,  __doc__, viewup='z', axes=1).close()

        # g.add_nodes_from(nodes)
        # g.add_edges_from(edges)
        # print(f"nodes: {g.order()}    edges: {g.size()}")
        #
        # nx.draw_networkx(g)
        # nx.draw(g)
        # plt.show()








if __name__ == "__main__":
    # reader = VrnReader("data/RorBCreER-262-14-B_1.CNG.vrn")
    reader = VrnReader("data/228-18MG.CNG.vrn")
    # reader = VrnReader("data/Green_19weeks_Neuron4.CNG.vrn")
    # reader.load()
    # print(reader.list())
    # print(reader.listRefinements())
    # print(reader.readUGX(reader.getMesh1dName()))
    # print(reader.readUGX(reader.getMesh2dName()))
    # print(reader.getMesh1dName(1))
    reader.readUGX(reader.getMesh2dName())
