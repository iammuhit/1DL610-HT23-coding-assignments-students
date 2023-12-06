def extract_author(str):
    parts = str.split(', ')
    if len(parts) == 1: #Only one element so it runs normally
        parts = str.split()
        if len(parts) == 1: #We only got the surname
            return parts[0], ''
        elif len(parts) == 2: #We got both surname and name
            return parts[-1], parts[0]
        else:   #Surname or name have multiple parts
            return parts[-1], ' '.join(parts[:-1])
    elif len(parts) == 2:   #There is a comma so we separate name and surname
        return parts[0], parts[1]

def extract_authors(str):
    list_of_authors = str.split(' and ')
    result = []
    for x in list_of_authors:
        parts = x.split(', ')
        if len(parts) == 1: #Only one element so it runs normally
            parts = [part.strip() for part in x.split()]
            if len(parts) == 1: #We only got the surname
                result.append((parts[0], ''))
            elif len(parts) == 2: #We got both surname and name
                result.append((parts[-1], parts[0]))
            else:   #Surname or name have multiple parts
                result.append((parts[-1], ' '.join(parts[:-1])))
        elif len(parts) == 2:   #There is a comma so we separate name and surname
            result.append((parts[0].strip(), parts[1].strip()))
    return result
