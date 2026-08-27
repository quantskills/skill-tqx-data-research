class UsVolumeFactor(Factor):
    def calculate(self, factors):
        return factors["volume"]
