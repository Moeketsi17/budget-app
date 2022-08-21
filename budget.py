from unicodedata import name


class Category:
    def __init__(self, name):
        self.category = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False
        else:
            self.ledger.append({"amount": amount * -1, "description": description})
            return True
	
    def get_balance(self):
        fund = 0
        for transaction in self.ledger:
            fund += transaction["amount"]
        return fund

    def transfer(self, amount, budget):
        if not self.withdraw(amount, f"Transfer to {budget.category}"):
            return False
        else:
            budget.deposit(amount, f"Transfer from {self.category}")
            return True
	
    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        return True
	
    def get_withdraw_amount(self):
        amount = 0
        for t in self.ledger:
            if t["amount"] < 0:
                amount += t["amount"]
        return amount

    def calc_percentage_withdraw(self, total):
        return round(self.get_withdraw_amount() * -1 / total * 100 /10)*10

    def __repr__(self):
        num_ast = (30 - len(self.category)) // 2
        result = ""
        for i in range(num_ast):
            result += "*"
        result += self.category
        for i in range(num_ast):
            result += "*"
        result += "\n"

        for t in self.ledger:
            end = len(str(t["description"]))
            if end > 23:
                end = 23
            result += t["description"][0:end]

            amount = "{:.2f}".format(t["amount"])
            num_space = 7-len(str(amount)) + 23 - len(t["description"][0:end])

            for i in range(num_space):
                result += " "

            result += str(amount) + "\n"

        bal = "{:.2f}".format(self.get_balance())
        result += f"Total: {bal}"

        return result
			


def create_spend_chart(categories):
	total_withdraw = 0
	for c in categories:
		total_withdraw += c.get_withdraw_amount() * -1

	result = "Percentage spent by category\n"
	for i in range(10, -1, -1):
		if i * 10 == 100:
			result += str(i*10) + "|"
		elif i == 0:
			result += "  0|"
		else:
			result += " " + str(i * 10) + "|"
		
		for c in categories:
			result += " "
			if i*10 <= c.calc_percentage_withdraw(total_withdraw):
				result += "o"
			else:
				result += " "
			result += " "

		result += "\n"

	result += "    " + "".join(["-" for i in range(len(categories) * 3 + 1)]) + "\n"

	greatest_name_length = 0
	for i in categories:
		if len(i.category) > greatest_name_length:
			greatest_name_length = len(i.category)
	
	for i in range(greatest_name_length):
		result += "    "
		for c in categories:
			if i < len(c.category):
				result += " " + c.category[i] + " "
			else:
				result += "   "
		result += " \n"
	
	
	return result