import csv
import json
import random

class తెలుగు_డేటాలోడర్:
    def __init__(self, ఫైల్_పేరు, ఫైల్_రకం, బ్యాచ్_పరిమాణం=32, షఫుల్=True):
        self.ఫైల్_పేరు = ఫైల్_పేరు
        self.ఫైల్_రకం = ఫైల్_రకం
        self.బ్యాచ్_పరిమాణం = బ్యాచ్_పరిమాణం
        self.షఫుల్ = షఫుల్
        self.డేటా = self._డేటా_లోడ్_చేయి()

    def _డేటా_లోడ్_చేయి(self):
        if self.ఫైల్_రకం == 'csv':
            return self._csv_నుండి_లోడ్_చేయి()
        elif self.ఫైల్_రకం == 'json':
            return self._json_నుండి_లోడ్_చేయి()
        else:
            raise ValueError(f"మద్దతు లేని ఫైల్ రకం: {self.ఫైల్_రకం}")

    def _csv_నుండి_లోడ్_చేయి(self):
        with open(self.ఫైల్_పేరు, 'r', encoding='utf-8') as ఫైల్:
            రీడర్ = csv.DictReader(ఫైల్)
            return list(రీడర్)

    def _json_నుండి_లోడ్_చేయి(self):
        with open(self.ఫైల్_పేరు, 'r', encoding='utf-8') as ఫైల్:
            return json.load(ఫైల్)

    def బ్యాచ్లు_పొందండి(self):
        డేటా = self.డేటా.copy()
        if self.షఫుల్:
            random.shuffle(డేటా)

        for i in range(0, len(డేటా), self.బ్యాచ్_పరిమాణం):
            yield డేటా[i:i + self.బ్యాచ్_పరిమాణం]

# ఉదాహరణ వినియోగం:
# csv_లోడర్ = తెలుగు_డేటాలోడర్('డేటా.csv', 'csv', బ్యాచ్_పరిమాణం=64)
# json_లోడర్ = తెలుగు_డేటాలోడర్('డేటా.json', 'json', బ్యాచ్_పరిమాణం=32, షఫుల్=False)

# for బ్యాచ్ in csv_లోడర్.బ్యాచ్లు_పొందండి():
#     print(f"CSV బ్యాచ్ పరిమాణం: {len(బ్యాచ్)}")

# for బ్యాచ్ in json_లోడర్.బ్యాచ్లు_పొందండి():
#     print(f"JSON బ్యాచ్ పరిమాణం: {len(బ్యాచ్)}")
