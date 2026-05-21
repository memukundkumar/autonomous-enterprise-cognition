import json
from datetime import datetime

class DARELoopWithAudit:

    def __init__(self):
        self.memory = []
        self.audit_log = []

        self.policies = {
            "AUTO_EXECUTE_ALLOWED": ["low"],
            "NEED_APPROVAL": ["medium"],
            "FORCE_ESCALATION": ["high"]
        }

    def detect(self, signal):
        print(f"[DETECT] {signal}")
        return {"signal": signal}

    def assess(self, context):
        risk = "low"

        if "failure" in context["signal"].lower():
            risk = "high"
        elif "delay" in context["signal"].lower():
            risk = "medium"

        context["risk"] = risk
        return context

    def govern(self, context):
        risk = context["risk"]

        if risk in self.policies["FORCE_ESCALATION"]:
            context["governance"] = "ESCALATE_TO_HUMAN"
        elif risk in self.policies["NEED_APPROVAL"]:
            context["governance"] = "REQUEST_APPROVAL"
        else:
            context["governance"] = "AUTO_EXECUTE"

        return context

    def resolve(self, context):
        action = context["governance"]

        if action == "ESCALATE_TO_HUMAN":
            decision = "ESCALATED"
        elif action == "REQUEST_APPROVAL":
            decision = "WAITING_APPROVAL"
        else:
            decision = "EXECUTED_AUTONOMOUSLY"

        context["decision"] = decision
        return context

    def explain(self, context):
        explanation = {
            "signal": context["signal"],
            "risk": context["risk"],
            "governance": context["governance"],
            "decision": context["decision"],
            "reason": "Policy + risk evaluation + system rules"
        }

        return explanation

    # -------------------------
    # 🧾 AUDIT SYSTEM
    # -------------------------
    def audit(self, context, explanation):

        record = {
            "timestamp": str(datetime.now()),
            "context": context,
            "explanation": explanation
        }

        self.audit_log.append(record)

    # -------------------------
    # 🔁 REPLAY SYSTEM
    # -------------------------
    def replay(self, index):
        print("\n[REPLAY MODE]")

        record = self.audit_log[index]

        print(json.dumps(record, indent=2))

    # -------------------------
    # RUN ENGINE
    # -------------------------
    def run(self, signal):

        context = self.detect(signal)
        context = self.assess(context)
        context = self.govern(context)
        context = self.resolve(context)

        explanation = self.explain(context)

        self.audit(context, explanation)

        return explanation


# -------------------------
# SIMULATION
# -------------------------
if __name__ == "__main__":

    engine = DARELoopWithAudit()

    signals = [
        "Data pipeline failure in Snowflake ingestion layer",
        "Minor delay in reporting dashboard",
        "System running normally"
    ]

    for s in signals:
        print("\n====================")
        result = engine.run(s)
        print(result)

    # Replay first decision
    engine.replay(0)
