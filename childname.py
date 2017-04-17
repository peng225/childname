#!/usr/bin/python

import argparse
import sys


class ChildName:
	def __init__(self, myojiKakusuus, addVirtualLetter):
		self._goodJinkakus = [11, 13, 15, 16, 17, 18, 21, 23]
		self._goodChikakus = [5, 6, 7, 8, 11, 13, 15, 16, 17, 18, 21, 23, 24, 25, 31, 32, 35]
		self._goodGaikakus = [5, 6, 8, 11, 13, 15, 16, 17, 18, 21, 23, 24, 25, 31]
		self._goodSoukakus = [13, 15, 16, 17, 18, 21, 23, 24, 25, 31, 32, 35, 37, 38, 41]

		self._forbiddenNameFirstKakusuus = [3, 5, 9, 13, 15, 19, 23]

		self._goodThreeOnmyoSequence = [[0, 1, 1], [0, 0, 1], [1, 0, 0], [1, 1, 0]]
		self._goodFourOnmyoSequence = [[0, 1, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 1]]
		self._goodFiveOnmyoSequence = [[0, 1, 0, 1, 1], [1, 0, 1, 0, 0], [1, 1, 0, 1, 0], [0, 0, 1, 0, 1], [0, 1, 0, 0, 1], [1, 0, 1, 1, 0]]
		self._goodSixOnmyoSequence = [[0, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1]]

		self._myojiKakusuus = myojiKakusuus

		self._addVirtualLetter = addVirtualLetter

		if self._addVirtualLetter and len(self._myojiKakusuus) == 1:
			virtualLetter = [1]
			self._myojiKakusuus = virtualLetter + self._myojiKakusuus
			print "Notice: A virtual letter is added at the top of myoji and now the list of myoji kakusuu is " + str(self._myojiKakusuus) + "."
			print "        This virtual letter is used for all but Soukaku calculation."


	def _isGoodJinkaku(self, nameKakusuus):
		jinkaku = self._myojiKakusuus[-1] + nameKakusuus[0]
		return jinkaku in self._goodJinkakus
	
	def _isGoodChikaku(self, nameKakusuus):
		chikaku = sum(nameKakusuus)
		return chikaku in self._goodChikakus
	
	def _isGoodGaikaku(self, nameKakusuus):
		# Please be careful that the length of the name is assumed to be larger than 1.
		if len(self._myojiKakusuus) == 1:
			gaikaku = self._myojiKakusuus[0] + sum(nameKakusuus[1:]) 
		else:
			gaikaku = sum(self._myojiKakusuus[0:-1]) + sum(nameKakusuus[1:]) 
		return gaikaku in self._goodGaikakus
	
	def _isGoodSoukaku(self, nameKakusuus):
		soukaku = sum(self._myojiKakusuus) + sum(nameKakusuus)
		if self._addVirtualLetter:
			soukaku -= 1
		return soukaku in self._goodSoukakus
	
	def _isGoodOnmyoSequence(self, nameKakusuus):
		totalLength = len(self._myojiKakusuus) + len(nameKakusuus)
		if totalLength < 3 or 6 < totalLength:
			print "Warning: Onmyo sequence calculation is not supported for the length of the name " + str(totalLength) + "."
			return True
	
		onmyoSequence = []
		for i in self._myojiKakusuus:
			if i % 2 == 0:
				onmyoSequence.append(0)
			else:
				onmyoSequence.append(1)
	
		for i in nameKakusuus:
			if i % 2 == 0:
				onmyoSequence.append(0)
			else:
				onmyoSequence.append(1)
	
		if totalLength == 3:
			return onmyoSequence in self._goodThreeOnmyoSequence
		elif totalLength == 4:
			return onmyoSequence in self._goodFourOnmyoSequence
		elif totalLength == 5:
			return onmyoSequence in self._goodFiveOnmyoSequence
		elif totalLength == 6:
			return onmyoSequence in self._goodSixOnmyoSequence
		else:
			print "Fatal Error."	
			sys.exit(1)
				
	
	def _isGoodKakusuu(self, nameKakusuus, isVerbose):
		if(self._isGoodJinkaku(nameKakusuus)
			and self._isGoodChikaku(nameKakusuus)
			and self._isGoodGaikaku(nameKakusuus)
			and self._isGoodSoukaku(nameKakusuus)
			and self._isGoodOnmyoSequence(nameKakusuus)):
			return True
		else:
			if isVerbose:
				if not self._isGoodJinkaku(nameKakusuus):
					print "Bad Jinkaku."
				elif not self._isGoodChikaku(nameKakusuus):
					print "Bad Chikaku."
				elif not self._isGoodGaikaku(nameKakusuus):
					print "Bad Gaikaku."
				elif not self._isGoodSoukaku(nameKakusuus):
					print "Bad Soukaku."
				elif not self._isGoodOnmyoSequence(nameKakusuus):
					print "Bad Onmyo sequence."
			return False
	
	def _isForbiddenNameFirstKakusuu(self, nameFirstKakusuu):
		if nameFirstKakusuu in self._forbiddenNameFirstKakusuus:
			return True
		else:
			return False
	
	def printGoodKakusuus(self, minLetterKakusuu, maxLetterKakusuu, isVerbose):
	
		# Two letters
		if isVerbose:
			print "Start two letter kakusuu search."
		twoLetterAnswer = []
		for i in range(minLetterKakusuu, maxLetterKakusuu + 1):
			if isVerbose:
				print "i: " + str(i)
			if self._isForbiddenNameFirstKakusuu(i):
				if isVerbose:
					print "The kakusuu was found in the forbidden list. Skip."
				continue
			for j in range(minLetterKakusuu, maxLetterKakusuu + 1):
				nameKakusuus = [i, j]
				if isVerbose:
					print "Kakusuu: " + str(nameKakusuus)
				if(self._isGoodKakusuu(nameKakusuus, isVerbose)):
					twoLetterAnswer.append(nameKakusuus)
	
		if isVerbose:
			print "End two letter kakusuu search."

		# Three letters
		if isVerbose:
			print "Start three letter kakusuu search."
		threeLetterAnswer = []
		for i in range(minLetterKakusuu, maxLetterKakusuu + 1):
			if isVerbose:
				print "i: " + str(i)
			if self._isForbiddenNameFirstKakusuu(i):
				if isVerbose:
					print "The kakusuu was found in the forbidden list. Skip."
				continue
			for j in range(minLetterKakusuu, maxLetterKakusuu + 1):
				for k in range(minLetterKakusuu, maxLetterKakusuu + 1):
					nameKakusuus = [i, j, k]
					if isVerbose:
						print "Kakusuu: " + str(nameKakusuus)
					if(self._isGoodKakusuu(nameKakusuus, isVerbose)):
						threeLetterAnswer.append(nameKakusuus)
	
		if isVerbose:
			print "End three letter kakusuu search."
	
	
		print "==== Two letters ===="
		print str(len(twoLetterAnswer)) + " combinations found."
		for i in twoLetterAnswer:
			print i
	
		print "==== Three letters ===="
		print str(len(threeLetterAnswer)) + " combinations found."
		for i in threeLetterAnswer:
			print i


def main():
	parser = argparse.ArgumentParser(description='Print the good kakusuus of names.')
	parser.add_argument("-m", type=int, nargs='+', required=True,
                    help='The list of the kakusuus of each letter in your family name.')
	parser.add_argument("-v", help='Verbose mode.', action='store_true')
	parser.add_argument("-a", help='If myoji kakusuu is 1, add a vertual letter at the top of myoji.', action='store_true')
	parser.add_argument("--min", type=int, default=1,
                    help='The minimum kakusuu of a letter. (default = 1)')
	parser.add_argument("--max", type=int, default=15,
                    help='The maximum kakusuu of a letter. (default = 15)')

	args = parser.parse_args()

	childName = ChildName(args.m, args.a)
	childName.printGoodKakusuus(args.min, args.max, args.v)

if __name__ == "__main__":
	main()
