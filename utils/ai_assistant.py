"""
AI Assistant module for Ministry of Labour Dashboard.
Handles chat, insights generation, reports, and scenario building using OpenAI and Anthropic.
"""
import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import tiktoken
import streamlit as st

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    OpenAI = None
    Anthropic = None

from .ai_prompts import (
    SYSTEM_PROMPTS,
    CONTEXT_TEMPLATES,
    INSIGHT_PROMPTS,
    REPORT_PROMPTS,
    SCENARIO_BUILDING_PROMPTS
)


class AIAssistant:
    """
    AI Assistant for the Ministry of Labour dashboard.
    Supports OpenAI GPT-4 and Anthropic Claude for various tasks.
    """
    
    def __init__(self, openai_api_key: str = None, anthropic_api_key: str = None):
        """
        Initialize AI Assistant with API keys.
        
        Args:
            openai_api_key: OpenAI API key
            anthropic_api_key: Anthropic API key
        """
        self.openai_client = None
        self.anthropic_client = None
        self.encoding = None
        
        # Initialize OpenAI
        if openai_api_key and OpenAI:
            try:
                self.openai_client = OpenAI(api_key=openai_api_key)
                self.encoding = tiktoken.encoding_for_model("gpt-4")
            except Exception as e:
                print(f"OpenAI initialization error: {e}")
        
        # Initialize Anthropic
        if anthropic_api_key and Anthropic:
            try:
                self.anthropic_client = Anthropic(api_key=anthropic_api_key)
            except Exception as e:
                print(f"Anthropic initialization error: {e}")
        
        # Initialize cache
        if 'ai_cache' not in st.session_state:
            st.session_state.ai_cache = {}
        
        # Initialize cost tracking
        if 'ai_costs' not in st.session_state:
            st.session_state.ai_costs = {
                'total_tokens': 0,
                'estimated_cost': 0.0,
                'requests': 0
            }
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        return len(text.split()) * 1.3  # Rough estimate
    
    def _get_cache_key(self, prompt: str, context: str = "") -> str:
        """Generate cache key for a prompt."""
        import hashlib
        combined = f"{prompt}:{context}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[str]:
        """Check if response is cached."""
        if cache_key in st.session_state.ai_cache:
            cached = st.session_state.ai_cache[cache_key]
            # Cache valid for 1 hour
            if time.time() - cached['timestamp'] < 3600:
                return cached['response']
        return None
    
    def _save_to_cache(self, cache_key: str, response: str):
        """Save response to cache."""
        st.session_state.ai_cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
    
    def _update_costs(self, tokens: int, model: str = "gpt-4"):
        """Update cost tracking."""
        # Rough cost estimates
        cost_per_1k = {
            'gpt-4': 0.03,
            'gpt-4-turbo': 0.01,
            'claude-opus': 0.015,
            'claude-sonnet': 0.003
        }
        
        rate = cost_per_1k.get(model, 0.01)
        cost = (tokens / 1000) * rate
        
        st.session_state.ai_costs['total_tokens'] += tokens
        st.session_state.ai_costs['estimated_cost'] += cost
        st.session_state.ai_costs['requests'] += 1
    
    def chat(
        self, 
        message: str, 
        context: Dict[str, Any] = None,
        language: str = "en",
        chat_history: List[Dict] = None
    ) -> str:
        """
        Chat with AI assistant using GPT-4.
        
        Args:
            message: User message
            context: Dashboard context (current page, data, etc.)
            language: Language preference ("en" or "ar")
            chat_history: Previous chat messages
            
        Returns:
            AI response
        """
        if not self.openai_client:
            return "AI chat is not available. Please configure OpenAI API key."
        
        try:
            # Build system prompt
            system_prompt = SYSTEM_PROMPTS[language]["chat"]
            
            # Add context if provided
            if context:
                context_text = self._format_context(context)
                system_prompt += f"\n\nCurrent Context:\n{context_text}"
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history
            if chat_history:
                messages.extend(chat_history[-10:])  # Last 10 messages
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Check cache
            cache_key = self._get_cache_key(message, str(context))
            cached_response = self._check_cache(cache_key)
            if cached_response:
                return cached_response
            
            # Call OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Update costs
            total_tokens = response.usage.total_tokens
            self._update_costs(total_tokens, "gpt-4-turbo")
            
            # Cache response
            self._save_to_cache(cache_key, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_insights(
        self,
        data_summary: Dict[str, Any],
        insight_type: str = "executive_summary",
        language: str = "en"
    ) -> str:
        """
        Generate AI insights using Claude for analysis.
        
        Args:
            data_summary: Dictionary with data to analyze
            insight_type: Type of insights to generate
            language: Language preference
            
        Returns:
            Generated insights
        """
        if not self.anthropic_client:
            # Fallback to OpenAI if Claude not available
            return self._generate_insights_openai(data_summary, insight_type, language)
        
        try:
            # Get prompt template
            prompt_template = INSIGHT_PROMPTS.get(insight_type, INSIGHT_PROMPTS["executive_summary"])
            
            # Format prompt with data
            prompt = prompt_template.format(**data_summary)
            
            # Check cache
            cache_key = self._get_cache_key(prompt, insight_type)
            cached_response = self._check_cache(cache_key)
            if cached_response:
                return cached_response
            
            # Call Claude - using Sonnet 4 (Latest)
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                system=SYSTEM_PROMPTS[language]["insights"],
                messages=[{"role": "user", "content": prompt}]
            )
            
            insights = message.content[0].text
            
            # Update costs (approximate)
            tokens = self.count_tokens(prompt + insights)
            self._update_costs(tokens, "claude-sonnet")
            
            # Cache response
            self._save_to_cache(cache_key, insights)
            
            return insights
            
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _generate_insights_openai(
        self,
        data_summary: Dict[str, Any],
        insight_type: str,
        language: str
    ) -> str:
        """Fallback to OpenAI for insights if Claude unavailable."""
        if not self.openai_client:
            return "AI insights unavailable. Please configure API keys."
        
        try:
            prompt_template = INSIGHT_PROMPTS.get(insight_type)
            prompt = prompt_template.format(**data_summary)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[language]["insights"]},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_report(
        self,
        data_summary: Dict[str, Any],
        scenario_info: Dict[str, Any] = None,
        language: str = "en"
    ) -> str:
        """
        Generate comprehensive executive report using Claude.
        
        Args:
            data_summary: Summary of dashboard data
            scenario_info: Information about active scenario
            language: Language preference
            
        Returns:
            Formatted report
        """
        if not self.anthropic_client:
            return self._generate_report_openai(data_summary, scenario_info, language)
        
        try:
            # Format data
            data_str = json.dumps(data_summary, indent=2)
            scenario_str = json.dumps(scenario_info, indent=2) if scenario_info else "No active scenario"
            
            # Build prompt
            prompt = REPORT_PROMPTS["executive_report"].format(
                data_summary=data_str,
                scenario_info=scenario_str
            )
            
            # Check cache
            cache_key = self._get_cache_key(prompt, "report")
            cached_response = self._check_cache(cache_key)
            if cached_response:
                return cached_response
            
            # Call Claude with longer context - using Opus 4 for best quality reports
            message = self.anthropic_client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=4000,
                system=SYSTEM_PROMPTS[language]["report"],
                messages=[{"role": "user", "content": prompt}]
            )
            
            report = message.content[0].text
            
            # Update costs
            tokens = self.count_tokens(prompt + report)
            self._update_costs(tokens, "claude-sonnet")
            
            # Cache
            self._save_to_cache(cache_key, report)
            
            return report
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _generate_report_openai(
        self,
        data_summary: Dict[str, Any],
        scenario_info: Dict[str, Any],
        language: str
    ) -> str:
        """Fallback to OpenAI for report generation."""
        if not self.openai_client:
            return "Report generation unavailable. Please configure API keys."
        
        try:
            data_str = json.dumps(data_summary, indent=2)
            scenario_str = json.dumps(scenario_info, indent=2) if scenario_info else "No active scenario"
            
            prompt = REPORT_PROMPTS["executive_report"].format(
                data_summary=data_str,
                scenario_info=scenario_str
            )
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[language]["report"]},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def parse_scenario_intent(
        self,
        user_input: str,
        service_list: List[str],
        category_list: List[str],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Parse natural language scenario request.
        
        Args:
            user_input: User's scenario description
            service_list: Available services
            category_list: Available categories
            language: Language preference
            
        Returns:
            Structured scenario intent
        """
        if not self.openai_client:
            return {"error": "AI unavailable"}
        
        try:
            # Build prompt
            prompt = SCENARIO_BUILDING_PROMPTS["intent_parsing"].format(
                user_input=user_input,
                service_list=", ".join(service_list[:20]),  # First 20 services
                category_list=", ".join(category_list)
            )
            
            # Call OpenAI with JSON mode
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a JSON parser. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.3
            )
            
            intent = json.loads(response.choices[0].message.content)
            return intent
            
        except Exception as e:
            return {"error": str(e)}
    
    def explain_chart(
        self,
        chart_type: str,
        data: Dict[str, Any],
        language: str = "en"
    ) -> str:
        """
        Explain a chart in plain language.
        
        Args:
            chart_type: Type of chart (pareto, quadrant, trend, etc.)
            data: Chart data
            language: Language preference
            
        Returns:
            Plain language explanation
        """
        explanations = {
            "pareto": "The Pareto chart shows that a small number of services handle most requests. Services on the left are your highest priority.",
            "quadrant": "The quadrant chart categorizes services by volume and revenue. Focus on high-volume, low-revenue services for quick wins.",
            "trend": "The trend chart shows how requests have changed over time. Use this to identify growth patterns.",
            "forecast": "The forecast predicts future demand based on historical patterns. Use this for capacity planning."
        }
        
        return explanations.get(chart_type, "This chart visualizes service data to help identify patterns and opportunities.")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into readable text."""
        lines = []
        for key, value in context.items():
            if isinstance(value, (int, float)):
                if value > 1000:
                    lines.append(f"{key}: {value:,.0f}")
                else:
                    lines.append(f"{key}: {value}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get current session cost summary."""
        return st.session_state.ai_costs.copy()
    
    def reset_costs(self):
        """Reset cost tracking."""
        st.session_state.ai_costs = {
            'total_tokens': 0,
            'estimated_cost': 0.0,
            'requests': 0
        }
    
    def is_available(self) -> bool:
        """Check if AI assistant is available."""
        return self.openai_client is not None or self.anthropic_client is not None


def load_ai_assistant() -> Optional[AIAssistant]:
    """
    Load AI assistant with API keys from environment.
    
    Returns:
        AIAssistant instance or None if keys not available
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not openai_key and not anthropic_key:
            return None
        
        return AIAssistant(openai_key, anthropic_key)
    except Exception as e:
        print(f"Error loading AI assistant: {e}")
        return None

