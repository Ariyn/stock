# _*_ coding: utf-8 _*_
# faction.py

# NP-Faction needs these things
# name
# friendship
# money
# army
# identity

class Faction:
	def __init__(self, name, x, y, z, isPlayer=False, isCompany=False):
		self.name = name
		self.isPlayer, self.isCompany = isPlayer, isCompany
		self.x, self.y, self.z = x,y,z
		self.friendship = {}
		self.army, self.armyPoint = {}, 0
		self.money = 0

		self.inventory = []

	def EditMoney(self, money):
		self.money += money

	def AddItems(self, item, name, amount):
		self.inventory.append({"item":item, "name":name, "amount":amount})
		self.sortInventory()

	def sortInventory(self):
		newInv = {}
		
		for x in self.inventory:
			# print(x)
			if x["name"] in newInv:
				newItem = newInv[x["name"]]
				newItem["amount"] += x["amount"]
			else:
				newInv[x["name"]] = x
		del self.inventory
		self.inventory = newInv

class Company(Faction):
	def __init__(self, name):
		Faction.__init__(self, name, 0,0,0, isCompany = True)
		self.name = name
		# self.HQ, self.asset

class Building:
	def __init__(self, name, type, level=1):
		self.name, self.type = name, type
		self.level = level

class NN_Faction(Faction):
	def __init__(self, name, x, y, z, isPlayer=False):
		Faction.__init__(self, name, x, y, z, isPlayer = isPlayer)
		self.buildings = {"research":[], "mine":[], "armory":[]}


