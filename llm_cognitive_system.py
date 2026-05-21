import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# DETECTOR AGENT (unchanged)
# -----------------------------
class DetectorAgent:
    def process(self, signal):
        return {"signal": signal}


# -----------------------------
# LLM RISK AGENT (NEW)
# -----------------------------
class RiskAgent:

    def evaluate(self, context):

        prompt = f"""
You are an enterprise risk analysis engine.

Analyze the following operational signal and classify risk as:
LOW, MEDIUM, or HIGH.

Signal:
{context['signal']}

Return ONLY one word.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        risk = response.choices[0].message.content.strip().upper()

        context["risk"] = risk
        return context


# -----------------------------
# GOVERNANCE AGENT (rule-based for now)
# -----------------------------
class GovernanceAgent:

    def apply(self, context):

        risk = context["risk"]

        if risk == "HIGH":
            context["governance"] = "ESCALATE_TO_HUMAN"
        elif risk == "MEDIUM":
            context["governance"] = "REQUEST_APPROVAL"
        else:
            context["governance"] = "AUTO_EXECUTE"

        return context


# -----------------------------
# DECISION AGENT
# -----------------------------
class DecisionAgent:

    def decide(self, context):

        gov = context["governance"]

        mapping = {
            "ESCALATE_TO_HUMAN": "ESCALATED",
            "REQUEST_APPROVAL": "WAITING_APPROVAL",
            "AUTO_EXECUTE": "EXECUTED_AUTONOMOUSLY"
        }

        context["decision"] = mapping.get(gov, "BLOCKED")

        return context


# -----------------------------
# AUDIT AGENT
# -----------------------------
class AuditAgent:

    def __init__(self):
        self.logs = []

    def record(self, context):
        self.logs.append(context)

    def replay(self):
        print("\n===== AUDIT LOG =====")
        for log in self.logs:
            print(log)


# -----------------------------
# COGNITIVE ORCHESTRATOR
# -----------------------------
class CognitiveSystem:

    def __init__(self):
        self.detector = DetectorAgent()
        self.risk = RiskAgent()
        self.gov = GovernanceAgent()
        self.decision = DecisionAgent()
        self.audit = AuditAgent()

    def run(self, signal):

        context = self.detector.process(signal)
        context = self.risk.evaluate(context)
        context = self.gov.apply(context)
        context = self.decision.decide(context)

        self.audit.record(context)

        return context


# -----------------------------
# SIMULATION
# -----------------------------
if __name__ == "__main__":

    system = CognitiveSystem()

    signals = [
        "Critical failure in Snowflake ingestion pipeline affecting billing",
        "Minor delay in dashboard refresh",
        "System operating normally"
    ]

    for s in signals:
        print("\n====================")
        result = system.run(s)
        print(result)

    system.audit.replay()
