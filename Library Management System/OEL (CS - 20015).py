# ======================= Main File =================================

# ----------------------- Import Projects ---------------------------------

from csv import *
import os
from datetime import *
from random import *



class DataStructures:
    
    @staticmethod
    def merge_sort(lst):
        if len(lst)>1:
            div = int(len(lst)/2)
        
            lst_1 = lst[:div]
            lst_2 = lst[div:]
            
            DataStructures.merge_sort(lst_1)
            DataStructures.merge_sort(lst_2)
            
            i = 0 #index for lst_1
            j = 0 #index for lst_2
            k = 0 #index for lst
            
            while i<len(lst_1) and j<len(lst_2):
                if lst_1[i]<lst_2[j]:
                    lst[k] = lst_1[i]
                    i+=1
                else:
                    lst[k] = lst_2[j]
                    j+=1
                k+=1
                
            while i<len(lst_1):
                lst[k] = lst_1[i]
                i+=1
                j+=1
            
            while j<len(lst_2):
                lst[k] = lst_2[j]
                j+=1
                k+=1
                
        
                
                
    @staticmethod
    def search_book(arr, book):
        beg = 0 
        end = len(arr)-1
        
        mid = int((beg+end)/2) 
        
        while beg<end and arr[mid][0]!=book:
            if arr[mid][0]<book:
                beg = mid+1
            else:
                end = mid-1
            mid = int((end+beg)/2)
        
        if arr[mid][0] == book:
            return mid
        else:
            print("No book found")
            return



class Library:
    
    def __init__(self):
        
        print(f"{'*'*25} Welcome To Library Management System {'*'*25}")
        
        print("""
              Please select the Login type:
              1. Member's Account
              2. Student's Account
              3. Exit""", )
        
        account_type = self.selection_checker("select the desired option: ", 3)
        
        if account_type == 1:
            self.admin_login()
        elif account_type==2:
            self.student_login()
        else:
            exit()
        
    
    @staticmethod
    def selection_checker(statement, max_number):
        option = input(f"{statement}: ")
        while True:
            if int(option)>max_number:
                option = input("Please select the correct option: ")
            else:
                return int(option)
    
    def student_login(self):
        students = self.data_reader("Students")
        user = None
        while True:
            st_id = input("Enter student id: ")
            st_pass = input("Enter student password: ")
            if any(i[1]==st_id and i[2]==st_pass for i in students):
                user = st_id    
                break
            else:
                print("Enter correct user information")
        StudentPortal(user)
    
    def admin_login(self):
        while True:
            user = input("Enter user id of member: ")
            password = input("Enter Password for member: ")
            if user=="library":
                if password=="12345":
                    break
                else:
                    print("Enter correct password")
            else:
                print("Enter correct username")
        AdminPortal()
        
        
    
    
    @staticmethod
    def data_reader(filename="", error="Enter the correct file name"):
        
        while True:
            if os.path.exists(filename+".csv"):
                with open(f"{filename}.csv","r+") as f:
                    content = reader(f)
                    data = []
                    for i in content:
                            data.append(i)
                for i in range(len(data)):
                    
                    data[i] = list(filter(lambda x :x!=" " , data[i]))
                return data
            else:
                print(error)
                filename = input("Enter File name again: ")
    
                

