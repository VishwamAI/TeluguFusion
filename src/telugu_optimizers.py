import math

class స్టోకాస్టిక్_గ్రేడియంట్_డీసెంట్:
    def __init__(self, పారామీటర్లు, అభ్యాస_రేటు=0.01, మోమెంటమ్=0.9):
        self.పారామీటర్లు = పారామీటర్లు
        self.అభ్యాస_రేటు = అభ్యాస_రేటు
        self.మోమెంటమ్ = మోమెంటమ్
        self.వేగం = {param: 0 for param in self.పారామీటర్లు}

    def అడుగు(self, గ్రేడియంట్లు):
        for param, grad in zip(self.పారామీటర్లు, గ్రేడియంట్లు):
            self.వేగం[param] = self.మోమెంటమ్ * self.వేగం[param] - self.అభ్యాస_రేటు * grad
            param += self.వేగం[param]

class ఆడమ్:
    def __init__(self, పారామీటర్లు, అభ్యాస_రేటు=0.001, బీటా1=0.9, బీటా2=0.999, ఎప్సిలాన్=1e-8):
        self.పారామీటర్లు = పారామీటర్లు
        self.అభ్యాస_రేటు = అభ్యాస_రేటు
        self.బీటా1 = బీటా1
        self.బీటా2 = బీటా2
        self.ఎప్సిలాన్ = ఎప్సిలాన్
        self.m = {param: 0 for param in self.పారామీటర్లు}
        self.v = {param: 0 for param in self.పారామీటర్లు}
        self.t = 0

    def అడుగు(self, గ్రేడియంట్లు):
        self.t += 1
        for param, grad in zip(self.పారామీటర్లు, గ్రేడియంట్లు):
            self.m[param] = self.బీటా1 * self.m[param] + (1 - self.బీటా1) * grad
            self.v[param] = self.బీటా2 * self.v[param] + (1 - self.బీటా2) * (grad ** 2)

            m_hat = self.m[param] / (1 - self.బీటా1 ** self.t)
            v_hat = self.v[param] / (1 - self.బీటా2 ** self.t)

            param -= self.అభ్యాస_రేటు * m_hat / (math.sqrt(v_hat) + self.ఎప్సిలాన్)

# ఉదాహరణ వినియోగం:
# పారామీటర్లు = [1.0, 2.0, 3.0]
# sgd = స్టోకాస్టిక్_గ్రేడియంట్_డీసెంట్(పారామీటర్లు, అభ్యాస_రేటు=0.01)
# adam = ఆడమ్(పారామీటర్లు, అభ్యాస_రేటు=0.001)

# గ్రేడియంట్లు = [0.1, 0.2, 0.3]
# sgd.అడుగు(గ్రేడియంట్లు)
# adam.అడుగు(గ్రేడియంట్లు)

# print("SGD అప్డేట్ చేసిన పారామీటర్లు:", పారామీటర్లు)
# print("Adam అప్డేట్ చేసిన పారామీటర్లు:", పారామీటర్లు)
