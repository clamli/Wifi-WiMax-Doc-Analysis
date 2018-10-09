# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 00:31:25 2018

@author: Administrator
"""

import os, pickle
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
def convertFile(file):
#    if (file.endswith(".ppt")):
#        try:
#            os.system(os.path.join(cmdPPT, file))
#        except:
#            return
    if (file.endswith(".doc")):
        try:
            os.system(os.path.join(cmdDOC, file))
        except:
            return
def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    p = ThreadPool(1)
    res = p.apply_async(func, args=args)
    try:
        out = res.get(timeout)  # Wait timeout seconds for func to complete.
        return out
    except multiprocessing.TimeoutError:
        print("Aborting due to timeout")
        p.terminate()
        raise
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
    for file in fileNames:
        abortable_func = partial(abortable_worker, convertFile, timeout=15)
        p.apply_async(abortable_func, args=file)
