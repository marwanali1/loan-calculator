from calendar import monthrange
from datetime import datetime, timedelta, date
from enum import Enum
from typing import List

class PaymentPeriod(Enum):
    BIWEEKLY = "Biweekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    BIANNUALLY = "Biannually"


class Loan:

    def __init__(self, principal: float, interest_rate: float, payment_period: PaymentPeriod = PaymentPeriod.MONTHLY, origination_date: str = None, payment_per_period: float = 0,):
        super().__init__()

        self.principle = principal
        self.interest_rate = interest_rate
        self.payment_period = payment_period
        self.payment_per_period = payment_per_period

        if origination_date:
            self.origination_date = datetime.strptime(
                origination_date, '%Y-%m-%d').date()
        else:
            self.origination_date = datetime.now().date()

        self.payment_dates: List[datetime.date] = []
        self.payment_dates.append(self.origination_date)
        self.payment_dates.append(self.increment_date(self.origination_date))

        self.balances: List[float] = []
        self.balances.append(principal)

        self.monthly_principles: List[float] = []
        self.monthly_interests: List[float] = []

    def new_balance(self) -> float:
        previous_balance = self.balances[len(self.balances)-1]
        monthly_principle = self.monthly_principles[len(self.monthly_principles)-1]
        new_balance = previous_balance - monthly_principle
        return new_balance
    
    def new_interest_payment(self) -> float:
        previous_balance = self.balances[len(self.balances)-1]
        previous_date = self.payment_dates[len(self.payment_dates)-2]
        current_date = self.payment_dates[len(self.payment_dates)-1]
        delta = current_date - previous_date
        new_interest = ((previous_balance * self.interest_rate) / 365) * delta.days
        return new_interest
    
    def increment_date(self, source_date: datetime.date = None) -> datetime.date:
        if source_date is None:
            source_date = self.payment_dates[len(self.payment_dates)-1]

        month = source_date.month - 1 + 1
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, monthrange(year,month)[1])
        date_str = "{}-{}-{}".format(year, month, day)
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    def calculate_payment(self):
        balance = self.balances[len(self.balances)-1] < 0
        if balance:
            return

        interest_payment = self.new_interest_payment()
        self.monthly_interests.append(interest_payment)

        principle_payment = self.payment_per_period - interest_payment
        # if balance < self.payment_per_period:
        #     principle_payment = balance
        self.monthly_principles.append(principle_payment)

        new_bal = self.new_balance()
        if new_bal < 0:
            new_bal = 0
        self.balances.append(new_bal)

        next_pay_date = self.increment_date()
        self.payment_dates.append(next_pay_date)

        print("Balance: {}".format(new_bal))
        print("Interest Payment: {}".format(interest_payment))
        print("Principle Payment: {}".format(principle_payment))
        print("\n")


    def amortize(self):
        while self.balances[len(self.balances)-1] > 0:
            self.calculate_payment()

        print("Date: {}".format(self.payment_dates[len(self.payment_dates)-1]))
        print("Balance: {}".format(self.balances[len(self.balances)-1]))
        print("Interest Payment: {}".format(self.monthly_interests[len(self.monthly_interests)-1]))
        print("Principle Payment: {}".format(self.monthly_principles[len(self.monthly_principles)-1]))

    def __str__(self):
        loan_str = "Principal: ${}\nInterest Rate: {}%\nPayment Period: {}\nPayment per Period: ${}\nOrigination Date: {}".format(
            self.principle, self.interest_rate, self.payment_period.value, self.payment_per_period, self.origination_date)
        return loan_str

    def __repr__(self):
        loan_repr = "Loan(principal={}, interest_rate={}, payment_period={}, payment_per_period={}, origination_date={})".format(
            self.principle, self.interest_rate, self.payment_period.value, self.payment_per_period, self.origination_date)
        return loan_repr


if __name__ == "__main__":
    loan = Loan(principal=12997.61, interest_rate=0.0504, payment_per_period=324.82, origination_date="2020-06-25")
    loan.amortize()

    # print(loan)
    # print(repr(loan))

