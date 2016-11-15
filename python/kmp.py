#!/usr/bin/env python3
#

#def partial_table(pat):
#	pnext, k = [], 0
#	for i, v in enumerate(pat):
#		if k == 0:
#			if i == 0:
#				pnext.append(k)
#			else:
#				if v == s[k]:
#					k += 1
#					pnext.append(k)
#				else:
#					pnext.append(k)
#		else:
#			if v == s[k]:
#				k += 1
#				pnext.append(k)
#			else:
#				while v != s[k] and k != 0:
#					k = pnext[k-1]
#				pnext.append(k)
#	return pnext


def partial_table(pat):
	k, m = 0, len(pat)
	pnext = [0] * m
	for i in range(1, m):
		while k > 0 and pat[k] != pat[i]:
			k = pnext[k - 1]
		if pat[k] == pat[i]:
			k += 1
		pnext[i] = k
	return pnext


def kmp_match(s, p, pnext):
	i, j = 0, 0
	pl = len(p)
	while j < pl:
		if s[i] != p[j]:
			i, j = i-pnext[j]+1, 0
		else:
			i, j = i+1, j+1
		if j == 0 and len(s[i:]) < pl:
			return -1
	return i - j + 1


if __name__ == '__main__':
#	expect: [0, 0, 1, 2, 3, 4, 0, 1]
#	s = 'abababca'
#	p = 'ca'
#	s = 'abcbcaba'
#	print(s)
#	print(partial_table(s))
#	print(partial_table2(s))
#	s = 'babcbabcabcaabcabcabcacabc'
#	p = 'abcabcacab'
	s = 'abcaaa32padrw'
	p = 'a32p'
	print(kmp_match(s, p, partial_table(p)))

