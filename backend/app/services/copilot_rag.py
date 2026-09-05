"""RAG Copilot & XAI Explanation Engine."""

import json
import os
from typing import Dict, Any, Optional, List
import httpx


class CopilotRAG:
    """RAG Copilot generating grounded financial advice from pre-calculated evidence packs."""

    @classmethod
    async def generate_explanation(
        cls,
        user_query: str,
        evidence_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consumes evidence JSON and produces grounded, non-hallucinated natural language explanations."""

        openai_key = os.getenv("OPENAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        prompt_system = (
            "You are an expert AI Finance Controller assistant.\n"
            "STRICT CONSTRAINT: Do NOT compute or recalculate any numbers yourself.\n"
            "Rely strictly on the provided JSON evidence payload to explain financial decisions, anomaly alerts, policy breaches, and goal impacts to the user.\n"
            "Keep explanations clear, actionable, grounded, and concise."
        )

        user_content = (
            f"User Query: {user_query}\n\n"
            f"Pre-Calculated Evidence JSON:\n{json.dumps(evidence_context, indent=2)}\n\n"
            "Provide a grounded explanation based ONLY on the evidence JSON above."
        )

        if openai_key:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {openai_key}"},
                        json={
                            "model": "gpt-4o-mini",
                            "messages": [
                                {"role": "system", "content": prompt_system},
                                {"role": "user", "content": user_content}
                            ],
                            "temperature": 0.2
                        }
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        answer = data["choices"][0]["message"]["content"]
                        return {
                            "answer": answer,
                            "evidence_citation": evidence_context
                        }
            except Exception:
                pass  # Fallback to local grounded synthesizer

        # Local Grounded Rule-based Synthesizer
        answer = cls._synthesize_local_response(user_query, evidence_context)
        return {
            "answer": answer,
            "evidence_citation": evidence_context
        }

    @classmethod
    def _synthesize_local_response(cls, query: str, context: Dict[str, Any]) -> str:
        q_lower = query.lower()

        if "flag" in q_lower or "anomaly" in q_lower:
            amount = context.get("amount", "N/A")
            mean = context.get("historical_mean", "N/A")
            z = context.get("z_score", "N/A")
            score = context.get("anomaly_score", "N/A")
            return (
                f"Your transaction of ₹{amount} was flagged because it significantly exceeds your category's historical average spend of ₹{mean}. "
                f"Statistical Z-score calculation returned Z={z} (Threshold > 3.0), resulting in an anomaly risk score of {score}. "
                f"This transaction has been recorded in the system audit registry for compliance review."
            )
        elif "simulate" in q_lower or "buy" in q_lower or "purchase" in q_lower:
            feasible = context.get("feasible", False)
            projected = context.get("projected_end_of_month_balance", "N/A")
            policy_breach = context.get("policy_breach", False)
            reserve_breach = context.get("reserve_breach", False)

            if feasible:
                return (
                    f"The purchase simulation is FEASIBLE. After this expense, your projected end-of-month balance will be ₹{projected:,.2f}, "
                    f"which safely maintains your minimum reserve threshold."
                )
            else:
                reasons = []
                if policy_breach:
                    reasons.append("it breaches your monthly budget category limit")
                if reserve_breach:
                    reasons.append("it drops your projected end-of-month balance below your safety reserve threshold")
                return (
                    f"The purchase simulation is NOT RECOMMENDED. Reasons: {', '.join(reasons)}. "
                    f"Your projected month-end balance would drop to ₹{projected:,.2f}."
                )
        else:
            return (
                f"Based on your profile evidence: Current reserve balance is ₹{context.get('current_balance', 45000):,.2f}. "
                f"All monthly policies and financial goal trajectories are being actively monitored by the controller pipeline."
            )
