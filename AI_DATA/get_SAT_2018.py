import re, requests, csv, pathlib
url = "https://21dzk.l.u-tokyo.ac.jp/SAT2018/master30.php?lang=en"
html = requests.get(url).text
links = re.findall(r'SAT2018/(JT\d{4}[a-z]?)\.xml', html)
pathlib.Path("xml").mkdir(exist_ok=True)
for jt in set(links):
    r = requests.get(f"https://21dzk.l.u-tokyo.ac.jp/SAT2018/{jt}.xml")
    open(f"xml/{jt}.xml", "wb").write(r.content)