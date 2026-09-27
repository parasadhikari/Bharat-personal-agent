from datetime import date


def check_healthcare_status(user_id):

    if user_id != "demo_user":
        raise ValueError("Invalid user ID")

    return {
        "scheme": "Ayushman Bharat",
        "status": "Eligible",
        "last_checked": str(date.today()),
        "source": "DEMO MOCK API"
    }


def get_document_status(document_id):

    if not document_id:
        raise ValueError("Document ID required")

    return {
        "document": "Aadhaar",
        "status": "Verified",
        "document_id": document_id,
        "source": "DEMO MOCK API"
    }


def check_payment_status(transaction_id):

    if not transaction_id:
        raise ValueError("Transaction ID required")

    return {
        "transaction_id": transaction_id,
        "status": "SUCCESS",
        "amount": "₹500",
        "source": "DEMO MOCK API"
    }


def save_user_preference(key, value):
    from memory import save_preference

    save_preference(key, value)

    return {
        "success": True,
        "key": key,
        "value": value
    }


def get_user_preference(key):
    from memory import get_preference

    value = get_preference(key)

    return {
        "key": key,
        "value": value
    }
TOOL_DEFINITIONS = [

    {
        "name": "check_healthcare_status",
        "description": "Checks demo healthcare eligibility information",
        "requires_permission": True
    },

    {
        "name": "get_document_status",
        "description": "Checks demo document verification status",
        "requires_permission": True
    },

    {
        "name": "check_payment_status",
        "description": "Checks demo payment transaction status",
        "requires_permission": True
    },

    {
        "name": "save_user_preference",
        "description": "Stores a non-sensitive user preference locally",
        "requires_permission": False
    },

    {
        "name": "get_user_preference",
        "description": "Retrieves a locally stored user preference",
        "requires_permission": False
    }
]