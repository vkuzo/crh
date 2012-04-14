def paginationList(n):
	"""
	Returns a list of pagination boundaries in sets of 10
	For example, for 26 entries would return
	[
		[1,10],
		[11,20],
		[21,26]
	]
	"""
	#generate numbers for bottom navigation (1-10, 11-20, etc.)
	pList = [[i*10+1, i*10+10]  for i in range(int((n-1)/10)+1)]
	#override the last value to be the actual last value (ex 41 through 46 instead of 41 through 50 if there are 46 items)
	if len(pList)>0:
		pList[-1][1] = n
	return pList