# from random import randint
# class Train:
#     def __init__(slf,trainNo):
#      slf.trainNo=trainNo
#     def book(slf,fro,to):
#         print(f"Ticket is booked in train no:{slf.trainNo}from{fro} to {to}")
#     def getStatus(slf):
#         print(f" train no:{slf.trainNo} is running on time")
#     def getFare(slf,fro,to):
#         print(f"Ticket fare in train no:{slf.trainNo}from{fro} to {to} is {randint(222,5555)}")
# t=Train(1299)
# t.book("Rampur","Delhi")
# t.getStatus()
# t.getFare("Rampur","Delhi")
from random import randint
class Train:
    def __init__(self,TrainNO):
        self.TrainNo=TrainNO
    def book(self,fro,to):
     print(f"Ticket is booked in TrainNo:{self.TrainNo}from {fro} to {to}")
    def getStatus(self):
       print(f"train no{self.TrainNo} is running on time")
    def getFare(self,fro,to):
       print(f"ticket fair in train no:{self.TrainNo} from {fro} to {to} is {randint(222,555)}")
t=Train(1053)
t.book("Mumbai","Delhi")
t.getStatus()
t.getFare("Mumbai","Delhi")
