import unittest
import sys
import os

# Navigate to parent directory 
parent_dir = os.path.abspath(os.path.join('..'))
sys.path.append(parent_dir)  

# Now imports will work
from app import app  

from models import ServiceTicket, User, db

class TestServices(unittest.TestCase):

  def setUp(self):
     self.app = app.test_client()

  # Rest of test cases

if __name__ == '__main__':
   unittest.main()

