# src/utils/voice_expense_ai.py
"""
Voice-to-Expense AI Module
Records audio, transcribes speech, and uses Ollama (llama3.2) to
parse natural language into structured expense data.
Supports multi-turn conversation for clarification.
"""

import json
import io
import wave
import tempfile
import os

# ── Optional dependencies (graceful degradation) ──
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import sounddevice as sd
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# ── Ollama System Prompt ──
SYSTEM_PROMPT = """You are a smart expense tracking assistant inside a mobile app.
Your ONLY job is to extract expense details from what the user says and return valid JSON.

RULES:
1. Extract: amount, currency, category, and description from the user's speech.
2. If you understand everything clearly, set "understood" to true.
3. If something is missing or unclear, set "understood" to false and ask ONE short follow-up question.
4. Be conversational, friendly, and concise.
5. ALWAYS respond with ONLY valid JSON — no markdown, no extra text, no code fences.

CATEGORIES (pick the best match):
Food & Dining, Transport, Shopping, Entertainment, Bills & Utilities, Health, Education, Electronics, Groceries, Rent, Travel, Subscription, Other

CURRENCY CODES: PHP (default), USD, EUR, JPY, GBP, KRW, SGD, AUD, CAD, INR

JSON FORMAT:
{"understood": true, "amount": 500.0, "currency": "PHP", "category": "Food & Dining", "description": "Starbucks coffee", "message": "Got it! 500 pesos for Starbucks coffee.", "follow_up": null}

EXAMPLE - user says "I spent 500 pesos on Starbucks":
{"understood": true, "amount": 500.0, "currency": "PHP", "category": "Food & Dining", "description": "Starbucks coffee", "message": "Got it! ₱500 for Starbucks coffee under Food & Dining.", "follow_up": null}

EXAMPLE - user says "I bought something at the mall":
{"understood": false, "amount": null, "currency": "PHP", "category": "Shopping", "description": "mall purchase", "message": "Sounds like a shopping trip! How much did you spend?", "follow_up": "How much did you spend?"}

EXAMPLE - user says "200 for grab":
{"understood": true, "amount": 200.0, "currency": "PHP", "category": "Transport", "description": "Grab ride", "message": "Got it! ₱200 for a Grab ride under Transport.", "follow_up": null}

IMPORTANT: Return ONLY the JSON object. No other text."""


class VoiceExpenseAI:
    """Handles speech recording, transcription, and AI expense parsing."""

    def __init__(self, model="llama3.2"):
        self.model = model
        self.conversation = []
        self.extracted = {
            "amount": None,
            "currency": "PHP",
            "category": "Other",
            "description": "",
        }
        self.is_recording = False
        self.is_processing = False

    # ── Dependency Checks ──
    @staticmethod
    def check_dependencies():
        """Return list of missing dependency messages. Empty = all good."""
        issues = []
        if not SPEECH_AVAILABLE:
            issues.append("SpeechRecognition not installed (pip install SpeechRecognition)")
        if not AUDIO_AVAILABLE:
            issues.append("sounddevice not installed (pip install sounddevice numpy)")
        if not OLLAMA_AVAILABLE:
            issues.append("ollama not installed (pip install ollama)")

        if OLLAMA_AVAILABLE:
            try:
                ollama.list()
            except Exception:
                issues.append("Ollama is not running. Start it with: ollama serve")
        return issues

    # ── Audio Recording ──
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio using sounddevice and return WAV bytes."""
        if not AUDIO_AVAILABLE:
            return None, "Audio library not available"

        try:
            self.is_recording = True
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
            )
            sd.wait()  # Block until recording finishes
            self.is_recording = False

            # Convert numpy array to WAV bytes
            buf = io.BytesIO()
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            buf.seek(0)
            return buf.read(), None

        except Exception as e:
            self.is_recording = False
            return None, f"Recording error: {e}"

    # ── Transcription ──
    def transcribe(self, wav_bytes):
        """Transcribe WAV audio bytes using Google Speech Recognition."""
        if not SPEECH_AVAILABLE:
            return None, "SpeechRecognition not installed"

        recognizer = sr.Recognizer()
        try:
            audio_file = io.BytesIO(wav_bytes)
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)
            return text, None

        except sr.UnknownValueError:
            return None, "Couldn't understand the audio. Please speak clearly and try again."
        except sr.RequestError:
            return None, "Speech service unavailable. Check your internet connection."
        except Exception as e:
            return None, f"Transcription error: {e}"

    # ── Record + Transcribe (convenience) ──
    def record_and_transcribe(self, duration=5):
        """Record audio and transcribe it. Returns (text, error)."""
        wav_bytes, err = self.record_audio(duration=duration)
        if err:
            return None, err
        return self.transcribe(wav_bytes)

    # ── AI Parsing via Ollama ──
    def parse_expense(self, user_text):
        """Send text to Ollama, get structured expense data back."""
        if not OLLAMA_AVAILABLE:
            return {"error": "Ollama package not installed"}

        self.is_processing = True
        self.conversation.append({"role": "user", "content": user_text})

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + self.conversation

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={"temperature": 0.2},
            )

            ai_text = response["message"]["content"]
            self.conversation.append({"role": "assistant", "content": ai_text})
            self.is_processing = False

            # Parse JSON from response
            result = self._extract_json(ai_text)

            # Accumulate extracted fields
            if result.get("amount") is not None:
                self.extracted["amount"] = result["amount"]
            if result.get("currency"):
                self.extracted["currency"] = result["currency"]
            if result.get("category") and result["category"] != "Other":
                self.extracted["category"] = result["category"]
            if result.get("description"):
                self.extracted["description"] = result["description"]

            return result

        except Exception as e:
            self.is_processing = False
            err_msg = str(e)
            if "connect" in err_msg.lower():
                return {"error": "Cannot connect to Ollama. Run 'ollama serve' first."}
            return {"error": f"AI error: {err_msg}"}

    # ── JSON Extraction ──
    @staticmethod
    def _extract_json(text):
        """Extract JSON from AI response, handling markdown fences."""
        clean = text.strip()

        # Strip markdown code fences
        if clean.startswith("```"):
            lines = clean.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            clean = "\n".join(lines).strip()

        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            # Try to find JSON object in the text
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    return json.loads(clean[start:end])
                except json.JSONDecodeError:
                    pass

            # Fallback: treat as plain conversation
            return {
                "understood": False,
                "amount": None,
                "currency": "PHP",
                "category": "Other",
                "description": "",
                "message": text,
                "follow_up": "Could you tell me more about this expense?",
            }

    # ── State Management ──
    def reset(self):
        """Clear conversation history and extracted data."""
        self.conversation = []
        self.extracted = {
            "amount": None,
            "currency": "PHP",
            "category": "Other",
            "description": "",
        }
        self.is_recording = False
        self.is_processing = False

    def get_extracted(self):
        """Return a copy of the currently extracted expense data."""
        return self.extracted.copy()
