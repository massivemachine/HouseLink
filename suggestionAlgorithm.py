from random import choice
from database import *
from statistics import stdev,mean
class HouseTinder():
    def __init__(self):
        self.rightHouseIds = set()
        self.leftHouseIds = set()
        self.unseenIds = set()
        self.rightPrices = []
        self.rightNumBeds = []
        self.rightNumBaths = []
        self.priceStdDev = 0
        self.numBedsStdDev = 0
        self.numBathsStdDev = 0
        self.priceMean = 0
        self.numBedsMean = 0
        self.numBathsMean = 0

    def get_seen_house_ids(self) -> set:
        return self.rightHouseIds.union(self.leftHouseIds)
    
    def append_right(self,id:int) -> None:
        self.rightHouseIds.add(id)
        connect_db()
        data = get_info(id)
        close_db()
        self.rightPrices.append(data[4])
        self.rightNumBeds.append(data[2])
        self.rightNumBaths.append(data[3])
        if len(self.rightHouseIds) > 1:
            self.priceStdDev = stdev(self.rightPrices)
            self.numBedsStdDev = stdev(self.rightNumBeds)
            self.numBathsStdDev = stdev(self.rightNumBaths)
            self.priceMean = mean(self.rightPrices)
            self.numBedsMean = mean(self.rightNumBeds)
            self.numBathsMean = mean(self.rightNumBaths)
        return

    def append_left(self,id:int) -> None:
        self.leftHouseIds.add(id)
        return
    
    def populate_unseen_houses_set(self) -> None:
        connect_db()
        ids = set(get_ids())
        close_db()
        self.unseenIds = ids - self.get_seen_house_ids()#unseen ids = all ids set minus seen ids
        return
    
    def get_id_of_closest_item_to_mean(self,idArray:list,index:int,mean:any):
        closestToMean = 100000000000
        closestToMeanIndex = -1
        connect_db()
        for i in range(len(idArray)):
            currVal = get_info(idArray[i])[index]
            if abs(currVal - mean) < closestToMean:
                closestToMean = currVal
                closestToMeanIndex = i
        close_db()
        return idArray[closestToMeanIndex]#throwing a value error here means you need to adjust your closest price to mean initial value

    def choose_house(self,idArray:list) -> int:#make this an actual algorithm at some point
        if len(self.rightHouseIds) < 1:
            return choice(idArray)
        if self.priceStdDev > self.numBedsStdDev and self.priceStdDev > self.numBathsStdDev:
            #price is most important - show entry closest to mean
            return self.get_id_of_closest_item_to_mean(idArray,4,self.priceMean)

        elif self.numBathsStdDev > self.numBedsStdDev and self.numBathsStdDev > self.priceStdDev:
            #baths is most important
            return self.get_id_of_closest_item_to_mean(idArray,3,self.numBathsMean)
        
        elif self.numBedsStdDev > self.numBathsStdDev and self.numBedsStdDev > self.priceStdDev:
            #beds is most important
            return self.get_id_of_closest_item_to_mean(idArray,2,self.numBedsMean)
        
        elif self.priceStdDev > self.numBedsStdDev and self.priceStdDev == self.numBathsStdDev:
            #price and baths are equally important
            priceCandidate = self.get_id_of_closest_item_to_mean(idArray,4,self.priceMean)
            bathCandidate = self.get_id_of_closest_item_to_mean(idArray,3,self.numBathsMean)
            return choice([priceCandidate,bathCandidate])
        
        elif self.priceStdDev > self.numBathsStdDev and self.priceStdDev == self.numBedsStdDev:
            #price and beds are equally important
            priceCandidate = self.get_id_of_closest_item_to_mean(idArray,4,self.priceMean)
            bedCandidate = self.get_id_of_closest_item_to_mean(idArray,2,self.numBedsMean)
            return choice([priceCandidate,bedCandidate])

        elif self.numBedsStdDev > self.priceStdDev and self.numBedsStdDev == self.numBathsStdDev:
            #beds and baths are equally important
            bathCandidate = self.get_id_of_closest_item_to_mean(idArray,3,self.numBathsMean)
            bedCandidate = self.get_id_of_closest_item_to_mean(idArray,2,self.numBedsMean)
            return choice([bathCandidate,bedCandidate])

        else:
            #all are equally important
            return choice(idArray)
        
            
        

    def get_house_to_display(self) -> list:
        displayId = self.choose_house(list(self.unseenIds))
        connect_db()
        row = get_info(displayId)#change this line when relevant method is done
        close_db()
        return row

    def get_next_house(self) -> list:
        self.populate_unseen_houses_set()
        if len(self.unseenIds) == 0:
            return []
        return self.get_house_to_display()
    










    



    

    


