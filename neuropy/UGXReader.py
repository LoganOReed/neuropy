from dataclasses import dataclass
import zipfile
import json
import xmlschema
from lxml import etree
from io import StringIO, BytesIO

def readUGX(fileName):
    XSD_SCHEMA_PATH = "data/ugx.xsd"
    schema = etree.XMLSchema(etree.parse(XSD_SCHEMA_PATH))
    f = etree.parse("data/"+fileName)
    print(schema.validate(f))


    # TODO: Figure out what this diameter attachment stuff is




if __name__ == "__main__":
    readUGX("228-20MGv2.CNG_segLength=12_3d_tris_x1_ref_0.ugx")