class Market:
	def __init__(self, factions):
		self.tradeQue = {}
		self.companyList = {}
		self.factions = {}

		for i in factions:
			self.AdmitFaction(i)

	def AdmitCompany(self, company):
		count = len(self.companyList)+1
		self.companyList[count] = {"company":company, "stock amount":1000000, "stock price":1000}

	def AdmitFaction(self, faction):
		name = faction.name
		if name not in self.factions:
			self.factions[name] = {"faction":faction, "stock":{}}

	def CompanyCheck(self, target = -1):
		retVal = None

		if type(target) == str:
			list = [self.companyList[x]["company"].name for x in self.companyList]
			if target in list:
				retVal = [self.companyList[x]["company"] for x in self.companyList if self.companyList[x]["company"].name == target]
				if retVal:
					retVal = retVal[0]
		elif type(target) == int:
			if target in self.companyList:
				retVal = self.companyList[target]["company"]
		else:
			print("error company doesn't exist")
		return retVal

	def OwnStocks(self, user, target=None):
		retVal = 0
		if user in self.factions:
			fac = self.factions[user]

			if target:
				if target in fac["stock"]:
					retVal = fac["stock"][target]
				else:
					retVal = 0
			else:
				retVal = fac["stock"]

		return retVal

	def AddStocks(self, user, target, amount):
		if user in self.factions:
			# print("in")
			fac = self.factions[user]
			if target in fac["stock"]:
				fac["stock"][target] += amount
			else:
				fac["stock"][target] = amount

	def AdmitOrder(self, user, target, orderType, price, amount):
		if target not in self.tradeQue:
			self.tradeQue[target] = {"sell":{}, "buy":{}}

		targetQue = self.tradeQue[target][orderType]
		if price not in targetQue:
			targetQue[price] = []
		targetQue[price].append(Order(user, target, orderType, amount, price))

	def CalcBidPrice(self, target):
		buy, sell = {}, {}
		buyQue, sellQue = self.tradeQue[target]["buy"], self.tradeQue[target]["sell"]
		buyList, sellList = sorted(buyQue, reverse=True), sorted(sellQue)

		if len(buyList) <= 0 or len(sellList) <= 0:
			# print(len(buyList), len(sellList))
			return False

		for buyPrice in buyList:
			totalAmount = [x.amount for x in buyQue[buyPrice]]
			buy[buyPrice] = sum(totalAmount)

		for sellPrice in sellList:
			totalAmount = [x.amount for x in sellQue[sellPrice]]
			sell[sellPrice] = sum(totalAmount)

		buyIndex, sellIndex =  0, 0
		orderSum = 0

		bigger, biggerType = len(buy) < len(sell) or len(sell) and len(buy), len(buy) > len(sell) or "small" and "buy"


		# refactorize like printOrder
		# put datas to one dictionary and loop with that data
		sumType = "buy"

		while (buyPrice != sellPrice) and (buyIndex < len(buy)) and (sellIndex < len(sell)):
			buyPrice, sellPrice = buyList[buyIndex], sellList[sellIndex]

			buyOrderSum, sellOrderSum = self._CheckAmountOrder(buy, buyList, buyIndex), self._CheckAmountOrder(sell, sellList, sellIndex)

			if buyPrice < sellPrice:
				if sumType == "buy":
					buyIndex -= 1
				else:
					sellIndex -= 1
				break

			if buyOrderSum < sellOrderSum:
				buyIndex += 1
				sumType = "buy"
			else:
				sellIndex += 1
				bumType = "sell"

		buyPrice, sellPrice = buyList[buyIndex], sellList[sellIndex]
		buyOrderSum, sellOrderSum = self._CheckAmountOrder(buy, buyList, buyIndex), self._CheckAmountOrder(sell, sellList, sellIndex)
		if buyPrice != sellPrice:
			print("Error, no trade", buyPrice, sellPrice)
			self.printOrder(target)
		else:
			price, orderSum = buyPrice, buyOrderSum - sellOrderSum
			# change current price of this company

			if orderSum < 0:
				pass
			elif orderSum > 0:
				pass
			print("successfull trade with "+str(buyPrice))
			# print("succeed")

			# the problem
			# many stocks bur now
			# solve the problem about current price
			for i in buyList[:buyList.index(buyPrice)+1]:
				for e in buyQue[i]:
					name = e.user
					if name not in self.factions:
						print("error raise no faction error")

					fac = self.factions[name]
					fac["faction"].money -= price*e.amount

					if target in fac["stock"]:
						fac["stock"][target] += e.amount
					else:
						fac["stock"][target] = e.amount

			for i in sellList[:sellList.index(sellPrice)+1]:
				for e in sellQue[i]:
					name = e.user
					if name not in self.factions:
						print("error raise no faction error")

					fac = self.factions[name]

					if target in fac["stock"]:
						fac["stock"][target] -= e.amount
						fac["faction"].money += price*e.amount
					else:
						print("error not enought stock")

	@staticmethod
	def _CheckAmountOrder(target, list, index):
		return sum([target[list[x]] for x in range(0, index+1)])

	def MetgeWithoutDup(self, listA, listB):
		return listA + list(set(listB) - set(listA))

	def printOrder(self, target):
		datas = {}
		buy, sell = {}, {}
		buyQue, sellQue = self.tradeQue[target]["buy"], self.tradeQue[target]["sell"]
		buyOrder, sellOrder = 0, 0
		buyList, sellList = sorted(buyQue, reverse=True), sorted(sellQue, reverse=True)

		for buyPrice in buyList:
			totalAmount = [x.amount for x in buyQue[buyPrice]]
			buy[buyPrice] = sum(totalAmount)

		for sellPrice in sellList:
			totalAmount = [x.amount for x in sellQue[sellPrice]]
			sell[sellPrice] = sum(totalAmount)
		
		for i in buy.items():
			datas[i[0]] = {"buysum":self._CheckAmountOrder(buy,buyList, buyList.index(i[0])), "buy":i[1], "sell":"", "sellsum":""}
		for i in sell.items():
			if i[0] in datas:
				datas[i[0]]["sell"], datas[i[0]]["sellsum"] = i[1], self._CheckAmountOrder(sell,sorted(sellQue), sorted(sellQue).index(i[0]))
			else:
				datas[i[0]] = {"sellsum":self._CheckAmountOrder(sell,sorted(sellQue), sorted(sellQue).index(i[0])),"sell":i[1], "buy":"", "buysum":""}


		template = "{0:8} | {1:8}\t{2:8}\t{3:8} | {4:8}"
		# _str = "sell\t\t\t\tprice\t\t\t\tbuy\n"
		print(template.format("sum", "sell", "price", "buy", "sum"))
		for index, i in enumerate(sorted(datas, reverse = True)):
			data = datas[i]

			# print (str(data["sellsum"]), str(data["sell"]), str(i), str(data["buy"]), str(data["buysum"]))
			print (template.format(str(data["sellsum"]), str(data["sell"]), str(i), str(data["buy"]), str(data["buysum"])))

		# print(_str)
		# while True:
		# 	buyPrice, sellPrice = buyList[buyOrder], sellList[sellOrder]
		# 	if buyPrice == sellPrice:
		# 		_str = str(buy[buyPrice])+" | "+str(buyPrice)+" | "+str(sell[sellPrice])
		# 	elif buyPrice 
