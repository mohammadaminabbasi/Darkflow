
string = "۳۳ea a"
newstring = ''.join([i for i in string if not i.isdigit()])
print(newstring)