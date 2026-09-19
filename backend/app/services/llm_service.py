from typing import List, Dict, Any, Generator, Optional
from openai import OpenAI
from backend.app.config import settings

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.NVIDIA_BASE_URL,
            api_key=settings.NVIDIA_API_KEY
        )
        self.model = settings.LLM_MODEL

    def build_system_prompt(
        self,
        user_profile: Optional[Dict[str, Any]] = None,
        rag_contexts: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Construct a comprehensive system prompt combining coach persona,
        user health metrics, and ChromaDB retrieved knowledge.
        """
        prompt_parts = [
            "You are 'Fitness AI-Chatbot', a premier, science-backed fitness and nutrition AI coach, styled like ChatGPT.",
            "CRITICAL INSTRUCTION: For EVERY query, you MUST give a SHORT, ACCURATE, and DIRECT response.",
            "- Get straight to the answer immediately. Do NOT use conversational filler, pleasantries, or preamble.",
            "- Be concise: Use concise bullet points, direct facts, and clean structured markdown tables where appropriate.",
            "- Focus strictly on what was asked without unnecessary fluff or sales pitches.",
            "- Prioritize accurate science, proper biomechanics, and clear actionable takeaways."
        ]

        # 1. User Profile Context
        if user_profile:
            prompt_parts.append("\n### USER HEALTH & BIOMETRIC PROFILE:")
            if user_profile.get("age"):
                prompt_parts.append(f"- Age: {user_profile['age']} years")
            if user_profile.get("gender"):
                prompt_parts.append(f"- Gender: {user_profile['gender'].capitalize()}")
            if user_profile.get("height_cm") and user_profile.get("weight_kg"):
                prompt_parts.append(f"- Height: {user_profile['height_cm']} cm | Weight: {user_profile['weight_kg']} kg")
            if user_profile.get("fitness_goal"):
                prompt_parts.append(f"- Primary Goal: {user_profile['fitness_goal'].replace('_', ' ').title()}")
            if user_profile.get("activity_level"):
                prompt_parts.append(f"- Activity Level: {user_profile['activity_level'].replace('_', ' ').title()}")
            if user_profile.get("dietary_preference"):
                prompt_parts.append(f"- Dietary Preference: {user_profile['dietary_preference'].capitalize()}")
            if user_profile.get("injuries_limitations"):
                prompt_parts.append(f"- Known Injuries/Limitations: {user_profile['injuries_limitations']}")

        # 2. RAG Context from ChromaDB
        if rag_contexts and len(rag_contexts) > 0:
            prompt_parts.append("\n### RETRIEVED SCIENTIFIC & COACHING KNOWLEDGE (ChromaDB RAG):")
            for idx, item in enumerate(rag_contexts, 1):
                prompt_parts.append(f"--- Document [{idx}]: {item.get('title', 'Guide')} ({item.get('category', 'Fitness')}) ---")
                prompt_parts.append(item.get("snippet", "").strip())
            prompt_parts.append("Integrate this scientific knowledge seamlessly into your advice.")

        return "\n".join(prompt_parts)


    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.5,
        max_tokens: int = 1500
    ) -> Dict[str, str]:
        """Synchronous completion returning content and reasoning_content"""
        formatted_messages = [{"role": "system", "content": system_prompt}] + messages
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                top_p=0.95,
                max_tokens=max_tokens,
                extra_body={"chat_template_kwargs": {"enable_thinking": True}},
                stream=False
            )
            choice = completion.choices[0]
            content = choice.message.content or ""
            reasoning = getattr(choice.message, "reasoning_content", "") or ""
            return {"content": content, "reasoning_content": reasoning}
        except Exception as e:
            print(f"[LLMService] Error during completion: {e}")
            return {
                "content": f"I apologize, but I encountered an error communicating with the AI model: {str(e)}",
                "reasoning_content": "Error during LLM API call."
            }

    def stream_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.5,
        max_tokens: int = 2048
    ) -> Generator[Dict[str, str], None, None]:

        """
        Streaming generator yielding dicts:
        {'type': 'thinking' | 'content', 'text': str}
        """
        formatted_messages = [{"role": "system", "content": system_prompt}] + messages
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                top_p=0.95,
                max_tokens=max_tokens,
                extra_body={"chat_template_kwargs": {"enable_thinking": True}},
                stream=True
            )
            for chunk in completion:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                
                # Check reasoning/thinking tokens
                reasoning = getattr(delta, "reasoning_content", None)
                if reasoning:
                    yield {"type": "thinking", "text": reasoning}

                # Check answer content
                if delta.content is not None and len(delta.content) > 0:
                    yield {"type": "content", "text": delta.content}
        except Exception as e:
            print(f"[LLMService] Error during streaming: {e}")
            yield {"type": "content", "text": f"\n\n[Error generating response: {str(e)}]"}

llm_service = LLMService()