class Order:
	def __init__(self, user, target, orderType, amount, price):
		self.user, self.target, self.amount, self.price, self.orderType = user, target, amount, price, orderType
		self.isDone, self.donePrice = False, -1


if __name__ == "__main__":
	testFactions = [NN_Faction("ariyn", 0,0,0), NN_Faction("ariyn1", 0,0,0), NN_Faction("ariyn2", 0,0,0),
					NN_Faction("rockpell", 0,0,0), NN_Faction("rockpell1", 0,0,0), NN_Faction("rockpell2", 0,0,0)]
	
	m = Market(testFactions)
	m.AdmitCompany(Company("Faction1's Tungsten Mine"))

	m.AddStocks("rockpell", 1, 5000)
	m.AddStocks("rockpell1", 1, 5000)
	m.AddStocks("rockpell2", 1, 5000)

	for i in ["ariyn", "ariyn1", "ariyn2", "rockpell", "rockpell1", "rockpell2"]:
		print(i, m.OwnStocks(i))

	print(m.CompanyCheck("Faction1's Tungsten Mine").name)

	m.AdmitOrder("ariyn", 1, "buy", 15400, 1000)
	m.AdmitOrder("ariyn", 1, "buy", 15350, 300)
	m.AdmitOrder("ariyn1", 1, "buy", 15300, 200)
	m.AdmitOrder("ariyn", 1, "buy", 15300, 500)
	m.AdmitOrder("ariyn1", 1, "buy", 15300, 3000)
	m.AdmitOrder("ariyn", 1, "buy", 15250, 200)
	m.AdmitOrder("ariyn2", 1, "buy", 15200, 200)
	m.AdmitOrder("ariyn", 1, "buy", 15150, 200)
	m.AdmitOrder("ariyn2", 1, "buy", 15100, 200)
	m.AdmitOrder("ariyn", 1, "buy", 15100, 500)
	m.AdmitOrder("ariyn", 1, "buy", 15100, 100)


	m.AdmitOrder("rockpell", 1, "sell", 15350, 100)
	m.AdmitOrder("rockpell", 1, "sell", 15300, 500)
	m.AdmitOrder("rockpell1", 1, "sell", 15250, 100)
	m.AdmitOrder("rockpell", 1, "sell", 15250, 500)

	m.AdmitOrder("rockpell", 1, "sell", 15250, 1000)
	m.AdmitOrder("rockpell2", 1, "sell", 15250, 2000)
	m.AdmitOrder("rockpell1", 1, "sell", 15200, 150)
	m.AdmitOrder("rockpell1", 1, "sell", 15150, 500)
	m.AdmitOrder("rockpell", 1, "sell", 15150, 150)
	m.AdmitOrder("rockpell2", 1, "sell", 15100, 500)
	m.AdmitOrder("rockpell2", 1, "sell", 15050, 150)

	m.printOrder(1)
	m.CalcBidPrice(1)
	
	for i in ["ariyn", "ariyn1", "ariyn2", "rockpell", "rockpell1", "rockpell2"]:
		# user = m.
		print(i, m.OwnStocks(i))

	print(25162500+40412500+11437500 - 30500000-48800000)
