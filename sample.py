
class Sample:
    def challenge(self, conts):
        if conts % 2 == 0:
            return True
        else:
            return False
        

    def main(self):
        current_conts = 1
        while True:
            if not self.challenge(current_conts):
                current_conts = current_conts + 1
                continue
            else:
                break
        
        return current_conts







        