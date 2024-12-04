def loadMatrix(path: str) -> list[int]:
    
    with open(path, "r") as file:
        
        m = []
        
        lines = file.readlines()
        
        for line in lines:
            
            l = line.split(",")
            l.pop()
            
            for x in l:
                
                m.append(int(x))
        
        return m