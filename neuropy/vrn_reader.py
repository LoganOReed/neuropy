from dataclasses import dataclass
import zipfile
import json

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


    def readUGX(self, meshName):
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



if __name__ == "__main__":
    reader = VrnReader("data/228-20MGv2.CNG.vrn")
    # reader = VrnReader("data/Green_19weeks_Neuron4.CNG.vrn")
    reader.load()
    print(reader.list())
    print(reader.listRefinements())
    print(reader.readUGX(reader.getMesh1dName()))
    print(reader.getMesh2dName(2.5))
