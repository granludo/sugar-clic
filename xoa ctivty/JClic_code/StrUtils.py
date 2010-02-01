class StrUtils(object):
    
    def replace(self, str, pattern, replace):
        s = 0
        e = 0
        if(str == None):
            str = ""
        result = ""
        e = str.index(pattern)
        while(e >= 0):
            result.append(str[s:e])
            if(replace != None):
                result.append(replace)
            s = e+len(pattern)
        result.append(str[s:])
        return result[0:]
    
    def nullableString(self, o):
        result = ""
        if(o != None):
            result = str(o)
            if(len(result) == 0):
                result = None 
        return result