class StudentPortal:
    
    def __init__(self, username):
        
        # ------------------------- variables ----------------------------
        
        self.username = username
        self.date = datetime.now()
        self.date_today = f"{self.date.day}/{self.date.month}/{self.date.year}"
        self.days_after = self.date+timedelta(7)
        self.date_after = f"{self.days_after.day}/{self.days_after.month}/{self.days_after.year}"
        
        # ------------------------- program -----------------------
        print()
        print(f"{'*'*25} Student Portal {'*'*25}")
        print()
        
        
        while True:
            print("""
Select the desired option:
    1. Check all the available books
    2. Borrow a book
    3. Check your borrowed book
    4. Renew a book
    5. Reserve a book
    6. Return a book
    7. Logout""")
            student_option = Library.selection_checker("Enter the option number", 7)
            print()
            if student_option==1:
                self.see_all_books()
            elif student_option==2:
                self.borrow_book()
            elif student_option==3:
                self.check_borrowed_books()
            elif student_option==4:
                self.renew_book()
            elif student_option==5:
                self.reserve_book()
            elif student_option==6:
                self.return_book()
            elif student_option==7:
                Library()
                break
                 
    
    def see_all_books(self):
        print()
        if os.path.exists("Book Record.csv"):
            data = Library.data_reader(filename="Book Record", error="Enter the correct file name")
            
            print(
f"""{'S.No':5}{'Book id':10}{'Book Name':30}{'Author Name':25}{'Subject':22}{'Publication Date':20}{'Quantity':8}"""
            )
            print("-"*120)
            for i in range(len(data)):
                print()
                print(
f"{str(i+1):5}{data[i][0]:10}{data[i][1]:30}{data[i][2]:25}{data[i][3]:26}{data[i][4]:20}{data[i][5]:8}"
)
                print("_"*120)

    def borrow_book(self):
        
        book_id = input("Enter the book id for the book you want to borrow: ")
        books = Library.data_reader(filename="Book Record", error="Enter the correct file name")
        book_ind = book_ind = DataStructures.search_book(books, book_id)
        if type(book_ind)==int:
            book = books[book_ind]
            borrow_book_data = [book[0], " ", book[1], " ", book[2], " ", book[3], " ", self.date_today, " ", self.date_after]
            if os.path.isdir("borrowed books"):
                if os.path.exists(f"borrowed books/{self.username}.csv"):
                    data = Library.data_reader(filename=f"borrowed books/{self.username}")
                    for i in data:
                        for j in range(1, (len(i)*2)-2, 2):
                            i.insert(j, " ")
                    data.append(borrow_book_data)
                    DataStructures.merge_sort(data)
                    with open(f"borrowed books/{self.username}.csv", "w+") as f:
                        pass
                    for dat in data:
                        AdminPortal.data_adder(filename=f"borrowed books/{self.username}", data=dat)
                else:
                    AdminPortal.data_adder(filename=f"borrowed books/{self.username}", data=borrow_book_data)
                    
            else:
                os.mkdir("borrowed books")
                AdminPortal.data_adder(filename=f"borrowed books/{self.username}", data=borrow_book_data)
        print("Book borrowed successfully")
    
    def check_borrowed_books(self):
        if os.path.exists(f"borrowed books/{self.username}"+".csv"):
            data = Library.data_reader(f"borrowed books/{self.username}")
            print(
f"""{'S.No':5}{'Book id':10}{'Book Name':30}{'Author Name':30}{'Subject':15}{'Date issued':20}{'Date return':20}"""
            )
            print("-"*121)
            for i in range(len(data)):
                print(f"{str(i+1):5}{data[i][0]:10}{data[i][1]:30}{data[i][2]:30}{data[i][3]:15}{data[i][4]:20}{data[i][5]:8}")
    
    def renew_book(self):
        
        book_id = input("Enter book id to renew: ")
        if os.path.exists(f"borrowed books/{self.username}.csv"):
            books = Library.data_reader(f"borrowed books/{self.username}")
            for i in books:
                for j in range(1, (len(i)*2)-2, 2):
                    i.insert(j, " ")
            book_ind = book_ind = DataStructures.search_book(books, book_id)
            book = books[book_ind]
            dated = list(map(int,book[-1].split("/")))
            dated = date(dated[2], dated[1], dated[0]) + timedelta(7)
            book[-1] = f"{dated.day}/{dated.month}/{dated.year}"
            books[book_ind] = book
            DataStructures.merge_sort(books)
            with open(f"borrowed books/{self.username}.csv", "w+") as f:
                pass
            for dat in books:
                AdminPortal.data_adder(filename=f"borrowed books/{self.username}", data=dat)
                        
            
            print("Successfully renewed the book")
            
        else:
            print("Issue your book first")
        
    def reserve_book(self):
        
        book_id = input("Enter book id to reserve: ")
        data_books = Library.data_reader("Book Record")
        book_ind = DataStructures.search_book(data_books, book_id)
        book = data_books[book_ind]
        if os.path.exists("Reserved Books.csv"):
            data = Library.data_reader("Reserved Books")
            data.append([book[0], book[1], book[2], self.username, self.date_today])
            DataStructures.merge_sort(data)
            for i in data:
                for j in range(1, (len(i)*2)-2, 2):
                    i.insert(j, " ")
            with open("Reserved Books.csv", "w+") as f:
                pass
            for dat in data:
                AdminPortal.data_adder("Reserved Books", data=dat)
        
        print("You reserved the book")

    def return_book(self):
        book_id = input("Enter the book id to return: ")
        books = Library.data_reader(filename=f"borrowed books/{self.username}", error="Enter the correct file name")
        book_ind = book_ind = DataStructures.search_book(books, book_id)
        if type(book_ind)==int:
            books.pop(book_ind)
            DataStructures.merge_sort(books)
            with open(f"borrowed books/{self.username}.csv", "w+") as f:
                pass
            for dat in books:
                AdminPortal.data_adder(filename=f"borrowed books/{self.username}", data=dat)
            print("Book removed successfully")
        else:
            print("Issue a book first")
        

