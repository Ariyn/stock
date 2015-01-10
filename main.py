# _*_ coding: utf-8 _*_

from faction import *
from map import *
from random import sample

class Engine:
	xSize, ySize, zSize = 9, 9, 9
	xOffset, yOffset, zOffset = -4, -4, -4
	def __init__(self):
		self.factions = {}
		self.resources = {}
		self.market = Market(self.factions)

		self.autoInit()

	def autoInit(self):
		self._mapInit()
		self._resourceInit()

	def _mapInit(self):
		self.map = [[[Tile(x,y,z) for x in range(self.xOffset, self.xOffset+self.xSize)] for y in range(self.yOffset, self.xOffset+self.ySize)] for z in range(self.zOffset, self.xOffset+self.zSize)]

	def _resourceInit(self):
		resourceTypes = ["metal", "silver", "gold", "tungsten", "uranium", "platinum", "tantalum", "lithium", "titanium", "vanadium", "chromium", "silicon", "gallium", "aluminium"]
		rateConsts = [1, 0.01, 0.001, 0.5, 0.78, 0.3, 0.5, 0.22, 0.5, 0.6, 1.2, 1.7, 2.5, 17.8]
		prices = [100, 250, 100, 300, 0,0,0,0,0,0,0,0,0,0]

		for key, type in enumerate(resourceTypes):
			res = Resource(type)
			rateConst = rateConsts[key]
			price = prices[key]
			self.resources[type] = {"resource":res, "rate":rateConst, "price":price, "name":type}
			# print(type, self.resources[type])

	def newFaction(self, faction):
		name = faction.name
		if name not in self.factions:
			self.market.AdmitFaction(faction)
			self.factions[name] = faction
		else:
			print("raise already faction name")

	def Trade(self, tUser, tType, tCompany, tAmount, tPrice = 0):
		user, company = self.UserCheck(tUser), self.market.CompanyCheck(tCompany)
		stock, money = self.market.OwnStocks(tUser, tCompany), user and user.money or 0
		suc = False

		if user and company:
			if (tType == "sell" and stock and tAmount <= stock)	or (tType == "buy" and money and tPrice * tAmount <= money):
				# order = Order(tUser, tCompany, tType, tAmount, tPrice)
				# print(tType)
				self.market.AdmitOrder(tUser, tCompany, tType, tPrice, tAmount)
				suc = True

		self.market.CalcBidPrice(tCompany)

		return suc

	def UserCheck(self, tUser):
		if type(tUser) == str and tUser in self.factions:
			return self.factions[tUser]
		else:
			print("raise user error. no such user")

	def buyStock(self, buyerName, target, amount):
		stock = self.market.CompanyCheck(target)
		if stock and buyerName in self.factions:
			buyer = self.factions[buyerName]
			realPrice = amount * self.resources[target]["price"]
			money = buyer.money
			# print(target, self.resources[target])

			if money >= realPrice:
				buyer.AddItems(self.resources[target]["resource"], target, amount)
				buyer.EditMoney(-realPrice)

	def sellStock(self, sellerName, target, amount):
		if sellerName in self.factions:
			pass


class Client:
	def __init__(self):
		pass

	def login(self, id, password):
		pass


class Tester:
	def __init__(self):
		self.tFaction, self.engine = [], Engine()
		self.market = self.engine.market
		self.facNames = ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8", "test9", "test10"]

		for name in self.facNames:
			fac = NN_Faction(name, 0,0,0)
			self.engine.newFaction(fac)
			self.tFaction.append(fac)
		
		self.engine.market.AdmitCompany(Company("Faction1's Tungsten Mine"))


	def TradeTest(self, tTarget, tMoney, tAmount):
		tUser1, tUser2 = sample(self.facNames, 2)
		user1, user2 = self.engine.UserCheck(tUser1), self.engine.UserCheck(tUser2)
		print(tUser1, tUser2)

		user1.money = tMoney
		self.market.AddStocks(tUser2, tTarget, tAmount)
		# print("stock", self.market.OwnStocks(tUser2, tTarget))

		money1, money2 = user1 and user1.money or 0, user2 and user2.money or 0
		print(money1, money2, self.market.OwnStocks(tUser1, tTarget), self.market.OwnStocks(tUser2, tTarget))

		# Tester.PrintInventory(player)

		print("----- trade on")

		suc = self.engine.Trade(tUser1, "buy", tTarget, tAmount, 1000)
	
		suc = self.engine.Trade(tUser2, "sell", tTarget, tAmount, 1000)

		if suc:
			print("----- trade off")
		else:
			print("----- trade error")

		money1, money2 = user1 and user1.money or 0, user2 and user2.money or 0
		print(money1, money2, self.market.OwnStocks(tUser1, tTarget), self.market.OwnStocks(tUser2, tTarget))
		# Tester.PrintInventory(player)

	@staticmethod
	def PrintInventory(faction):
		inv = faction.inventory
		string = u"inventory List"
		for x in inv:
			string += u"\n"+str(inv[x]["amount"])+"  "+str(x)+"s"

		string += u"\n-----------------"+str(len(faction.inventory))+" items"
		print(string)



if __name__ == "__main__":
	tester = Tester()
	tester.TradeTest(1, 100000, 100)