from tools import (
    check_healthcare_status,
    get_document_status,
    check_payment_status,
    save_user_preference,
    get_user_preference
)

from permissions import PermissionManager
from memory import save_interaction
from model_provider import DemoModelProvider, LocalSLMProvider


class Agent:

    def __init__(self):

        # Permission manager
        self.permission_manager = PermissionManager()

        # Stores requests waiting for permission
        self.pending_requests = {}

        # Intent detection model
        self.model = DemoModelProvider()

        # Local SLM for general responses
        self.response_model = LocalSLMProvider()

    # ===================================
    # MAIN AGENT PROCESS
    # ===================================

    def process(self, message, user_id):

        # Detect intent
        intent = self.model.detect_intent(message)

        activity = [
            "User request received",
            f"Intent detected → {intent}"
        ]

        # ===================================
        # USER PREFERENCE / MEMORY
        # ===================================

        if intent == "save_user_preference":

            value = "short answers"

            if (
                "short" in message.lower()
                or "concise" in message.lower()
            ):
                value = "short answers"

            save_user_preference(
                "response_style",
                value
            )

            response = (
                "Got it. I'll remember that you prefer short answers."
            )

            save_interaction(
                message,
                response
            )

            activity.append(
                "Memory updated"
            )

            activity.append(
                "Interaction saved to local memory"
            )

            return {
                "message": response,
                "intent": intent,
                "permission_required": False,
                "activity": activity
            }

        # ===================================
        # HEALTHCARE
        # ===================================

        if intent == "healthcare_status":

            permission_id = "healthcare_access"

            if not self.permission_manager.allowed(
                permission_id
            ):

                self.pending_requests[user_id] = {
                    "message": message,
                    "intent": intent
                }

                activity.append(
                    "Permission required"
                )

                return {
                    "message":
                        "I need your permission to access your healthcare information.",
                    "intent": intent,
                    "permission_required": True,
                    "permission_id": permission_id,
                    "activity": activity
                }

            activity.append(
                "Permission granted"
            )

            activity.append(
                "Tool → check_healthcare_status"
            )

            try:

                result = check_healthcare_status(
                    user_id
                )

                activity.append(
                    "Tool response received"
                )

                response = (
                    f"You are {result['status']} "
                    f"according to the demo healthcare data."
                )

            except Exception as error:

                response = (
                    f"Healthcare tool failed: {str(error)}"
                )

                activity.append(
                    "Tool execution failed"
                )

            save_interaction(
                message,
                response
            )

            activity.append(
                "Interaction saved to local memory"
            )

            return {
                "message": response,
                "intent": intent,
                "permission_required": False,
                "activity": activity
            }

        # ===================================
        # DOCUMENT
        # ===================================

        if intent == "document_status":

            permission_id = "document_access"

            if not self.permission_manager.allowed(
                permission_id
            ):

                self.pending_requests[user_id] = {
                    "message": message,
                    "intent": intent
                }

                activity.append(
                    "Permission required"
                )

                return {
                    "message":
                        "I need your permission to access your document information.",
                    "intent": intent,
                    "permission_required": True,
                    "permission_id": permission_id,
                    "activity": activity
                }

            activity.append(
                "Permission granted"
            )

            activity.append(
                "Tool → get_document_status"
            )

            try:

                result = get_document_status(
                    "demo-aadhaar"
                )

                activity.append(
                    "Tool response received"
                )

                response = (
                    f"Your document is {result['status']} "
                    f"according to the demo data."
                )

            except Exception as error:

                response = (
                    f"Document tool failed: {str(error)}"
                )

                activity.append(
                    "Tool execution failed"
                )

            save_interaction(
                message,
                response
            )

            activity.append(
                "Interaction saved to local memory"
            )

            return {
                "message": response,
                "intent": intent,
                "permission_required": False,
                "activity": activity
            }

        # ===================================
        # PAYMENT
        # ===================================

        if intent == "payment_status":

            permission_id = "payment_access"

            if not self.permission_manager.allowed(
                permission_id
            ):

                self.pending_requests[user_id] = {
                    "message": message,
                    "intent": intent
                }

                activity.append(
                    "Permission required"
                )

                return {
                    "message":
                        "I need your permission to access your payment information.",
                    "intent": intent,
                    "permission_required": True,
                    "permission_id": permission_id,
                    "activity": activity
                }

            activity.append(
                "Permission granted"
            )

            activity.append(
                "Tool → check_payment_status"
            )

            try:

                result = check_payment_status(
                    "demo-txn-123"
                )

                activity.append(
                    "Tool response received"
                )

                response = (
                    f"Payment status: {result['status']} "
                    f"for {result['amount']}."
                )

            except Exception as error:

                response = (
                    f"Payment tool failed: {str(error)}"
                )

                activity.append(
                    "Tool execution failed"
                )

            save_interaction(
                message,
                response
            )

            activity.append(
                "Interaction saved to local memory"
            )

            return {
                "message": response,
                "intent": intent,
                "permission_required": False,
                "activity": activity
            }

        # ===================================
        # GENERAL REQUEST → LOCAL SLM
        # ===================================

        if intent == "general":

            try:

                # generate_response now returns:
                # {
                #     "text": "...",
                #     "latency": 3.32
                # }
                slm_result = self.response_model.generate_response(
                    message
                )

                response = slm_result["text"]

                latency = slm_result["latency"]

                activity.append(
                    "Local SLM → Qwen 2.5 0.5B"
                )

                activity.append(
                    f"SLM latency → {latency:.2f}s"
                )

            except Exception as error:

                response = (
                    "Sorry, the local AI model is currently unavailable."
                )

                activity.append(
                    f"Local SLM failed → {str(error)}"
                )

            save_interaction(
                message,
                response
            )

            activity.append(
                "Interaction saved to local memory"
            )

            return {
                "message": response,
                "intent": intent,
                "permission_required": False,
                "activity": activity
            }

        # ===================================
        # FALLBACK
        # ===================================

        response = (
            "I can help with healthcare status, document status, "
            "payment status, and personal preferences."
        )

        save_interaction(
            message,
            response
        )

        activity.append(
            "Interaction saved to local memory"
        )

        return {
            "message": response,
            "intent": intent,
            "permission_required": False,
            "activity": activity
        }

    # ===================================
    # PERMISSION HANDLER
    # ===================================

    def handle_permission(
        self,
        permission_id,
        allowed
    ):

        if allowed:

            self.permission_manager.grant(
                permission_id
            )

            return "Permission granted."

        self.permission_manager.deny(
            permission_id
        )

        return "Permission denied."

    # ===================================
    # CONTINUE PENDING REQUEST
    # ===================================

    def continue_request(
        self,
        user_id
    ):

        request = self.pending_requests.get(
            user_id
        )

        if not request:

            return {
                "message": "No pending request found.",
                "activity": []
            }

        # Remove pending request
        del self.pending_requests[user_id]

        # Execute original request again
        return self.process(
            request["message"],
            user_id
        )