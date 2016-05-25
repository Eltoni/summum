#-*- coding: UTF-8 -*-
import csv

def detecta_delimitador(csvFile):
    # delimitadores = ['\t', ';', ',', ' ']   # tab, ponto e virgula, virgula, espaço
    with open(csvFile) as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        return dialect.delimiter


def converte_bytes(size,precision=2):
    """
    Fonte: http://stackoverflow.com/a/32009595
    """
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1                        #increment the index of the suffix
        size = size/1024.0                      #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])