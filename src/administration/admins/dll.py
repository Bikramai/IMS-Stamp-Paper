
class ReportNonJudicial:

    def __init__(
            self, treasury, s100, s150, s200, s250, s300, s400, s500, s750, s1000, s2000, s3000, s5000, s10000,
            s25000, s50000
    ):
        self.treasury = treasury
        self.s100 = s100
        self.s150 = s150
        self.s200 = s200
        self.s250 = s250
        self.s300 = s300
        self.s400 = s400
        self.s500 = s500
        self.s750 = s750
        self.s1000 = s1000
        self.s2000 = s2000
        self.s3000 = s3000
        self.s5000 = s5000
        self.s10000 = s10000
        self.s25000 = s25000
        self.s50000 = s50000

    def __str__(self):
        return self.treasury

    def increase(
            self, s100, s150, s200, s250, s300, s400, s500, s750, s1000, s2000, s3000, s5000, s10000, s25000, s50000
    ):
        self.s100 += s100
        self.s150 += s150
        self.s200 += s200
        self.s250 += s250
        self.s300 += s300
        self.s400 += s400
        self.s500 += s500
        self.s750 += s750
        self.s1000 += s1000
        self.s2000 += s2000
        self.s3000 += s3000
        self.s5000 += s5000
        self.s10000 += s10000
        self.s25000 += s25000
        self.s50000 += s50000

    def __sub__(self, other):
        return ReportNonJudicial(
            self.treasury, self.s100 - other.s100, self.s150 - other.s150, self.s200 - other.s200, self.s250 - other.s250,
            self.s300 - other.s300, self.s400 - other.s400, self.s500 - other.s500, self.s750 - other.s750,
            self.s1000 - other.s1000, self.s2000 - other.s2000, self.s3000 - other.s3000, self.s5000 - other.s5000,
            self.s10000 - other.s10000, self.s25000 - other.s25000, self.s50000 - other.s50000
        )

    def __add__(self, other):
        return ReportNonJudicial(
            self.treasury, self.s100 + other.s100, self.s150 + other.s150, self.s200 + other.s200, self.s250 + other.s250,
            self.s300 + other.s300, self.s400 + other.s400, self.s500 + other.s500, self.s750 + other.s750,
            self.s1000 + other.s1000, self.s2000 + other.s2000, self.s3000 + other.s3000, self.s5000 + other.s5000,
            self.s10000 + other.s10000, self.s25000 + other.s25000, self.s50000 + other.s50000
        )

    def sum(self):
        result = (self.s100 + self.s150 + self.s200 + self.s250 + self.s300 + self.s400 + self.s500 + self.s750 +
                  self.s1000 + self.s2000 + self.s3000 + self.s5000 + self.s10000 + self.s25000 + self.s50000)
        return result

    def sum_amount(self):
        result = (self.s100 * 100 + self.s150 * 150 + self.s200 * 200 + self.s250 * 250 + self.s300 * 300 +
                  self.s400 * 400 + self.s500 * 500 + self.s750 * 750 + self.s1000 * 1000 + self.s2000 * 2000 +
                  self.s3000 * 3000 + self.s5000 * 5000 + self.s10000 * 10000 + self.s25000 * 25000 +
                  self.s50000 * 50000)
        return '{:.1f}'.format(result)

    def sum_manufacturing_cost(self):
        result = float(self.sum()) * 27.423
        return '{:.1f}'.format(result)

    def sum_high_denomination(self):
        # >= 2000
        result = (self.s2000 + self.s3000 + self.s5000 + self.s10000 + self.s25000 + self.s50000)
        return result

    def sum_low_denomination(self):
        # < 2000
        result = (self.s100 + self.s150 + self.s200 + self.s250 + self.s300 + self.s400 + self.s500 + self.s750 + self.s1000)
        return result

    def sum_high_denomination_amount(self):
        result = (
                self.s2000 * 2000 + self.s3000 * 3000 + self.s5000 * 5000 + self.s10000 * 10000 +
                self.s25000 * 25000 + self.s50000 * 50000
        )
        return '{:.1f}'.format(result)

    def sum_low_denomination_amount(self):
        result = (
                self.s100 * 100 + self.s150 * 150 + self.s200 * 200 + self.s250 * 250 + self.s300 * 300 +
                self.s400 * 400 + self.s500 * 500 + self.s750 * 750 + self.s1000 * 1000
        )
        return '{:.1f}'.format(result)

    def sum_high_manufacturing_cost(self):
        result = float(self.sum_high_denomination()) * 27.423
        return '{:.1f}'.format(result)

    def sum_low_manufacturing_cost(self):
        result = float(self.sum_low_denomination()) * 27.423
        return '{:.1f}'.format(result)


