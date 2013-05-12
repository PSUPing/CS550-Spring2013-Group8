#!/usr/bin/env/python
import sys

#this class represents the memory system. Basically,
#it is a list of memory elemnts and then some methods
class Memory():
#initialize by making all of the memory one big list
#with each element pointing to the next and make the
#avail list point to the front of it
    def __init__(self,size):
        if type(size) is not int:
            raise Exception('Invalid type')
        self.memory=[]
        for i in range(size):
            self.memory.append(Mem_element(0,i-1))
            self.avail=i	
#this allows visualization of the the memory
    def __str__(self):
        s=''
        for i in self.memory:
            s= s+ str(i.first)+' '+str(i.second)+'\n'
        return s

#garbage collection. First mark everything that can be reached
#through the name table, then sweep the memory
#the extra field is so that if you are performing multiple 
#allocs before an assignment you dont accidently delete elements
#you already alloced just because they aren't pointed to yet
#also marks the avail list so that it doesn't get freed (this is for the
#strange case when gc is called when there is some memory left)
    def gc(self,indeces,extra={}):
        if type(indeces) is not dict or type(extra) is not dict:
            raise Exception('Invalid type')
        for i in indeces.values():
            if i.isPointer and i.element!=-1:
                self._mark(i.element)
        for i in extra.values():
            if i.isPointer and i.element!=-1:
                self._mark(i.element)
        self._mark(self.avail)
        self._sweep()
				
#this marks the given index if it is not already marked and then cals itself
#on the first and second elements in the pair if they are lists
    def _mark(self,index):
        if type(index) is not int:
            raise Exception('Invalid type')
        if not self.memory[index].marked and index!=-1:
            self.memory[index].marked=True
            if self.memory[index].Lfirst and self.memory[index].first!=-1:
                self._mark(self.memory[index].first)
            if self.memory[index].Lsecond and self.memory[index].second!=-1:
                self._mark(self.memory[index].second)

#iterate through the  memory. If something isn't marked then add it to
#avail, otherwise unmark it
    def _sweep(self):
        for i in range(len(self.memory)):
          if not self.memory[i].marked:
            self.memory[i].Lfirst=False
            self.memory[i].first=0
            self.memory[i].Lsecond=True
            self.memory[i].second=self.avail
            self.avail=i
          else:
            self.memory[i].marked=False

#returns true if the object is a Value representing an int
    def intp(self, value):
        if not isinstance(value,Value):
            raise Exception('Invalid type')
        if value.isPointer==False:
            return True
        return False

#returns true if the object is a Value representing a list
    def listp(self, value):
        if not isinstance(value,Value):
            raise Exception('Invalid type')
        if value.isPointer==True:
            return True
        return False

#returns true if the object is a Value representing the empty list
    def nullp(self,index):
        if not isinstance(index,Value):
            raise Exception('Invalid type')
        if index.element==-1 and  index.isPointer==True:
            return True
        return False

#returns the first element of the Value passed
    def car(self,index):
        if not isinstance(index,Value) or index.isPointer==False:
            raise Exception('Invalid type')
        if self.nullp(index):
            return index
        return Value(self.memory[index.element].first,self.memory[index.element].Lfirst)

#returns the second element of the Value passed
    def cdr(self,index):
        if not isinstance(index,Value) or index.isPointer==False:
            raise Exception('Invalid type')
        if self.nullp(index):
            return index
        return Value(self.memory[index.element].second,self.memory[index.element].Lsecond)

#adds the value to the front of the list represented by index
#calls gc if it can't find enough memory
    def cons(self,value,index,nt,extra={}):
        if not isinstance(value,Value) or not isinstance(index,Value) or index.isPointer==False:
            raise Exception('invalid type')
        if self.avail==-1:
            self.gc(nt,extra)
            if self.avail==-1:
                print 'Error out of memory'
                sys.exit(-1)
            return self.cons(value,index,nt,extra)
        else:
            newIndex=self.avail
            self.avail=self.memory[newIndex].second
            self.memory[newIndex].second=index.element
            self.memory[newIndex].Lsecond=True
            self.memory[newIndex].first=value.element
            self.memory[newIndex].Lfirst=value.isPointer
            return Value(newIndex,True)

#concatonate two lists by creating a duplicate of the first list and then
#pointing it to the second list (so that the first one doesn't get destoryed
#the second one won't sent there is not set-car or set-cdr.
#If the first element is ever a list then that is not duplicated and just
#pointed to, since it won't affect the list
    def concat(self,index1,index2,nt):
        if not isinstance(index1,Value) or not isinstance(index2,Value) or index1.isPointer==False or index2.isPointer==False:
            raise Exception('Invalid type')
        count=0
        l=[]
        currentIndex=index1.element
        while currentIndex!=-1:
            l.insert(0,Value(self.memory[currentIndex].first,self.memory[currentIndex].Lfirst))
            currentIndex=self.memory[currentIndex].second
            count+=1
            if count >= len(self.memory):
                print 'Error cannot concatenate to the end of a circular list'
                sys.exit(-1)
        for i in l:
            print i
            extra={'extra':Value(index2,True)}
            index2=self.cons(i,index2,nt,extra)	
        return index2
			
#elements in the memory array
class Mem_element():
    def __init__(self,element,pointer):
        self.first=element
        self.second=pointer
        self.Lfirst=False#first element is a list
        self.Lsecond=True#second element is a list
        self.marked=False

#these are the pointers into the array or integers
class Value():
    def __init__(self,element,isPointer):
        self.element=element
        self.isPointer=isPointer
    def __str__(self):
        return str(self.element)+' '+str(self.isPointer)
