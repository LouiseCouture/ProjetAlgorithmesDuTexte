import traceback
from .DNA_parser.sequence_parser import parseSequence
from .DNA_parser.CDS_parser import parseCDS
from ..app.logger import emitLog, Log
from Bio import Entrez

def parseFeatures(region_type, path, id, organism, record, worker=None):
    """
    Parse a feature in a record (GenBank file).

    Args:
        region_type (list): Types of DNA region to parse.
        path (string): Path of the organism in the "Result" folder.
        id (string): ID of the GenBank file.
        organism (string): Name of the organism.
        record (...): Record (content of the GenBank file).
    """
    emitLog(Log.INFO, "Start parsing id = " + str(id), worker)

    summary_handle = Entrez.esummary(db="nucleotide", id=id)
    summary_record = Entrez.read(summary_handle)
    chloro = False
    plasmid = False
    mito = False
    # Check if "Chloroplast" is in the title
    print(summary_record[0]["Title"])
    if "chloroplast" in summary_record[0]["Title"].lower():
        chloro = True
        emitLog(Log.DEBUG, "Chloroplast found in id = " + str(id), worker)
    elif "plasmid" in summary_record[0]["Title"].lower():
        plasmid = True
        emitLog(Log.DEBUG, "Plasmid found in id = " + str(id), worker)
    elif "mitochondrion" in summary_record[0]["Title"].lower():
        mito = True
        emitLog(Log.DEBUG, "Mitochondrion found in id = " + str(id), worker)
    summary_handle.close()

    # Initialize variables
    file_name = id.split(".")[0]
    if chloro:
        file_name = "Chloroplast_" + file_name
    elif plasmid:
        file_name = "Plasmid_" + file_name
    elif mito:
        file_name = "Mitochondrion_" + file_name
    DNA = None
    DNA_length = -1

    # Read DNA sequence from record
    try:
        DNA = record.seq
        DNA_length = len(DNA)
    except:
        emitLog(Log.ERROR, "Unable to read DNA sequence from id = " + str(id), worker)

    # Parse feature according to its type
    try:
        for feature in record.features:
            # if feature.type in region_type:
            if feature.type == "CDS" and (("CDS" in region_type) or ("intron" in region_type)):
                emitLog(Log.DEBUG, "CDS or intron in id = " + str(id), worker)
                parseCDS(path, file_name, id, organism, DNA, DNA_length, feature, "CDS" in region_type, "intron" in region_type, worker=worker)
            elif feature.type == "centromere" and "centromere" in region_type:
                emitLog(Log.DEBUG, "centromere in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "centromere", worker=worker)
            elif feature.type == "mobile_element" and "mobile_element" in region_type:
                emitLog(Log.DEBUG, "mobile_element in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "mobile_element", worker=worker)
            elif feature.type == "telomere" and "telomere" in region_type:
                emitLog(Log.DEBUG, "telomere in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "telomere", worker=worker)
            elif feature.type == "3'UTR" and "3'UTR" in region_type:
                emitLog(Log.DEBUG, "3'UTR in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "3'UTR", worker=worker)
            elif feature.type == "5'UTR" and "5'UTR" in region_type:
                emitLog(Log.DEBUG, "5'UTR in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "5'UTR", worker=worker)
            elif feature.type == "tRNA" and "tRNA" in region_type:
                emitLog(Log.DEBUG, "tRNA in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "tRNA", worker=worker)
            elif feature.type == "rRNA" and "rRNA" in region_type:
                emitLog(Log.DEBUG, "rRNA in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "rRNA", worker=worker)
            elif feature.type == "ncRNA" and "ncRNA" in region_type:
                emitLog(Log.DEBUG, "ncRNA in id = " + str(id), worker)
                parseSequence(path, file_name, id, organism, DNA, DNA_length, feature, "ncRNA", worker=worker)
    except:
        emitLog(Log.ERROR, traceback.format_exc(), worker)
        emitLog(Log.ERROR, "Unable to read feature(s) from id = " + str(id), worker)