class ReportJudicial:

    def __init__(
            self, treasury, j25, j30, j35, j50, j60, j75, j100, j125, j150, j200, j500,
            j1000, j2000, j3000, j5000, j10000, j15000
    ):
        self.treasury = treasury
        self.j25 = j25
        self.j30 = j30
        self.j35 = j35
        self.j50 = j50
        self.j60 = j60
        self.j75 = j75
        self.j100 = j100
        self.j125 = j125
        self.j150 = j150
        self.j200 = j200
        self.j500 = j500
        self.j1000 = j1000
        self.j2000 = j2000
        self.j3000 = j3000
        self.j5000 = j5000
        self.j10000 = j10000
        self.j15000 = j15000

    def __str__(self):
        return self.treasury

    def increase(
            self, j25, j30, j35, j50, j60, j75, j100, j125, j150, j200, j500, j1000,
            j2000, j3000, j5000, j10000, j15000
    ):
        self.j25 += j25
        self.j30 += j30
        self.j35 += j35
        self.j50 += j50
        self.j60 += j60
        self.j75 += j75
        self.j100 += j100
        self.j125 += j125
        self.j150 += j150
        self.j200 += j200
        self.j500 += j500
        self.j1000 += j1000
        self.j2000 += j2000
        self.j3000 += j3000
        self.j5000 += j5000
        self.j10000 += j10000
        self.j15000 += j15000

    def __add__(self, other):
        return ReportJudicial(
            self.treasury, self.j25 + other.j25, self.j30 + other.j30, self.j35 + other.j35, self.j50 + other.j50,
            self.j60 + other.j60, self.j75 + other.j75, self.j100 + other.j100, self.j125 + other.j125,
            self.j150 + other.j150, self.j200 + other.j200, self.j500 + other.j500, self.j1000 + other.j1000,
            self.j2000 + other.j2000, self.j3000 + other.j3000, self.j5000 + other.j5000, self.j10000 + other.j10000,
            self.j15000 + other.j15000
        )

    def __sub__(self, other):
        return ReportJudicial(
            self.treasury, self.j25 - other.j25, self.j30 - other.j30, self.j35 - other.j35, self.j50 - other.j50,
            self.j60 - other.j60, self.j75 - other.j75, self.j100 - other.j100, self.j125 - other.j125,
            self.j150 - other.j150, self.j200 - other.j200, self.j500 - other.j500, self.j1000 - other.j1000,
            self.j2000 - other.j2000, self.j3000 - other.j3000, self.j5000 - other.j5000, self.j10000 - other.j10000,
            self.j15000 - other.j15000
        )

    def sum(self):
        result = (self.j25 + self.j30 + self.j35 + self.j50 + self.j60 + self.j75 + self.j100 + self.j125 +
                  self.j150 + self.j200 + self.j500 + self.j1000 + self.j2000 + self.j3000 + self.j5000 +
                  self.j10000 + self.j15000)
        return result

    def sum_amount(self):
        result = (
                self.j25 * 25 + self.j30 * 30 + self.j35 * 35 + self.j50 * 50 + self.j60 * 60 + self.j75 * 75 +
                self.j100 * 100 + self.j125 * 125 + self.j150 * 150 + self.j200 * 200 + self.j500 * 500 +
                self.j1000 * 1000 + self.j2000 * 2000 + self.j3000 * 3000 + self.j5000 * 5000 +
                self.j10000 * 10000 + self.j15000 * 15000
        )
        return '{:.1f}'.format(result)

    def sum_manufacturing_cost(self):
        result = float(self.sum()) * 27.423
        return '{:.1f}'.format(result)

    def sum_high_denomination(self):
        # >= 2000
        result = (self.j2000 + self.j3000 + self.j5000 + self.j10000 + self.j15000)
        return result

    def sum_low_denomination(self):
        # < 2000
        result = (
                self.j25 + self.j30 + self.j35 + self.j50 + self.j60 + self.j75 + self.j100 + self.j125 +
                self.j150 + self.j200 + self.j500 + self.j1000
        )
        return result

    def sum_high_denomination_amount(self):
        result = (self.j2000 * 2000 + self.j3000 * 3000 + self.j5000 * 5000 + self.j10000 * 10000 + self.j15000 * 15000)
        return '{:.1f}'.format(result)

    def sum_low_denomination_amount(self):
        result = (
                self.j25 * 25 + self.j30 * 30 + self.j35 * 35 + self.j50 * 50 + self.j60 * 60 + self.j75 * 75 +
                self.j100 * 100 + self.j125 * 125 + self.j150 * 150 + self.j200 * 200 + self.j500 * 500 +
                self.j1000 * 1000
        )
        return '{:.1f}'.format(result)

    def sum_high_manufacturing_cost(self):
        result = float(self.sum_high_denomination()) * 27.423
        return '{:.1f}'.format(result)

    def sum_low_manufacturing_cost(self):
        result = float(self.sum_low_denomination()) * 27.423
        return '{:.1f}'.format(result)


