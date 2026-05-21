class DARELoop:

    def detect(self, signal):
        print(f"[DETECT] Signal received: {signal}")
        return {"signal": signal, "risk": "medium"}

    def assess(self, context):
        print("[ASSESS] Evaluating impact...")
        if "failure" in context["signal"].lower():
            context["risk"] = "high"
        elif "delay" in context["signal"].lower():
            context["risk"] = "medium"
        else:
            context["risk"] = "low"
        return context

    def resolve(self, context):
        print("[RESOLVE] Deciding action...")

        if context["risk"] == "high":
            action = "ESCALATE_TO_HUMAN"
        elif context["risk"] == "medium":
            action = "AUTOMATED_RETRY"
        else:
            action = "NO_ACTION_REQUIRED"

        context["action"] = action
        return context

    def explain(self, context):
        print("[EXPLAIN] Generating reasoning trace...")
        explanation = f"""
Signal: {context['signal']}
Risk Level: {context['risk']}
Action Taken: {context['action']}

Reason:
- Based on enterprise signal interpretation
- Risk evaluated using heuristic rules
- Governance constraints applied
"""
        context["explanation"] = explanation
        return context


# ---- Simulation ----
if __name__ == "__main__":
    engine = DARELoop()

    signal = "Data pipeline failure in Snowflake ingestion layer"

    context = engine.detect(signal)
    context = engine.assess(context)
    context = engine.resolve(context)
    context = engine.explain(context)

    print("\n===== FINAL OUTPUT =====")
    print(context["explanation"])
