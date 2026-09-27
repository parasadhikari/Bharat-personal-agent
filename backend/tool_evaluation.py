from model_provider import DemoModelProvider


model = DemoModelProvider()


TOOL_ROUTES = {
    "healthcare_status": "check_healthcare_status",
    "document_status": "get_document_status",
    "payment_status": "check_payment_status",
    "save_user_preference": "save_user_preference",
    "general": None
}


TEST_CASES = [
    {
        "message": "Check my healthcare status",
        "expected_tool": "check_healthcare_status"
    },
    {
        "message": "Am I eligible for Ayushman?",
        "expected_tool": "check_healthcare_status"
    },
    {
        "message": "Check my Aadhaar",
        "expected_tool": "get_document_status"
    },
    {
        "message": "Is my document verified?",
        "expected_tool": "get_document_status"
    },
    {
        "message": "Check my UPI payment",
        "expected_tool": "check_payment_status"
    },
    {
        "message": "Is my transaction successful?",
        "expected_tool": "check_payment_status"
    },
    {
        "message": "Remember I prefer short answers",
        "expected_tool": "save_user_preference"
    },
    {
        "message": "Hello",
        "expected_tool": None
    },
]


def run_evaluation():

    total = len(TEST_CASES)
    correct = 0

    print("\n==============================")
    print(" Bharat Personal Agent")
    print(" Tool Routing Evaluation")
    print("==============================\n")

    for index, test in enumerate(TEST_CASES, start=1):

        message = test["message"]
        expected_tool = test["expected_tool"]

        # Step 1: detect intent
        intent = model.detect_intent(message)

        # Step 2: route intent to tool
        predicted_tool = TOOL_ROUTES.get(intent)

        passed = predicted_tool == expected_tool

        if passed:
            correct += 1

        status = "PASS" if passed else "FAIL"

        print(
            f"{index}. {status} | Input: {message}"
        )

        print(
            f"   Intent: {intent}"
        )

        print(
            f"   Expected Tool: {expected_tool}"
        )

        print(
            f"   Predicted Tool: {predicted_tool}\n"
        )

    accuracy = (correct / total) * 100

    print("==============================")
    print(f"Total Tests : {total}")
    print(f"Correct     : {correct}")
    print(f"Accuracy    : {accuracy:.2f}%")
    print("==============================\n")


if __name__ == "__main__":
    run_evaluation()