class ReportConsolidated:

    def __init__(self, treasury, non_judicial, judicial):
        self.treasury = treasury
        self.non_judicial = non_judicial
        self.judicial = judicial

    def __str__(self):
        return self.treasury.name or "-"

    def counts_judicial(self):
        return (
            self.judicial.j25 + self.judicial.j30 + self.judicial.j35 + self.judicial.j50 + self.judicial.j60 +
            self.judicial.j75 + self.judicial.j100 + self.judicial.j125 + self.judicial.j150 + self.judicial.j200 +
            self.judicial.j500 + self.judicial.j1000 + self.judicial.j2000 + self.judicial.j3000 + self.judicial.j5000 +
            self.judicial.j10000 + self.judicial.j15000
        ) or 0

    def counts_non_judicial(self):
        return (
            self.non_judicial.s100 + self.non_judicial.s150 + self.non_judicial.s200 + self.non_judicial.s250 +
            self.non_judicial.s300 + self.non_judicial.s400 + self.non_judicial.s500 + self.non_judicial.s750 +
            self.non_judicial.s1000 + self.non_judicial.s2000 + self.non_judicial.s3000 + self.non_judicial.s5000 +
            self.non_judicial.s10000 + self.non_judicial.s25000 + self.non_judicial.s50000
        ) or 0

    def amounts_judicial(self):
        return (
            self.judicial.j25 * 25 + self.judicial.j30 * 30 + self.judicial.j35 * 35 + self.judicial.j50 * 50 +
            self.judicial.j60 * 60 + self.judicial.j75 * 75 + self.judicial.j100 * 100 + self.judicial.j125 * 125 +
            self.judicial.j150 * 150 + self.judicial.j200 * 200 + self.judicial.j500 * 500 + self.judicial.j1000 * 1000 +
            self.judicial.j2000 * 2000 + self.judicial.j3000 * 3000 + self.judicial.j5000 * 5000 +
            self.judicial.j10000 * 10000 + self.judicial.j15000 * 15000
        ) or 0

    def amounts_non_judicial(self):
        return (
            self.non_judicial.s100 * 100 + self.non_judicial.s150 * 150 + self.non_judicial.s200 * 200 +
            self.non_judicial.s250 * 250 + self.non_judicial.s300 * 300 + self.non_judicial.s400 * 400 +
            self.non_judicial.s500 * 500 + self.non_judicial.s750 * 750 + self.non_judicial.s1000 * 1000 +
            self.non_judicial.s2000 * 2000 + self.non_judicial.s3000 * 3000 + self.non_judicial.s5000 * 5000 +
            self.non_judicial.s10000 * 10000 + self.non_judicial.s25000 * 25000 + self.non_judicial.s50000 * 50000
        ) or 0

    def counts_total(self):
        return self.counts_judicial() + self.counts_non_judicial()

    def amounts_total(self):
        return self.amounts_judicial() + self.amounts_non_judicial()


class NonJudicialDenomination:

    def __init__(
            self, title, s100, s150, s200, s250, s300, s400, s500, s750, s1000,
            s2000, s3000, s5000, s10000, s25000, s50000
    ):
        self.title = title
        self.s100 = s100
        self.s150 = s150
        self.s200 = s200
        self.s250 = s250
        self.s300 = s300
        self.s400 = s400
        self.s500 = s500
        self.s750 = s750
        self.s1000 = s1000
        self.s2000 = s2000
        self.s3000 = s3000
        self.s5000 = s5000
        self.s10000 = s10000
        self.s25000 = s25000
        self.s50000 = s50000

    def __str__(self):
        return "Non-Judicial Denomination"
