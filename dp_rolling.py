#!/usr/bin/python3
#
# dynamic programming rolling approach for edit
#

_MAX = 61
_OO = (1 << 60)
import sys
dis = [[0 for _ in range(8)] for _ in range(8)]
for i in range(8):
	for j in range(8):
		dis[i][j] = min(abs(i - j), min(i, j) + 8 - max(i, j)) * 1/2
print('coco')
# allocate memory once
_DP_ROLL = [[_OO for x in range(_MAX)] for y in range(2)]
c = 0
def dp_rolling_ed(s1, s2):
	global c
	sz1 = len(s1)
	sz2 = len(s2)
	c += 1
	if c%1000 == 0:
		print(c//1000)
		sys.stdout.flush()
	for i in range(sz2 + 1):
		_DP_ROLL[0][i] = i

	for i in range(1, sz1 + 1):
		_DP_ROLL[i % 2][0] = i
		for j in range(1, sz2 + 1):
			if(s1[i - 1] == s2[j - 1]):
				_DP_ROLL[i % 2][j] = _DP_ROLL[(i + 1) % 2][j - 1]
			else:
				if min(_DP_ROLL[(i + 1) % 2][j], _DP_ROLL[i % 2][j - 1]) < _DP_ROLL[(i + 1) % 2][j - 1]:
					cost = 1
				else:
					cost = dis[int(s1[i - 1])][int(s2[j - 1])]
					
				_DP_ROLL[i % 2][j] = cost + min(_DP_ROLL[(i + 1) % 2][j],
											_DP_ROLL[i % 2][j - 1], _DP_ROLL[(i + 1) % 2][j - 1])
	return _DP_ROLL[sz1 % 2][sz2]

if __name__ == "__main__":
	print(dp_rolling_ed("02156", "431515"))
	print(dp_rolling_ed("342345", "12366546"))
	print(dp_rolling_ed("056652156", "431123132515"))
	print(dp_rolling_ed("34534534535345353", "431515"))
	print(dp_rolling_ed("214513654", "1247650165725"))
	

	