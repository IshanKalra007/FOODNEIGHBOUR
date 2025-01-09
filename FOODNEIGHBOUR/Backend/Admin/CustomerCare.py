from pip._internal.utils import subprocess
from sqlalchemy.orm import Session
from Backend.Class.User import User
from Backend.Class.CustomerSupport import CustomerSupport
from Backend.Admin.Login import role_required
import socket


@role_required('ADMIN')
def view_requests():
    session = Session()
    requests = session.query(CustomerSupport).all()
    session.close()
    return requests


server_process = None


def start_server_if_needed():
    global server_process
    if server_process is None:
        server_process = subprocess.Popen(['python', 'server.py'])


@role_required('ADMIN')
def send_message(user_id, message):
    session = Session()
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9999))
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            print(f"Message sent to {user.user_email}: {response}")
            client_socket.close()
            session.close()
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            session.close()
            return False
    else:
        session.close()
        return False


@role_required('ADMIN')
def extract_customer_info(user_id):
    session = Session()
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        customer_info = {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.user_email,
            'user_mobile': user.user_mobile,
            'user_postcode': user.user_postcode
        }
        session.close()
        return customer_info
    else:
        session.close()
        return None
