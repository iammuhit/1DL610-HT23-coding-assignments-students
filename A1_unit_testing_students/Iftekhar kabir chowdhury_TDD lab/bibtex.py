def extract_author(str):
    if(str.find(',')!=-1):
        names = str.split(',')
        Firstnames = ''.join(names[1:])
        Firstnames = names[1].strip()
        Surname = names[0]
        return Surname,Firstnames
    else:
        names = str.split()
        if len(names) == 2:
            Surname, FirstNames = names
            return FirstNames, Surname
        elif len(names) == 3:
            Firstnames =' '.join(names[0: 2])
            Surname =names[2]
            return Surname,Firstnames
        return(str,"")

def extract_authors(str):
    names = str.split('and')
    Aurthors=[]
    Aurthors.append(extract_author(names[0].strip()))
    Aurthors.append(extract_author(names[1].strip()))
    return Aurthors