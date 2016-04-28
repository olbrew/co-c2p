from HelloListener import HelloListener

class KeyPrinter(HelloListener):     
    def enterR(self, ctx):         
        print("enterR") 
        
    def exitR(self, ctx):         
        print("exitR") 
