import pandas as pd
import xml.etree.ElementTree as ET
# Regex för att garantera att ingen package-tagg har annan data än nplpackid
# <package>\n\s+<nplpackid>[0-9]{14}<\/nplpackid>\n\s+<(?!\/package>)
# <package>\n\s+<(?!nplpackid)

def get_text(e):
    if (e is not None):
        return(e.text)
    else:
        return(e)
    
tree = ET.parse("restnoteringar.xml")
root = tree.getroot()

df = pd.DataFrame(columns=["nplid", "nplpackid", "start_date", "end_date", "actual_date"])
ns = "urn:schemas-supply:instance:1"

for child in root:
    prods = child.find("{{{}}}medicinalproducts".format(ns))
    for prod in prods:
        nplid = get_text(prod.find("{{{}}}nplid".format(ns)))
        start = get_text(prod.find("{{{}}}forecast-start-date".format(ns)))
        end = get_text(prod.find("{{{}}}forecast-end-date".format(ns)))
        actual = get_text(prod.find("{{{}}}actual-end-date".format(ns)))
        for package in prod.findall("{{{}}}packages/".format(ns)):
            nplpackid = get_text(package.find("{{{}}}nplpackid".format(ns)))
            df.loc[len(df), :] = [nplid, nplpackid, start, end, actual] 
            
df.to_csv("restnoteringar_stadad.csv", index=False)
