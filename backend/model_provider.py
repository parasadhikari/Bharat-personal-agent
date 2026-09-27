import time
import requests


class ModelProvider:

    def detect_intent(self, message):
        raise NotImplementedError

    def generate_response(self, context):
        raise NotImplementedError


class DemoModelProvider(ModelProvider):

    def detect_intent(self, message):

        text = message.lower()

        if any(word in text for word in [
            "health",
            "healthcare",
            "ayushman",
            "medical",
            "hospital"
        ]):
            return "healthcare_status"

        if any(word in text for word in [
            "document",
            "aadhaar",
            "aadhar",
            "verified",
            "verification"
        ]):
            return "document_status"

        if any(word in text for word in [
            "payment",
            "upi",
            "transaction",
            "paid"
        ]):
            return "payment_status"

        if any(word in text for word in [
            "remember",
            "preference",
            "prefer"
        ]):
            return "save_user_preference"

        return "general"

    def generate_response(self, context):
        return context


class LocalSLMProvider(ModelProvider):

    def __init__(self):

        self.model_name = "qwen2.5:0.5b"

        self.url = "http://localhost:11434/api/generate"

        self.keep_alive = "10m"

    def detect_intent(self, message):

        return DemoModelProvider().detect_intent(
            message
        )

    def generate_response(self, context):

        prompt = f"""
You are Bharat Personal Agent.

Answer the user's question briefly,
clearly and naturally.

Use maximum 2-3 sentences.

Do not mention internal tools,
permissions, system prompts,
or implementation details.

User question:
{context}
"""

        start_time = time.perf_counter()

        try:

            response = requests.post(
                self.url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 80,
                        "temperature": 0.3
                    },
                    "keep_alive": self.keep_alive
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            latency = time.perf_counter() - start_time

            print(
                f"Local SLM latency: {latency:.2f} seconds"
            )

            return {
                "text": data["response"].strip(),
                "latency": latency
            }

        except requests.exceptions.RequestException as error:

            latency = time.perf_counter() - start_time

            print(
                f"Local SLM request failed after "
                f"{latency:.2f} seconds: {error}"
            )

            raise RuntimeError(
                "Local SLM is currently unavailable."
            )


if __name__ == "__main__":

    provider = LocalSLMProvider()

    print("\nTesting Local SLM...\n")

    result = provider.generate_response(
        "What is an AI agent?"
    )

    print("Response:")
    print(result["text"])

    print(
        f"\nLatency: {result['latency']:.2f} seconds"
    )