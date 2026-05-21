import os
import numpy as np 
from dotenv import load_dotenv  # <-- Add this
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()  # <-- Add this

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# EMBEDDING FUNCTION
# -----------------------------
def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)


# -----------------------------
# SEMANTIC MEMORY AGENT
# -----------------------------
class SemanticMemory:

    def __init__(self):
        self.store = []

    def add(self, signal, risk):
        vector = embed(signal)
        self.store.append({
            "signal": signal,
            "vector": vector,
            "risk": risk
        })

    def retrieve(self, signal, top_k=2):
        if not self.store:
            return []

        query_vec = embed(signal)

        scores = []
        for item in self.store:
            sim = np.dot(query_vec, item["vector"]) / (
                np.linalg.norm(query_vec) * np.linalg.norm(item["vector"])
            )
            scores.append((sim, item))

        scores.sort(reverse=True, key=lambda x: x[0])

        return [item for _, item in scores[:top_k]]


# -----------------------------
# RISK AGENT (LLM)
# -----------------------------
class RiskAgent:

    def evaluate(self, signal, memory_context):

        prompt = f"""
You are an enterprise risk engine.

Current signal:
{signal}

Similar past incidents:
{memory_context}

Classify risk as LOW, MEDIUM, or HIGH.
Return only one word.
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content.strip().upper()


# -----------------------------
# GOVERNANCE AGENT
# -----------------------------
class GovernanceAgent:

    def apply(self, risk):

        return {
            "HIGH": "ESCALATE",
            "MEDIUM": "APPROVAL",
            "LOW": "AUTO"
        }.get(risk, "BLOCK")


# -----------------------------
# DECISION AGENT
# -----------------------------
class DecisionAgent:

    def decide(self, gov):

        return {
            "ESCALATE": "ESCALATED",
            "APPROVAL": "WAITING_APPROVAL",
            "AUTO": "EXECUTED",
            "BLOCK": "BLOCKED"
        }.get(gov, "BLOCKED")


# -----------------------------
# COGNITIVE SYSTEM
# -----------------------------
class CognitiveSystem:

    def __init__(self):
        self.memory = SemanticMemory()
        self.risk = RiskAgent()
        self.gov = GovernanceAgent()
        self.decision = DecisionAgent()

    def run(self, signal):

        print("\n[INPUT]", signal)

        # 1. Retrieve semantic memory
        similar = self.memory.retrieve(signal)

        print("[MEMORY] Similar cases:")
        for s in similar:
            print(" -", s["signal"], "| risk:", s["risk"])

        # 2. Risk reasoning with context
        risk = self.risk.evaluate(signal, similar)

        # 3. Governance
        gov = self.gov.apply(risk)

        # 4. Decision
        decision = self.decision.decide(gov)

        # 5. Store memory
        self.memory.add(signal, risk)

        return {
            "signal": signal,
            "risk": risk,
            "governance": gov,
            "decision": decision
        }


# -----------------------------
# SIMULATION
# -----------------------------
if __name__ == "__main__":

    system = CognitiveSystem()

    signals = [
        "Snowflake ingestion pipeline failure impacting billing",
        "ETL pipeline failure in data warehouse",
        "Minor dashboard refresh delay",
        "System operating normally"
    ]

    for s in signals:
        result = system.run(s)
        print(result)
