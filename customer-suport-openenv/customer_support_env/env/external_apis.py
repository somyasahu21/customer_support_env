import time
import random

def verify_payment(order_id):
    time.sleep(0.5)
    return {
        "status": "verified",
        "order_id": order_id
    }


def process_refund(order_id):
    time.sleep(0.5)
    return {
        "status": "success",
        "refund_id": f"rf_{random.randint(1000,9999)}"
    }


def send_auth_otp(user_id):
    return {
        "status": "otp_sent",
        "user_id": user_id
    }