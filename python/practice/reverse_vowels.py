class Solution(object):
    VOWELS = 'aeiou'
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        news = []
        dstack = {}
        
        for k, v in enumerate(s):
            if v in Solution.VOWELS:
                if not dstack:
                    dstack[k] =  v
                    news.append(v)
                else:
                   prik, priv =  dstack.popitem()
                   if prik <= len(news) - 1:
                        news[prik] = v
                   if k <= len(news) - 1:
                        news[k] = priv
                   else:
                        news.append(priv)
                   
                   dstack[k] = priv
            
            else:
                news.append(v)
        return ''.join(news)

if __name__ == '__main__':
	a = Solution()
	print(a.reverseVowels('hello'))
