#!/usr/bin/python3
#
# dynamic programming rolling approach for edit
#

_MAX = 200
_OO = (1 << 60)

def distance(i, j):
    i, j = int(i), int(j)
    return min(abs(i - j), min(i, j) + 8 - max(i, j)) * 1/2

# allocate memory once
_DP_ROLL = [[_OO for x in range(_MAX)] for y in range(2)]

def dp_rolling_ed(s1, s2):
	sz1 = len(s1)
	sz2 = len(s2)

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
					cost = distance(s1[i - 1], s2[j - 1])
					
				_DP_ROLL[i % 2][j] = cost + min(_DP_ROLL[(i + 1) % 2][j],
				                            _DP_ROLL[i % 2][j - 1], _DP_ROLL[(i + 1) % 2][j - 1])
	return _DP_ROLL[sz1 % 2][sz2]

if __name__ == "__main__":
	print(dp_rolling_ed("JEAN", "MONNET"))