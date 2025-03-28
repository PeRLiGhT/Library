from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import Counter

# สิ่งพิมพ์
class Publication(ABC):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    @abstractmethod
    def display(self):
        pass

# หนังสือ
class Book(Publication):
    def __init__(self, title, author, year, isbn, category):
        super().__init__(title, author, year)
        self.isbn = isbn
        self.category = category

    def display(self):
        print(f"Book: {self.title}, Author: {self.author}, Year: {self.year}, ISBN: {self.isbn}, Category: {self.category}")

# สมาชิกห้องสมุด
class Member:
    def __init__(self, name, member_id, contact):
        self.name = name
        self.member_id = member_id
        self.contact = contact

    def display(self):
        print(f"Member ID: {self.member_id}, Name: {self.name}, Contact: {self.contact}")

# การยืม
class Loan:
    def __init__(self, member, publication):
        self.member = member
        self.publication = publication
        self.loan_date = datetime.now()
        self.due_date = self.loan_date + timedelta(days=14)

    def display(self):
        print(f"Loan - Member: {self.member.name}, Book: {self.publication.title}, Loan Date: {self.loan_date.date()}, Due Date: {self.due_date.date()}")

# ระบบจัดการห้องสมุด
class Library:
    def __init__(self):
        self.members = []
        self.publications = []
        self.loans = []
        self.loan_history = []  # เก็บประวัติการยืมทั้งหมด

    # เพิ่มสมาชิก
    def add_member(self, member):
        self.members.append(member)

    # เพิ่มหนังสือ
    def add_publication(self, publication):
        self.publications.append(publication)

    # ค้นหาข้อมูลสมาชิกหรือหนังสือ
    def search_library(self, query):
        member = next((m for m in self.members if m.member_id == query), None)
        publication = next((p for p in self.publications if p.title.lower() == query.lower()), None)

        if member:
            member.display()
            print("Books Borrowed:")
            borrowed_books = [loan.publication.title for loan in self.loans if loan.member.member_id == member.member_id]
            if borrowed_books:
                for book in borrowed_books:
                    print(f"- {book}")
            else:
                print("No books borrowed.")

        elif publication:
            publication.display()
            borrower = next((loan.member for loan in self.loans if loan.publication.title.lower() == publication.title.lower()), None)
            if borrower:
                print(f"Borrowed by: {borrower.name} (Member ID: {borrower.member_id})")
            else:
                print("Status: Available on shelf.")

        else:
            print("No matching member or book found.")

    # ยืมหนังสือ
    def loan_publication(self, member_id, title):
        member = next((m for m in self.members if m.member_id == member_id), None)
        pub = next((p for p in self.publications if p.title.lower() == title.lower()), None)

        if member and pub:
            if any(loan.publication.title.lower() == title.lower() for loan in self.loans):
                print(f"'{title}' is already borrowed.")
            else:
                loan = Loan(member, pub)
                self.loans.append(loan)
                self.loan_history.append(pub.title)  # ✅ บันทึกการยืมลง loan_history
                print(f"Loan successful: {member.name} borrowed '{pub.title}'.")
        else:
            print("Member or Publication not found.")

    # คืนหนังสือ
    def return_publication(self, title):
        for loan in self.loans:
            if loan.publication.title.lower() == title.lower():
                self.loans.remove(loan)
                print(f"Return successful: '{title}' returned.")
                return
        print("Loan not found.")

    # แสดงสิ่งพิมพ์ยอดนิยม
    def popular_books(self):
        print("\nPopular Books:")
        if not self.loan_history:
            print("No books have been borrowed yet.")
            return

        book_count = Counter(self.loan_history)
        sorted_books = book_count.most_common()

        for title, count in sorted_books:
            print(f"- {title}: Borrowed {count} times")

        # อัปเดตข้อมูลสมาชิก
    def update_member(self, member_id, new_name=None, new_contact=None):
        member = self.find_member(member_id)
        if member:
            if new_name:
                member.name = new_name
            if new_contact:
                member.contact = new_contact
            print(f"Member ID {member_id} updated successfully.")
        else:
            print("Member not found.")


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    lib = Library()

    # เพิ่มสมาชิก
    lib.add_member(Member("Alice", "123", "alice@example.com"))
    lib.add_member(Member("Bob", "456", "bob@example.com"))

    # เพิ่มหนังสือ
    lib.add_publication(Book("Python 101", "John Doe", 2020, "ISBN123456", "Programming"))
    lib.add_publication(Book("Data Science Essentials", "Jane Smith", 2021, "ISBN789101", "Data Science"))

    # ยืมหนังสือ
    lib.loan_publication("123", "Python 101")
    lib.loan_publication("456", "Python 101")
    lib.loan_publication("456", "Data Science Essentials")

    # ค้นหาข้อมูล
    while True:
        query = input("\nEnter Member ID or Book Title to search (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        lib.search_library(query)

    # แสดงหนังสือยอดนิยม
    lib.popular_books()
