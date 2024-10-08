# telugu_gymnasium.py - జిమ్నేజియం లైబ్రరీ యొక్క తెలుగు అమలు

import random

class పర్యావరణం:
    def __init__(self):
        self.స్థితి = None
        self.చర్యల_సంఖ్య = 0
        self.పరిశీలనల_ఆకారం = None

    def ప్రారంభించు(self):
        raise NotImplementedError("ప్రారంభించు() పద్ధతిని అమలు చేయాలి")

    def చర్య_తీసుకొను(self, చర్య):
        raise NotImplementedError("చర్య_తీసుకొను() పద్ధతిని అమలు చేయాలి")

    def పరిశీలన_పొందు(self):
        raise NotImplementedError("పరిశీలన_పొందు() పద్ధతిని అమలు చేయాలి")

    def ముగిసిందా(self):
        raise NotImplementedError("ముగిసిందా() పద్ధతిని అమలు చేయాలి")

class సరళ_గ్రిడ్_ప్రపంచం(పర్యావరణం):
    def __init__(self, పరిమాణం=5):
        super().__init__()
        self.పరిమాణం = పరిమాణం
        self.గమ్యం = (పరిమాణం - 1, పరిమాణం - 1)
        self.స్థితి = (0, 0)
        self.చర్యల_సంఖ్య = 4  # ఎగువ, దిగువ, ఎడమ, కుడి
        self.పరిశీలనల_ఆకారం = (2,)  # x, y కోఆర్డినేట్లు

    def ప్రారంభించు(self):
        self.స్థితి = (0, 0)
        return self.స్థితి

    def చర్య_తీసుకొను(self, చర్య):
        x, y = self.స్థితి
        if చర్య == 0:  # ఎగువ
            y = max(0, y - 1)
        elif చర్య == 1:  # దిగువ
            y = min(self.పరిమాణం - 1, y + 1)
        elif చర్య == 2:  # ఎడమ
            x = max(0, x - 1)
        elif చర్య == 3:  # కుడి
            x = min(self.పరిమాణం - 1, x + 1)

        self.స్థితి = (x, y)
        బహుమతి = 1 if self.స్థితి == self.గమ్యం else 0
        ముగిసింది = self.స్థితి == self.గమ్యం

        return self.స్థితి, బహుమతి, ముగిసింది, {}

    def పరిశీలన_పొందు(self):
        return self.స్థితి

    def ముగిసిందా(self):
        return self.స్థితి == self.గమ్యం

class క్యూ_అభ్యాసకుడు:
    def __init__(self, చర్యల_సంఖ్య, అన్వేషణ_రేటు=0.1, తగ్గింపు_కారకం=0.95, అభ్యాస_రేటు=0.1):
        self.చర్యల_సంఖ్య = చర్యల_సంఖ్య
        self.అన్వేషణ_రేటు = అన్వేషణ_రేటు
        self.తగ్గింపు_కారకం = తగ్గింపు_కారకం
        self.అభ్యాస_రేటు = అభ్యాస_రేటు
        self.క్యూ_టేబుల్ = {}

    def చర్య_ఎంచుకోండి(self, స్థితి):
        if random.random() < self.అన్వేషణ_రేటు:
            return random.randint(0, self.చర్యల_సంఖ్య - 1)
        else:
            return max(range(self.చర్యల_సంఖ్య), key=lambda a: self.క్యూ_విలువ_పొందండి(స్థితి, a))

    def క్యూ_విలువ_పొందండి(self, స్థితి, చర్య):
        return self.క్యూ_టేబుల్.get((స్థితి, చర్య), 0.0)

    def నేర్చుకోండి(self, స్థితి, చర్య, బహుమతి, తదుపరి_స్థితి):
        ప్రస్తుత_క్యూ = self.క్యూ_విలువ_పొందండి(స్థితి, చర్య)
        ఉత్తమ_తదుపరి_క్యూ = max(self.క్యూ_విలువ_పొందండి(తదుపరి_స్థితి, a) for a in range(self.చర్యల_సంఖ్య))
        నవీకరణ = బహుమతి + self.తగ్గింపు_కారకం * ఉత్తమ_తదుపరి_క్యూ - ప్రస్తుత_క్యూ
        self.క్యూ_టేబుల్[(స్థితి, చర్య)] = ప్రస్తుత_క్యూ + self.అభ్యాస_రేటు * నవీకరణ

def శిక్షణ(పర్యావరణం, ఏజెంట్, ఎపిసోడ్లు=1000):
    for ఎపిసోడ్ in range(ఎపిసోడ్లు):
        స్థితి = పర్యావరణం.ప్రారంభించు()
        మొత్తం_బహుమతి = 0

        while not పర్యావరణం.ముగిసిందా():
            చర్య = ఏజెంట్.చర్య_ఎంచుకోండి(స్థితి)
            తదుపరి_స్థితి, బహుమతి, ముగిసింది, _ = పర్యావరణం.చర్య_తీసుకొను(చర్య)
            ఏజెంట్.నేర్చుకోండి(స్థితి, చర్య, బహుమతి, తదుపరి_స్థితి)
            స్థితి = తదుపరి_స్థితి
            మొత్తం_బహుమతి += బహుమతి

        if ఎపిసోడ్ % 100 == 0:
            print(f"ఎపిసోడ్ {ఎపిసోడ్}: మొత్తం బహుమతి = {మొత్తం_బహుమతి}")

# ఉదాహరణ వినియోగం
if __name__ == "__main__":
    పర్యావరణం = సరళ_గ్రిడ్_ప్రపంచం()
    ఏజెంట్ = క్యూ_అభ్యాసకుడు(చర్యల_సంఖ్య=పర్యావరణం.చర్యల_సంఖ్య)
    శిక్షణ(పర్యావరణం, ఏజెంట్)
