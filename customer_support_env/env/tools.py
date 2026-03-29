def check_order_status(order_id):
    return f"Order {order_id} verified"

def refund_api(order_id, verified=True):
    return f"Refund processed for order {order_id}"

def tech_diagnostics(device_id):
    return f"Device {device_id} battery issue detected"

def escalate_to_human():
    return "Escalated to human agent"


def send_reset_link(method="email"):
    return f"Password reset link sent via {method}"


TOOLS = {
    "check_order_status": check_order_status,
    "refund_api": refund_api,
    "tech_diagnostics": tech_diagnostics,
    "escalate": escalate_to_human,
    "send_reset_link": send_reset_link
}
