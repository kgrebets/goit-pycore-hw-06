from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise Exception("Name can't be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise Exception("Phone number must be 10 digits long")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone:str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone:str):
        ph = self.find_phone(phone) 
        index_to_delete = self.phones.index(ph) 
        self.phones.pop(index_to_delete)

    def edit_phone(self, old_phone:str, new_phone:str):
        for ind, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[ind] = Phone(new_phone)
                return
        raise Exception(f"No {old_phone} phone found for {self.name.value}")
    
    def find_phone(self, phone:str):
        for  ph in self.phones:
            if phone == ph.value:
                return ph
        raise Exception(f"No {ph} phone found for {self.name.value}")
    
class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name:str)->Record:
        item = self.data.get(name)
        if(item is None):
            raise Exception("Can't find item: " + name)
        return item
    
    def delete(self, name:str):
        if name in self.data:
            del self.data[name]
        else:
            raise Exception("Can't find item: " + name)
             
def print_all():
    print("\nAddress book:")
    for _, record in book.data.items():
        print(record)
    print()
    
#--------------------------------

try:
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("7777777777")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print_all()

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john.remove_phone("7777777777")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  

    book.delete("Jane")

    print_all()

except Exception as e:
    print(f'Error: {e}')