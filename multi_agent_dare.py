from datetime import datetime

# -----------------------------
# 1. DETECTOR AGENT
# -----------------------------
class DetectorAgent:
    def process(self, signal):
        return {"signal": signal}


# -----------------------------
# 2. RISK AGENT
# -----------------------------
class RiskAgent:
    def evaluate(self, context):
        signal = context["signal"].lower()

        if "failure" in signal:
            context["risk"] = "high"
        elif "delay" in signal:
            context["risk"] = "medium"
        else:
            context["risk"] = "low"

        return context


# -----------------------------
# 3. GOVERNANCE AGENT
# -----------------------------
class GovernanceAgent:
    def __init__(self):
        self.policy = {
            "high": "ESCALATE_TO_HUMAN",
            "medium": "REQUEST_APPROVAL",
            "low": "AUTO_EXECUTE"
        }

    def apply(self, context):
        context["governance"] = self.policy.get(context["risk"], "BLOCK")
        return context


# -----------------------------
# 4. DECISION AGENT
# -----------------------------
class DecisionAgent:
    def decide(self, context):

        gov = context["governance"]

        if gov == "ESCALATE_TO_HUMAN":
            context["decision"] = "ESCALATED"
        elif gov == "REQUEST_APPROVAL":
            context["decision"] = "WAITING_APPROVAL"
        elif gov == "AUTO_EXECUTE":
            context["decision"] = "EXECUTED_AUTONOMOUSLY"
        else:
            context["decision"] = "BLOCKED"

        return context


# -----------------------------
# 5. AUDIT AGENT
# -----------------------------
class AuditAgent:
    def __init__(self):
        self.logs = []

    def record(self, context):
        entry = {
            "timestamp": str(datetime.now()),
            "context": context
        }
        self.logs.append(entry)

    def replay(self):
        print("\n===== AUDIT REPLAY =====")
        for log in self.logs:
            print(log)


# -----------------------------
# ORCHESTRATOR (COGNITIVE SYSTEM)
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
        "Data pipeline failure in Snowflake ingestion layer",
        "Minor delay in reporting dashboard",
        "System operating normally"
    ]

    for s in signals:
        print("\n===================")
        result = system.run(s)
        print(result)

    system.audit.replay()
