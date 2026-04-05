class Position:
    def __init__(self, budget):
        self.budget = budget
        self.cash = budget
        self.shares = 0.0
        self.avg_price = 0.0
        self.entry_date = None
        self.total_invested = 0.0
        self.history = []

    def buy(self, price, amount, date, reason):
        if self.cash >= amount:
            new_shares = amount / price
            self.avg_price = (self.avg_price * self.shares + amount) / (self.shares + new_shares)
            self.shares += new_shares
            self.cash -= amount
            self.entry_date = date if self.entry_date is None else self.entry_date
            self.history.append({"date": date, "type": "BUY", "price": price, "shares": new_shares, "reason": reason})
            return True
        return False

    def sell(self, price, ratio, date, reason):
        if self.shares > 0:
            sell_shares = self.shares * ratio
            self.cash += sell_shares * price
            self.shares -= sell_shares
            if self.shares == 0:
                self.avg_price = 0.0
                self.entry_date = None
            self.history.append({"date": date, "type": "SELL", "price": price, "shares": sell_shares, "reason": reason})
            return True
        return False