class encoding:
    
    def __init__(self, query):
        self.query = query

    def getBytes(query):
        count = 0
        query_sep = query.split(" ")
        for string in query_sep:
            if string.isdigit():
                count = count + 4
            else:
                count = count + len(string)
        return count