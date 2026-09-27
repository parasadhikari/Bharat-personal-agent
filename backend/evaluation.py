from model_provider import DemoModelProvider


model = DemoModelProvider()


TEST_CASES = [

    # Healthcare
    {
        "message": "Check my healthcare status",
        "expected": "healthcare_status"
    },
    {
        "message": "Am I eligible for Ayushman Bharat?",
        "expected": "healthcare_status"
    },
    {
        "message": "Show my medical status",
        "expected": "healthcare_status"
    },

    # Document
    {
        "message": "Check my Aadhaar status",
        "expected": "document_status"
    },
    {
        "message": "Is my document verified?",
        "expected": "document_status"
    },
    {
        "message": "Check document verification",
        "expected": "document_status"
    },

    # Payment
    {
        "message": "Check my UPI payment",
        "expected": "payment_status"
    },
    {
        "message": "Is my transaction successful?",
        "expected": "payment_status"
    },
    {
        "message": "Show my payment status",
        "expected": "payment_status"
    },

    # Memory
    {
        "message": "Remember that I prefer short answers",
        "expected": "save_user_preference"
    },
    {
        "message": "Remember my preference",
        "expected": "save_user_preference"
    },

    # General
    {
        "message": "Hello",
        "expected": "general"
    },
    {
        "message": "Hi there",
        "expected": "general"
    },
    {
        "message": "What can you do?",
        "expected": "general"
    },
    {
        "message": "Tell me something",
        "expected": "general"
    }
]


def run_evaluation():

    total = len(TEST_CASES)
    correct = 0

    print("\n==============================")
    print(" Bharat Personal Agent")
    print(" Intent Evaluation")
    print("==============================\n")

    for index, test in enumerate(TEST_CASES, start=1):

        message = test["message"]
        expected = test["expected"]

        predicted = model.detect_intent(message)

        passed = predicted == expected

        if passed:
            correct += 1

        status = "PASS" if passed else "FAIL"

        print(
            f"{index}. {status} | "
            f"Input: {message}"
        )

        print(
            f"   Expected: {expected}"
        )

        print(
            f"   Predicted: {predicted}\n"
        )

    accuracy = (correct / total) * 100

    print("==============================")
    print(f"Total Tests : {total}")
    print(f"Correct     : {correct}")
    print(f"Accuracy    : {accuracy:.2f}%")
    print("==============================\n")


if __name__ == "__main__":
    run_evaluation()