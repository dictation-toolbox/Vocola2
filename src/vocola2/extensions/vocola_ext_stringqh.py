from natlinkcore import nsformat

# QH, two string functions:
# extract part before the first ":" in String.GetName
# extract the latter part, so after the first ":" in String.GetPassword
# also: format _anything

# Vocola function: String.GetName
def getname(name):
    return name.split(":")[0]

# Vocola function: String.GetPassword
def getpassword(name):
    return name.split(":", 1)[1]

# Vocola function: String.NsformatCapitalize
def nsformatcapitalize(text):
    formattedOutput, _outputState = nsformat.formatString(text)   # starting no-space cap-next  
    return formattedOutput

# Vocola function: String.Capitalize
def capitalize(name):
    words = name.split()
    capped = ' '.join([w.capitalize() for w in words])
    return capped

if __name__ == "__main__":
    
    assert getname("name:password") == "name"
    assert getpassword("name:password") == "password"

    Text = "hello, THIS is a Test"
    assert nsformatcapitalize(Text) == "Hello, THIS is a Test"
    
    Text = "hi. I am doing well. how are you?"
    assert nsformatcapitalize(Text) == "Hi.  I am doing well.  How are you?"

    assert capitalize("quintijn hoogenboom") == "Quintijn Hoogenboom"
    
    
    
    