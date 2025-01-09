from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomerSupport(Base):  # Linked to the customer support table in the database
    __tablename__ = 'Customer_Support'

    Email = Column(String)  # Associated columns mapped to those in the database
    Support_Id = Column(Integer, primary_key=True)
    Contact_Us = Column(String)
    Issue_Description = Column(String)

    def __init__(self, email, contact_us, issue_description):
        self.Email = email
        self.Contact_Us = contact_us
        self.Issue_Description = issue_description

    def file_complaint(self, session, description):
        "File a new complaint"
        self.issue_description = description
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"<CustomerSupport(support_id={self.support_id}, user_id={self.user_id})>"
