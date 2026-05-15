# src/utils/orpheus_tts.py
"""
Orpheus TTS Module - Text-to-Speech using legraphista/Orpheus via Ollama
Generates natural-sounding speech from text using the SNAC audio codec.
"""

import os
import io
import json
import time
import wave
import tempfile
import threading
import requests
import numpy as np

# ── Optional heavy imports (graceful degradation) ──
try:
    import sounddevice as sd
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from snac import SNAC
    SNAC_AVAILABLE = True
except ImportError:
    SNAC_AVAILABLE = False

# ── Constants ──
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "legraphista/Orpheus:latest"
SAMPLE_RATE = 24000
MAX_TOKENS = 1200
TEMPERATURE = 0.6
TOP_P = 0.9
REPETITION_PENALTY = 1.1

VOICES = ["tara", "leah", "jess", "leo", "dan", "mia", "zac", "zoe"]
DEFAULT_VOICE = "tara"

SPECIAL_START = "<|audio|>"
SPECIAL_END = "<|eot_id|>"
CUSTOM_TOKEN_PREFIX = "<custom_token_"


class OrpheusTTS:
    """Text-to-Speech engine using Orpheus model via Ollama + SNAC decoder."""

    def __init__(self, voice: str = DEFAULT_VOICE):
        self.voice = voice if voice in VOICES else DEFAULT_VOICE
        self.session = requests.Session()
        self.snac_model = None
        self.snac_device = "cpu"
        self.is_speaking = False
        self._initialized = False
        self._init_error = None

    # ── Lazy initialization (don't block app startup) ──
    def _ensure_initialized(self):
        """Initialize SNAC model on first use."""
        if self._initialized:
            return self._init_error is None

        self._initialized = True

        if not TORCH_AVAILABLE:
            self._init_error = "PyTorch not installed (pip install torch)"
            return False

        if not SNAC_AVAILABLE:
            self._init_error = "SNAC not installed (pip install snac)"
            return False

        if not SD_AVAILABLE:
            self._init_error = "sounddevice not installed (pip install sounddevice)"
            return False

        try:
            print("[OrpheusTTS] Loading SNAC model...")
            self.snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()

            if torch.cuda.is_available():
                self.snac_device = "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.snac_device = "mps"
            else:
                self.snac_device = "cpu"

            self.snac_model = self.snac_model.to(self.snac_device)
            print(f"[OrpheusTTS] SNAC loaded on {self.snac_device}")
            return True

        except Exception as e:
            self._init_error = f"SNAC init error: {e}"
            print(f"[OrpheusTTS] {self._init_error}")
            return False

    # ── Check if TTS is available ──
    def check_available(self) -> tuple:
        """Check if TTS system is available. Returns (available: bool, error: str|None)."""
        if not TORCH_AVAILABLE:
            return False, "PyTorch not installed"
        if not SNAC_AVAILABLE:
            return False, "SNAC not installed (pip install snac)"
        if not SD_AVAILABLE:
            return False, "sounddevice not installed"

        # Check Ollama connectivity
        try:
            resp = self.session.get("http://localhost:11434/api/tags", timeout=3)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                # Check for any Orpheus model
                has_orpheus = any("orpheus" in n.lower() for n in model_names)
                if not has_orpheus:
                    return False, "Orpheus model not found in Ollama. Run: ollama pull legraphista/Orpheus"
                return True, None
            return False, "Ollama not responding"
        except Exception:
            return False, "Ollama not running. Start with: ollama serve"

    # ── Token to ID conversion ──
    @staticmethod
    def _turn_token_into_id(token_string, index):
        """Convert a token string like <custom_token_XXXX> to an audio code ID."""
        token_string = token_string.strip()
        last_token_start = token_string.rfind(CUSTOM_TOKEN_PREFIX)

        if last_token_start == -1:
            return None

        last_token = token_string[last_token_start:]

        if last_token.startswith(CUSTOM_TOKEN_PREFIX) and last_token.endswith(">"):
            try:
                number_str = last_token[14:-1]
                token_id = int(number_str) - 10 - ((index % 7) * 4096)
                return token_id
            except ValueError:
                return None
        return None

    # ── Convert tokens to audio via SNAC ──
    def _convert_to_audio(self, multiframe):
        """Decode audio tokens using SNAC codec."""
        if self.snac_model is None or len(multiframe) < 7:
            return None

        codes_0 = torch.tensor([], device=self.snac_device, dtype=torch.int32)
        codes_1 = torch.tensor([], device=self.snac_device, dtype=torch.int32)
        codes_2 = torch.tensor([], device=self.snac_device, dtype=torch.int32)

        num_frames = len(multiframe) // 7
        frame = multiframe[:num_frames * 7]

        for j in range(num_frames):
            i = 7 * j
            codes_0 = torch.cat([codes_0, torch.tensor([frame[i]], device=self.snac_device, dtype=torch.int32)])

            codes_1 = torch.cat([codes_1, torch.tensor([frame[i + 1]], device=self.snac_device, dtype=torch.int32)])
            codes_1 = torch.cat([codes_1, torch.tensor([frame[i + 4]], device=self.snac_device, dtype=torch.int32)])

            codes_2 = torch.cat([codes_2, torch.tensor([frame[i + 2]], device=self.snac_device, dtype=torch.int32)])
            codes_2 = torch.cat([codes_2, torch.tensor([frame[i + 3]], device=self.snac_device, dtype=torch.int32)])
            codes_2 = torch.cat([codes_2, torch.tensor([frame[i + 5]], device=self.snac_device, dtype=torch.int32)])
            codes_2 = torch.cat([codes_2, torch.tensor([frame[i + 6]], device=self.snac_device, dtype=torch.int32)])

        codes = [codes_0.unsqueeze(0), codes_1.unsqueeze(0), codes_2.unsqueeze(0)]

        # Validate code ranges
        for c in codes:
            if torch.any(c < 0) or torch.any(c > 4096):
                return None

        with torch.inference_mode():
            audio_hat = self.snac_model.decode(codes)

        audio_slice = audio_hat[:, :, 2048:4096]
        detached_audio = audio_slice.detach().cpu()
        audio_np = detached_audio.numpy()
        audio_int16 = (audio_np * 32767).astype(np.int16)
        return audio_int16.tobytes()

    # ── Format the prompt ──
    def _format_prompt(self, text: str) -> str:
        """Format text with voice and special tokens for Orpheus."""
        return f"{SPECIAL_START}{self.voice}: {text}{SPECIAL_END}"

    # ── Generate speech from text ──
    def generate_speech(self, text: str, play: bool = True) -> bytes:
        """
        Generate speech audio from text using Orpheus model.
        
        Args:
            text: The text to speak
            play: If True, play audio through speakers immediately
            
        Returns:
            Raw audio bytes (PCM int16, 24kHz mono)
        """
        if not self._ensure_initialized():
            print(f"[OrpheusTTS] Cannot generate: {self._init_error}")
            return b""

        self.is_speaking = True
        formatted_prompt = self._format_prompt(text)
        print(f"[OrpheusTTS] Generating speech: \"{text[:60]}...\"")

        start_time = time.time()
        collected_tokens = []

        try:
            # Call Ollama API with streaming
            payload = {
                "model": MODEL_NAME,
                "prompt": formatted_prompt,
                "options": {
                    "num_predict": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "repeat_penalty": REPETITION_PENALTY,
                },
                "stream": True,
            }

            response = self.session.post(
                OLLAMA_API_URL,
                headers={"Content-Type": "application/json"},
                json=payload,
                stream=True,
                timeout=60,
            )

            if response.status_code != 200:
                print(f"[OrpheusTTS] API error: {response.status_code}")
                self.is_speaking = False
                return b""

            # Collect tokens from streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "response" in data:
                            token_text = data["response"]
                            if token_text:
                                collected_tokens.append(token_text)
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

            token_time = time.time()
            print(f"[OrpheusTTS] Token generation: {token_time - start_time:.2f}s ({len(collected_tokens)} tokens)")

            # Convert tokens to audio
            audio_segments = []
            buffer = []
            count = 0

            for token_text in collected_tokens:
                token = self._turn_token_into_id(token_text, count)
                if token is not None and token > 0:
                    buffer.append(token)
                    count += 1

                    if count % 7 == 0 and count > 27:
                        buffer_to_proc = buffer[-28:]
                        audio_samples = self._convert_to_audio(buffer_to_proc)
                        if audio_samples is not None:
                            audio_segments.append(audio_samples)

            audio_time = time.time()
            print(f"[OrpheusTTS] Audio conversion: {audio_time - token_time:.2f}s ({len(audio_segments)} segments)")

            audio_buffer = b"".join(audio_segments) if audio_segments else b""

            # Play audio
            if play and audio_buffer and SD_AVAILABLE:
                try:
                    audio_data = np.frombuffer(audio_buffer, dtype=np.int16)
                    audio_float = audio_data.astype(np.float32) / 32767.0
                    print(f"[OrpheusTTS] Playing audio ({len(audio_float) / SAMPLE_RATE:.1f}s)...")
                    sd.play(audio_float, SAMPLE_RATE)
                    sd.wait()
                except Exception as e:
                    print(f"[OrpheusTTS] Playback error: {e}")

            total_time = time.time() - start_time
            print(f"[OrpheusTTS] Total time: {total_time:.2f}s")

            self.is_speaking = False
            return audio_buffer

        except Exception as e:
            print(f"[OrpheusTTS] Generation error: {e}")
            self.is_speaking = False
            return b""

    # ── Speak in background thread ──
    def speak_async(self, text: str, on_complete=None):
        """Generate and play speech in a background thread."""
        def _run():
            self.generate_speech(text, play=True)
            if on_complete:
                try:
                    on_complete()
                except Exception:
                    pass

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return thread

    # ── Stop playback ──
    def stop(self):
        """Stop any currently playing audio."""
        self.is_speaking = False
        if SD_AVAILABLE:
            try:
                sd.stop()
            except Exception:
                pass

    # ── Save to WAV file ──
    def save_to_wav(self, audio_bytes: bytes, filepath: str):
        """Save raw audio bytes to a WAV file."""
        if not audio_bytes:
            return

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_bytes)
        print(f"[OrpheusTTS] Saved to {filepath}")

    def set_voice(self, voice: str):
        """Change the speaking voice."""
        if voice in VOICES:
            self.voice = voice
        else:
            print(f"[OrpheusTTS] Unknown voice '{voice}'. Available: {VOICES}")
