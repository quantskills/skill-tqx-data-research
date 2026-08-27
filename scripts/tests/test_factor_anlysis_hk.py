class HkMomentumFactor(Factor):
    def calculate(self, factors):
        return factors["close"]