class AdminPortal:
    
    def __init__(self):
        
        # ------------------------- variables ----------------------------
        
        self.date = datetime.now()
        self.date_today = f"{self.date.day}/{self.date.month}/{self.date.year}"
        
        # ------------------------- program ------------------------------
        
        print()
        print(f"{'*'*25} Admin Portal {'*'*25}")
        
        while True:
            print()
            print("""
Select your desired operation:
    1. Add a new book
    2. Add new student
    3. Remove Book
    4. Edit book data
    5. Search Book
    6. See all the available books
    7. Logout""")
            print()
            admin_option = Library.selection_checker("Enter the option number", 7)
            if admin_option==1:
                self.add_book()
            elif admin_option==2:
                self.add_student()
            elif admin_option==3:
                self.remove_book()
            elif admin_option==4:
                self.edit_book_data()
            elif admin_option==5:
                self.search_book()
            elif admin_option==6:
                self.see_all_book()
            elif admin_option==7:
                Library()
                break
           
    def add_book(self):
        
        book_id = input("Enter the book id: ")
        book_name = input("Enter the name of the book: ")
        author_name = input("Enter the author name of the book: ")
        subject_name = input("Enter the Subject of the book: ")
        pub_date = self.date_today
        quantity = input("Enter the total number of books to publish: ")
        if os.path.exists("Book Record.csv"):
            data = Library.data_reader(filename="Book Record", error="Enter the correct file name")
            for i in data:
                for j in range(1, (len(i)*2)-2, 2):
                    i.insert(j, " ")
            data.append([book_id, " ", book_name, " ", author_name, " ", subject_name, " ", pub_date, " ", quantity])
            main_data = data
            DataStructures.merge_sort(main_data)
            with open("Book Record.csv", "w+") as f:
                pass
            for dat in main_data:
                self.data_adder(filename="Book Record", error="Please close the file first", data=dat)
        
        else:
            main_data = [book_id, " ", book_name, " ", author_name, " ", subject_name, " ", pub_date, " ", quantity]
            self.data_adder(filename="Book Record", error="Please close the file first", data=main_data)
        
        print("Book added successfully")
        

    def see_all_book(self):
        print()
        if os.path.exists("Book Record.csv"):
            data = Library.data_reader(filename="Book Record", error="Enter the correct file name")
            
            print(
f"""{'S.No':5}{'Book id':10}{'Book Name':30}{'Author Name':25}{'Subject':22}{'Publication Date':20}{'Quantity':8}"""
            )
            print("-"*120)
            for i in range(len(data)):
                print()
                print(
f"{str(i+1):5}{data[i][0]:10}{data[i][1]:30}{data[i][2]:25}{data[i][3]:26}{data[i][4]:20}{data[i][5]:8}"
)
                print("_"*120)
                
    def add_student(self):
        student_name = input("Enter the student name: ")
        student_id = input("Enter the student id: ")
        student_password = input("Enter password for student id: ")
        if os.path.exists("Students.csv"):
            data = Library.data_reader(filename="Students", error="Enter the correct file name")
            for i in data:
                for j in range(1, (len(i)*2)-2, 2):
                    i.insert(j, " ")
            data.append([student_name, " ", student_id, " ", student_password])
            main_data = data
            DataStructures.merge_sort(main_data)
            with open("Students.csv", "w+") as f:
                pass
            for dat in main_data:
                self.data_adder(filename="Students", error="Please close the file first", data=dat)
        else:
            main_data = [student_name, " ", student_id, " ", student_password]
            self.data_adder(filename="Students", error="Please close the file first", data=main_data)
        
        print("Student Successfully added")
        
    def remove_book(self):
        
        book_id = input("Enter book id to remove that book: ")
        data = Library.data_reader(filename="Book Record", error= "No file found")
        data = list(filter(lambda x: x[0]!=book_id, data))
        for i in data:
            for j in range(1, (len(i)*2)-2, 2):
                i.insert(j, " ")
        with open("Book Record.csv", "w+") as f:
            pass
        for dat in data:
            self.data_adder(filename="Book Record", error="Close the file", data=dat)
        print("Book successfully removed")
        
    def edit_book_data(self):
        
        book_id = input("Enter book id to edit the book: ")
        books = Library.data_reader("Book Record")
        for i in books:
            for j in range(1, (len(i)*2)-2, 2):
                i.insert(j, " ")
        book = DataStructures.search_book(books, book_id)
        book_name = input("Enter the name of the book: ")
        author_name = input("Enter the author name of the book: ")
        subject_name = input("Enter the Subject of the book: ")
        pub_date = self.date_today
        quantity = input("Enter the total number of books to publish: ")
        books[book] = [book_id, " ", book_name, " ", author_name, " ", subject_name, " ", pub_date, " ", quantity]
        with open("Book Record.csv", "w+") as f:
            pass
        for dat in books:
            self.data_adder(filename="Book Record", data=dat)
        print("Book edited successfully")
        
    def search_book(self):
        book_id = input("Enter the book id to search: ")
        books = Library.data_reader("Book Record")       
        book_ind = DataStructures.search_book(books, book_id)
        if type(book_ind)==int:
            book = books[book_ind]
            print(f"{'Book id':10}{'Book Name':30}{'Author Name':30}{'Subject':15}{'Publication Date':20}{'Quantity':8}")
            print("-"*115)
            i = book
            print(f"{i[0]:10}{i[1]:30}{i[2]:30}{i[3]:15}{i[4]:20}{i[5]:8}")
            
         
    
   
   
    @staticmethod
    def data_adder(filename="", error="Close the file", data=[]):
        try:
           
            with open(f"{filename}.csv","a+",newline="") as file:
                write = writer(file)
                write.writerow(data)

            
        except:
            print(error)        
        
        

if __name__ == '__main__':

    a = Library()