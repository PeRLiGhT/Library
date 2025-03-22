from abc import ABC, abstractmethod

# รหัสสมาชิก ชื่อสมาชิก
class Member:
    def __init__(self, member_id, name, contact):
        self.member_id = member_id
        self.name = name
        self.contact = contact

    def display(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Contact: {self.contact}"

#ชื่อหนังสือ ผู้เขียน ประเภท
class Publication(ABC):
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category

    @abstractmethod
    def display(self):
        pass

#หนังสือ รหัส ISBN(หมายเลขประจำหนังสือมาตรฐานสากล)
class Book(Publication):
    def __init__(self, title, author, category, isbn):
        super().__init__(title, author, category)
        self.isbn = isbn

    def display(self):
        return f"Book: {self.title}, Author: {self.author}, Category: {self.category}, ISBN: {self.isbn}"

#ยืม
class Loan:
    def __init__(self, member, publication, rent_date, due_date):
        self.member = member
        self.publication = publication
        self.rent_date = rent_date
        self.due_date = due_date

    def display(self):
        return f"{self.member.name} borrowed '{self.publication.title}' rent on '{self.rent_date}' due on {self.due_date}"

#ห้องสมุด
class Library:
    def __init__(self):
        self.members = []
        self.publications = []
        self.loans = []
    
    def add_member(self, member):
        self.members.append(member)
    
    def find_member(self, member_id):
        return next((m for m in self.members if m.member_id == member_id), None)
    
    def display_member_details(self, member_id):
        member = self.find_member(member_id)
        return member.display() if member else "Member not found."
    
    def update_member(self, member_id, name=None, contact=None):
        member = self.find_member(member_id)
        if member:
            if name:
                member.name = name
            if contact:
                member.contact = contact
            return "Member information updated."
        return "Member not found."
    
    def add_publication(self, publication):
        self.publications.append(publication)
    
    def find_publication(self, title=None, author=None, category=None):
        results = [p for p in self.publications if (title and p.title == title) or (author and p.author == author) or (category and p.category == category)]
        return results if results else "No matching publications found."
    
    def display_publication_details(self, title):
        publication = next((p for p in self.publications if p.title == title), None)
        return publication.display() if publication else "Publication not found."
    
    def update_publication(self, title, new_title=None, new_author=None, new_category=None):
        publication = next((p for p in self.publications if p.title == title), None)
        if publication:
            if new_title:
                publication.title = new_title
            if new_author:
                publication.author = new_author
            if new_category:
                publication.category = new_category
            return "Publication information updated."
        return "Publication not found."
    
    def issue_loan(self, member_id, publication_title, rent_date, due_date):
        member = self.find_member(member_id)
        publication = next((p for p in self.publications if p.title == publication_title), None)
        
        if member and publication:
            loan = Loan(member, publication,rent_date, due_date)
            self.loans.append(loan)
            return "Loan issued successfully."
        return "Member or Publication not found."
    
    def return_loan(self, member_id, publication_title):
        loan = next((l for l in self.loans if l.member.member_id == member_id and l.publication.title == publication_title), None)
        if loan:
            self.loans.remove(loan)
            return "Publication returned successfully."
        return "Loan record not found."
    
    def display_loans(self, member_id=None, publication_title=None):
        if member_id:
            return [loan.display() for loan in self.loans if loan.member.member_id == member_id]
        if publication_title:
            return [loan.display() for loan in self.loans if loan.publication.title == publication_title]
        return [loan.display() for loan in self.loans]
        return [loan.display() for loan in self.loans]

    def overdue_loans(self, current_date):
        return [loan.display() for loan in self.loans if loan.due_date < current_date]
    
    def popular_publications(self):
        from collections import Counter
        count = Counter(loan.publication.title for loan in self.loans)
        return count.most_common()

if __name__ == "__main__":
    lib = Library()
    
    # Adding Members
    m1 = Member(1, "Pream", "pream@example.com")
    lib.add_member(m1)
    
    # Adding Books
    b1 = Book("Python Basics", "John Doe", "Programming", "1234567890")
    lib.add_publication(b1)
    
    # Issuing a Loan
    print(lib.issue_loan(1, "Python Basics", "2025-04-01", "2025-04-02"))
    
    # Displaying Loans
    print(lib.display_loans())
    
    # Returning a Loan
    print(lib.return_loan(1, "Python Basics"))
    
    # Displaying Loans after return
    print(lib.display_loans())
    
    # Finding and displaying member details
    print(lib.display_member_details(1))
    
    # Updating member information
    print(lib.update_member(1, name="Pream Smith", contact="Pream.smith@example.com"))
    print(lib.display_member_details(1))
    
    # Searching for a book
    print(lib.find_publication(title="Python Basics"))
    
    # Displaying book details
    print(lib.display_publication_details("Python Basics"))
    
    # Updating book information
    print(lib.update_publication("Python Basics", new_author="Jane Doe"))
    print(lib.display_publication_details("Python Basics"))
    
    # Generating overdue loans report
    print("Overdue Loans:", lib.overdue_loans("2025-04-02"))
    
    # Displaying popular publications
    print("Popular Publications:", lib.popular_publications())