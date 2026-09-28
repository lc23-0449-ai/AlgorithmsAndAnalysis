#Toby Strawser

class HorspoolStringMatcher:

    def __init__(self,pattern):
        self.pattern = pattern
        self.dict = {}
        for i in range(len(self.pattern) - 1):
            self.dict[self.pattern[i]] = len(self.pattern) - i - 1

    # The pattern is provided as an argument to the initializer,
    # which creates the shift table. The text is provided as an argument to match,
    # which returns the first index where the pattern appears in the text,
    # or -1 if it does not appear.
    def match(self,text):
        skip = 0
        while skip <= len(text) - len(self.pattern):
            if self.str_comp(text[skip:],self.pattern,len(self.pattern)):
                return skip
            skip += self._get_shift(text[skip + len(self.pattern) - 1])
        return -1

    def str_comp(self,str1,str2,leng):
        i = leng -1
        while str1[i] == str2[i]:
            if i == 0:
                return True
            i = i -1
        return False

    #takes a character and returns the shift value for that character.
    def _get_shift(self,char):
        return self.dict.get(char, len(self.pattern))
        pass
