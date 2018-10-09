# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 00:21:42 2018
this file is used to convert all the doc and ppt file in 80211mentor included file list
@author: Administrator
"""

#command line
import os, pickle
def convertFile(file):
    if (file.endswith(".ppt")):
        try:
            os.system(os.path.join(cmdPPT, file))
        except:
            return
#    if (file.endswith(".doc")):
#        try:
#            os.system(os.path.join(cmdDOC, file))
#        except:
#            return
cmdPPT = 'D:\\Program_Files\\libreOffice\\program\\soffice.exe --writer --headless --convert-to pdf:writer_pdf_Export --outdir F:\\WireLessNLPGRA\\gitFiles\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\80211convertedPPT F:\\WireLessNLPGRA\\gitFiles\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\80211mentor\\'
cmdDOC = 'D:\\Program_Files\\libreOffice\\program\\soffice.exe --writer --headless --convert-to pdf:writer_pdf_Export --outdir F:\\WireLessNLPGRA\\gitFiles\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\80211convertedDOC F:\\WireLessNLPGRA\\gitFiles\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\80211mentor\\'
abbInfo = {
        "fileName":"80211mentorIncludedFileNames.dat",
        "abbWLDict": "80211mentorIncludedAbbWLDict.dat",
        "fileDir": "F:\\WireLessNLPGRA\\gitFiles\\Wifi-WiMax-Doc-Analysis\\Spider_Kay\\80211mentor"
        }
fileNames = pickle.load(open(abbInfo["fileName"], "rb"))
import multiprocessing
if __name__ == "__main__":
    p = multiprocessing.Pool(5)
    p.map(convertFile, [file for file in fileNames])