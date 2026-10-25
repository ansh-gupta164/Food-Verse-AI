"""
Centralized AI service module for Food Verse AI using the official google-genai SDK.
Handles multimodal requests, API key detection, structured output parsing, and graceful fallbacks.
"""

import io
import os
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    types = None
    GENAI_AVAILABLE = False

from utils.constants import DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODEL
from utils.validators import extract_and_parse_json


class AIService:
    """
    Central service interface managing interactions with Google Gemini API.
    """

    def __init__(self, override_key: Optional[str] = None):
        self.api_key = self._resolve_api_key(override_key)
        self.model_name = DEFAULT_GEMINI_MODEL
        self.client = None
        if self.api_key and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def _resolve_api_key(self, override_key: Optional[str] = None) -> Optional[str]:
        """Resolves API key from override, streamlit secrets, or environment."""
        if override_key and override_key.strip():
            return override_key.strip()

        # Check Streamlit secrets if running inside streamlit
        try:
            import streamlit as st
            if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
        except Exception:
            pass

        # Environment variable fallback
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key and env_key.strip():
            return env_key.strip()

        return None

    def is_live(self) -> bool:
        """Returns True if a valid client is configured."""
        return self.client is not None

    def get_status_info(self) -> Dict[str, Any]:
        """Returns human-readable AI connection status."""
        if not GENAI_AVAILABLE:
            return {
                "is_live": False,
                "status_text": "Demo Mode (google-genai SDK not installed)",
                "color": "#ef4444",
                "badge": "Offline Demo"
            }
        if self.client is not None:
            # Mask key for privacy
            masked_key = self.api_key[:4] + "..." + self.api_key[-4:] if len(self.api_key) > 8 else "****"
            return {
                "is_live": True,
                "status_text": f"Live Gemini AI Active ({self.model_name}) [Key: {masked_key}]",
                "color": "#10b981",
                "badge": "Live AI Active"
            }
        return {
            "is_live": False,
            "status_text": "Demo Mode (No API Key configured - using curated intelligence)",
            "color": "#f59e0b",
            "badge": "Curated Demo Mode"
        }

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Executes a text generation request with error handling and JSON parsing.
        """
        if not self.is_live():
            return False, "Gemini API key is not configured. Falling back to Demo Mode.", None

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json"
        ) if types else None

        for model in [self.model_name, FALLBACK_GEMINI_MODEL]:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )
                raw_text = response.text or ""
                parsed_json = extract_and_parse_json(raw_text)
                return True, raw_text, parsed_json
            except Exception as e:
                err_msg = str(e)
                # If model is unavailable or rate limited, loop may try fallback
                if model == FALLBACK_GEMINI_MODEL or "API_KEY_INVALID" in err_msg:
                    return False, f"Gemini API Error: {err_msg}", None

        return False, "Failed to generate AI response across available models.", None

    def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Multimodal visual analysis of an image.
        """
        if not self.is_live():
            return False, "Gemini API key is not configured. Falling back to Demo Mode.", None

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json"
        ) if types else None

        contents = [
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt
        ]

        for model in [self.model_name, FALLBACK_GEMINI_MODEL]:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                raw_text = response.text or ""
                parsed_json = extract_and_parse_json(raw_text)
                return True, raw_text, parsed_json
            except Exception as e:
                err_msg = str(e)
                if model == FALLBACK_GEMINI_MODEL or "API_KEY_INVALID" in err_msg:
                    return False, f"Vision API Error: {err_msg}", None

        return False, "Failed to analyze image across available vision models.", None

    def analyze_frames(
        self,
        frames_bytes: List[Tuple[bytes, str]],
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Analyzes sampled video frames.
        """
        if not self.is_live():
            return False, "Gemini API key is not configured. Falling back to Demo Mode.", None

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json"
        ) if types else None

        contents = []
        for f_bytes, f_mime in frames_bytes:
            contents.append(types.Part.from_bytes(data=f_bytes, mime_type=f_mime))
        contents.append(prompt)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            raw_text = response.text or ""
            parsed_json = extract_and_parse_json(raw_text)
            return True, raw_text, parsed_json
        except Exception as e:
            return False, f"Video frame analysis error: {str(e)}", None
