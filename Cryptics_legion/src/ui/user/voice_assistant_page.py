# src/ui/user/voice_assistant_page.py
"""
Full-screen Voice Assistant page with waveform visualization,
AI conversation, TTS speech output via Orpheus, and personalized greeting.

OPTIMIZED: 
- TTS greeting removed (instant page load)
- TTS initialization is lazy (background thread)
- Session guard prevents re-greeting on back-navigation
"""

import flet as ft
import threading
import time
import random
from datetime import datetime
from core import db
from core.theme import get_theme
from utils.voice_expense_ai import VoiceExpenseAI
from utils.currency import get_currency_symbol

# ── TTS import (graceful) ──
try:
    from utils.orpheus_tts import OrpheusTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


def build_voice_assistant_content(page: ft.Page, state: dict, toast, go_back, show_add_expense):
    """Build the voice assistant full-screen page."""
    theme = get_theme()
    voice_ai = VoiceExpenseAI(model="llama3.2")
    
    # ── Initialize TTS engine (lazy — availability checked in background) ──
    tts_engine = None
    if TTS_AVAILABLE:
        tts_engine = OrpheusTTS(voice="tara")
    
    # ── Get user info for greeting ──
    user_info = db.get_user_profile(state["user_id"]) if state.get("user_id") else None
    user_name = ""
    if user_info:
        user_name = user_info.get("first_name", "") or user_info.get("username", "")
    
    # ── Time-based greeting ──
    hour = datetime.now().hour
    if hour < 12:
        greeting_time = "Good morning"
        greeting_emoji = "☀️"
    elif hour < 17:
        greeting_time = "Good afternoon"
        greeting_emoji = "🌤️"
    else:
        greeting_time = "Good evening"
        greeting_emoji = "🌙"
    
    greeting_text = f"{greeting_time}, {user_name}!" if user_name else f"{greeting_time}!"
    
    # ── Recording & speaking state ──
    rec_state = {
        "is_recording": False,
        "is_processing": False,
        "is_speaking": False,
        "animation_running": False,
        "tts_enabled": False,  # Start disabled, enable once background check passes
        "tts_ready": False,
        "tts_checking": True,  # Background availability check in progress
    }
    
    # ── Waveform Bars ──
    NUM_BARS = 28
    bar_containers = []
    for i in range(NUM_BARS):
        bar = ft.Container(
            width=4,
            height=4,
            bgcolor="#7C3AED",
            border_radius=2,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )
        bar_containers.append(bar)
    
    waveform_row = ft.Row(
        bar_containers,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=3,
    )
    
    waveform_container = ft.Container(
        content=waveform_row,
        height=60,
        alignment=ft.alignment.center,
        visible=False,
    )
    
    # ── Chat area ──
    chat_column = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO, auto_scroll=True)
    
    chat_area = ft.Container(
        content=chat_column,
        expand=True,
        padding=ft.padding.symmetric(vertical=8, horizontal=4),
    )
    
    # ── Status text ──
    status_text = ft.Text(
        "🎤 Tap the microphone to start",
        size=13, color=theme.text_muted,
        text_align=ft.TextAlign.CENTER,
    )
    
    # ── Mic button elements ──
    mic_icon = ft.Icon(ft.Icons.MIC, color="white", size=32)
    
    # ── TTS toggle button ──
    tts_icon = ft.Icon(
        ft.Icons.HOURGLASS_EMPTY_ROUNDED,
        color=theme.text_muted,
        size=20,
    )
    
    tts_label = ft.Text(
        "Checking...",
        size=9,
        color=theme.text_muted,
        weight=ft.FontWeight.BOLD,
    )
    
    def toggle_tts(e=None):
        """Toggle TTS on/off."""
        if not rec_state["tts_ready"]:
            if rec_state["tts_checking"]:
                toast("⏳ Voice engine still loading...", "#F59E0B")
            else:
                toast("⚠️ Orpheus TTS not available. Check Ollama.", "#EF4444")
            return
        rec_state["tts_enabled"] = not rec_state["tts_enabled"]
        if rec_state["tts_enabled"]:
            tts_icon.name = ft.Icons.VOLUME_UP_ROUNDED
            tts_icon.color = "#10B981"
            tts_label.value = "Voice ON"
            tts_label.color = "#10B981"
        else:
            tts_icon.name = ft.Icons.VOLUME_OFF_ROUNDED
            tts_icon.color = theme.text_muted
            tts_label.value = "Voice OFF"
            tts_label.color = theme.text_muted
            # Stop any current speech
            if tts_engine:
                tts_engine.stop()
                rec_state["is_speaking"] = False
        page.update()
    
    tts_toggle = ft.Container(
        content=ft.Column([
            tts_icon,
            tts_label,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        on_click=toggle_tts,
        ink=True,
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        tooltip="Toggle AI voice responses",
    )
    
    # ── TTS status indicator (initially shows "Checking...") ──
    tts_status_text_val = "Checking Voice..."
    tts_status_color = "#F59E0B"
    
    tts_status_badge = ft.Container(
        content=ft.Row([
            ft.Icon(
                ft.Icons.HOURGLASS_EMPTY_ROUNDED,
                color=tts_status_color,
                size=12,
            ),
            ft.Text(tts_status_text_val, size=9, color=tts_status_color, weight=ft.FontWeight.W_500),
        ], spacing=4),
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=10,
        bgcolor=f"{tts_status_color}15",
        border=ft.border.all(1, f"{tts_status_color}30"),
    )
    
    # ── Background TTS availability check ──
    def check_tts_in_background():
        """Check TTS availability without blocking UI."""
        if not TTS_AVAILABLE or not tts_engine:
            rec_state["tts_checking"] = False
            rec_state["tts_ready"] = False
            try:
                tts_status_badge.content.controls[0].name = ft.Icons.VOICE_OVER_OFF_ROUNDED
                tts_status_badge.content.controls[0].color = "#EF4444"
                tts_status_badge.content.controls[1].value = "Voice Unavailable"
                tts_status_badge.content.controls[1].color = "#EF4444"
                tts_status_badge.bgcolor = "#EF444415"
                tts_status_badge.border = ft.border.all(1, "#EF444430")
                tts_icon.name = ft.Icons.VOLUME_OFF_ROUNDED
                tts_label.value = "Voice OFF"
                page.update()
            except Exception:
                pass
            return
        
        avail, err = tts_engine.check_available()
        rec_state["tts_checking"] = False
        rec_state["tts_ready"] = avail
        rec_state["tts_enabled"] = avail  # Auto-enable if available
        
        try:
            if avail:
                tts_status_badge.content.controls[0].name = ft.Icons.RECORD_VOICE_OVER_ROUNDED
                tts_status_badge.content.controls[0].color = "#10B981"
                tts_status_badge.content.controls[1].value = "Orpheus Voice Active"
                tts_status_badge.content.controls[1].color = "#10B981"
                tts_status_badge.bgcolor = "#10B98115"
                tts_status_badge.border = ft.border.all(1, "#10B98130")
                tts_icon.name = ft.Icons.VOLUME_UP_ROUNDED
                tts_icon.color = "#10B981"
                tts_label.value = "Voice ON"
                tts_label.color = "#10B981"
            else:
                tts_status_badge.content.controls[0].name = ft.Icons.VOICE_OVER_OFF_ROUNDED
                tts_status_badge.content.controls[0].color = "#EF4444"
                tts_status_badge.content.controls[1].value = "Voice Unavailable"
                tts_status_badge.content.controls[1].color = "#EF4444"
                tts_status_badge.bgcolor = "#EF444415"
                tts_status_badge.border = ft.border.all(1, "#EF444430")
                tts_icon.name = ft.Icons.VOLUME_OFF_ROUNDED
                tts_icon.color = theme.text_muted
                tts_label.value = "Voice OFF"
                tts_label.color = theme.text_muted
                print(f"[VoiceAssistant] TTS not available: {err}")
            page.update()
        except Exception:
            pass
    
    # Launch background TTS check (does NOT block page rendering)
    threading.Thread(target=check_tts_in_background, daemon=True).start()
    
    # ── Confirm row (hidden until AI understands) ──
    confirm_row = ft.Row([], alignment=ft.MainAxisAlignment.CENTER, spacing=12, visible=False)
    
    # ── Helper: add chat bubble ──
    def add_bubble(role, text):
        if role == "user":
            bubble = ft.Container(
                content=ft.Row([
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, color="white", size=12),
                                ft.Text("You", size=9, color="#ffffffaa", weight=ft.FontWeight.BOLD),
                            ], spacing=4),
                            ft.Text(text, color="white", size=13),
                        ], spacing=4),
                        bgcolor="#4F46E5",
                        border_radius=ft.border_radius.only(
                            top_left=16, top_right=16, bottom_left=16, bottom_right=4,
                        ),
                        padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    ),
                ]),
                padding=ft.padding.only(left=40),
            )
        elif role == "ai":
            # Build speaking indicator
            speaking_indicator = ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME, color="#FFD700", size=12),
                ft.Text("AI Assistant", size=9, color="#FFD700", weight=ft.FontWeight.BOLD),
                # Small speaker icon if TTS is active
                ft.Icon(
                    ft.Icons.VOLUME_UP_ROUNDED,
                    color="#10B981",
                    size=10,
                    visible=rec_state["tts_enabled"],
                ),
            ], spacing=4)
            
            bubble = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Column([
                            speaking_indicator,
                            ft.Text(text, color=theme.text_primary, size=13),
                        ], spacing=4),
                        bgcolor=f"{theme.accent_primary}18",
                        border_radius=ft.border_radius.only(
                            top_left=16, top_right=16, bottom_left=4, bottom_right=16,
                        ),
                        padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    ),
                    ft.Container(expand=True),
                ]),
                padding=ft.padding.only(right=40),
            )
        else:
            bubble = ft.Container(
                content=ft.Text(
                    text, color="#F59E0B", size=11,
                    text_align=ft.TextAlign.CENTER, italic=True,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=4),
            )
        chat_column.controls.append(bubble)
    
    # ── Speak AI response via TTS ──
    def speak_response(text: str):
        """Speak the AI response text using Orpheus TTS in background."""
        if not rec_state["tts_enabled"] or not tts_engine or not rec_state["tts_ready"]:
            return
        
        # Clean text for TTS (remove emojis and special chars that confuse TTS)
        clean_text = text
        for char in ["✅", "✓", "⚠️", "❌", "🎤", "💰", "📝", "🔴", "🤔", "₱", "$", "€", "¥", "£"]:
            clean_text = clean_text.replace(char, "")
        clean_text = clean_text.strip()
        
        if not clean_text or len(clean_text) < 3:
            return
        
        rec_state["is_speaking"] = True
        status_text.value = "🔊 AI is speaking..."
        waveform_container.visible = True
        
        try:
            page.update()
        except Exception:
            pass
        
        # Animate speaking waveform
        def animate_speaking():
            while rec_state["is_speaking"]:
                for bar in bar_containers:
                    bar.height = random.randint(4, 35)
                    bar.bgcolor = random.choice(["#06B6D4", "#3B82F6", "#8B5CF6", "#10B981"])
                try:
                    page.update()
                except Exception:
                    break
                time.sleep(0.1)
            
            # Reset bars
            for bar in bar_containers:
                bar.height = 4
                bar.bgcolor = "#7C3AED"
            waveform_container.visible = False
            try:
                page.update()
            except Exception:
                pass
        
        def on_speech_done():
            rec_state["is_speaking"] = False
            status_text.value = "🎤 Tap mic to continue"
            try:
                page.update()
            except Exception:
                pass
        
        # Start speaking animation
        threading.Thread(target=animate_speaking, daemon=True).start()
        # Start TTS in background
        tts_engine.speak_async(clean_text, on_complete=on_speech_done)
    
    # ── Waveform animation for recording ──
    def animate_waveform():
        """Animate waveform bars while recording."""
        rec_state["animation_running"] = True
        waveform_container.visible = True
        try:
            page.update()
        except Exception:
            pass
        
        while rec_state["is_recording"] or rec_state["is_processing"]:
            for bar in bar_containers:
                if rec_state["is_recording"]:
                    # Active recording — energetic bars (purple/pink)
                    bar.height = random.randint(6, 50)
                    bar.bgcolor = random.choice(["#7C3AED", "#EC4899", "#A855F7", "#8B5CF6"])
                else:
                    # Processing — gentle pulse (amber)
                    bar.height = random.randint(4, 20)
                    bar.bgcolor = "#7C3AED"
            try:
                page.update()
            except Exception:
                break
            time.sleep(0.12)
        
        # Reset bars (only if not speaking)
        if not rec_state["is_speaking"]:
            for bar in bar_containers:
                bar.height = 4
                bar.bgcolor = "#7C3AED"
            waveform_container.visible = False
        rec_state["animation_running"] = False
        try:
            page.update()
        except Exception:
            pass
    
    # ── Apply results to state and go back ──
    def apply_and_go_back(e=None):
        """Save extracted data to state and navigate back to add expense."""
        # Stop any speaking
        if tts_engine:
            tts_engine.stop()
            rec_state["is_speaking"] = False
        
        extracted = voice_ai.get_extracted()
        state["voice_expense_data"] = extracted
        toast("✓ Voice data ready! Review and save.", "#10B981")
        if show_add_expense:
            show_add_expense()
    
    # ── Mic tap handler ──
    def on_mic_tap(e=None):
        if rec_state["is_recording"] or rec_state["is_processing"]:
            return
        
        # Stop any current speech before recording
        if rec_state["is_speaking"] and tts_engine:
            tts_engine.stop()
            rec_state["is_speaking"] = False
        
        rec_state["is_recording"] = True
        status_text.value = "🔴 Listening... speak now (5 seconds)"
        mic_icon.name = ft.Icons.HEARING
        confirm_row.visible = False
        page.update()
        
        # Start waveform animation
        if not rec_state["animation_running"]:
            threading.Thread(target=animate_waveform, daemon=True).start()
        
        def do_voice_flow():
            # Record
            text, err = voice_ai.record_and_transcribe(duration=5)
            rec_state["is_recording"] = False
            
            if err:
                rec_state["is_processing"] = False
                add_bubble("system", f"⚠️ {err}")
                status_text.value = "🎤 Tap mic to try again"
                mic_icon.name = ft.Icons.MIC
                page.update()
                return
            
            # Show transcribed text
            add_bubble("user", text)
            rec_state["is_processing"] = True
            status_text.value = "🤔 AI is thinking..."
            mic_icon.name = ft.Icons.PSYCHOLOGY
            page.update()
            
            # Parse with Ollama
            result = voice_ai.parse_expense(text)
            rec_state["is_processing"] = False
            
            if "error" in result:
                add_bubble("system", f"⚠️ {result['error']}")
                status_text.value = "🎤 Tap mic to try again"
            else:
                ai_msg = result.get("message", "I processed your request.")
                add_bubble("ai", ai_msg)
                
                # ── SPEAK the AI response! ──
                speak_response(ai_msg)
                
                if result.get("understood"):
                    status_text.value = "✅ Ready! Tap 'Add This Expense' to confirm"
                    
                    # Build confirm buttons
                    confirm_row.controls.clear()
                    confirm_row.controls.extend([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color="white", size=18),
                                ft.Text("Add This Expense", color="white", size=13, weight=ft.FontWeight.W_600),
                            ], spacing=6, alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor="#10B981",
                            border_radius=12,
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            on_click=apply_and_go_back,
                            ink=True,
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.MIC, color=theme.text_muted, size=16),
                                ft.Text("Redo", color=theme.text_muted, size=12),
                            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                            border=ft.border.all(1, theme.border_primary),
                            border_radius=12,
                            padding=ft.padding.symmetric(horizontal=16, vertical=12),
                            on_click=on_mic_tap,
                            ink=True,
                        ),
                    ])
                    confirm_row.visible = True
                else:
                    follow_up = result.get("follow_up", "")
                    status_text.value = "🎤 Tap mic to answer the question"
            
            mic_icon.name = ft.Icons.MIC
            page.update()
        
        threading.Thread(target=do_voice_flow, daemon=True).start()
    
    # ── Check dependencies on page load ──
    dep_issues = voice_ai.check_dependencies()
    if dep_issues:
        add_bubble("system", f"⚠️ {dep_issues[0]}")
        status_text.value = "⚠️ Setup required — see message above"
    else:
        # Show text greeting only (NO TTS greeting — eliminates delay)
        # Only show if not already shown in this session (prevents re-greeting on back-nav)
        if not state.get("_voice_greeting_shown"):
            greeting_msg = (
                f"{greeting_text} {greeting_emoji}\n"
                f"I'm your AI expense assistant.\n\n"
                f"Just tap the mic and tell me what you spent — "
                f"like \"I spent 500 pesos on Starbucks coffee\" and I'll handle the rest!"
            )
            add_bubble("ai", greeting_msg)
            state["_voice_greeting_shown"] = True
        else:
            # Returning to voice assistant — show a shorter message
            add_bubble("ai", "Welcome back! 🎤 Tap the mic to add another expense.")
    
    # ══════════ BUILD UI ══════════
    
    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=theme.text_primary,
                    icon_size=20,
                    on_click=lambda e: _handle_back(),
                ),
                ft.Text("Voice Assistant", size=18, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.AUTO_AWESOME, color="#FFD700", size=14),
                            ft.Text("AI", size=10, color="#FFD700", weight=ft.FontWeight.BOLD),
                        ], spacing=3),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=10,
                        bgcolor=f"{theme.accent_primary}25",
                    ),
                    tts_toggle,
                ], spacing=4),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            # TTS status badge
            ft.Container(
                content=tts_status_badge,
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=4),
            ),
        ], spacing=2),
        padding=ft.padding.only(bottom=4),
    )
    
    def _handle_back():
        """Handle back navigation - stop TTS first."""
        if tts_engine:
            tts_engine.stop()
            rec_state["is_speaking"] = False
        if go_back:
            go_back()
    
    # Mic button with glow
    mic_button = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Container(
                    content=mic_icon,
                    width=72, height=72,
                    border_radius=36,
                    gradient=ft.LinearGradient(
                        colors=["#7C3AED", "#EC4899"],
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=2, blur_radius=25,
                        color="#7C3AED50",
                    ),
                ),
                on_click=on_mic_tap,
                ink=True,
                border_radius=36,
            ),
            ft.Container(height=4),
            ft.Text("Tap to Speak", size=11, color=theme.text_muted),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=8, bottom=12),
    )
    
    # Main layout
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=16, right=16, top=10),
        content=ft.Column([
            header,
            # Chat area (expandable)
            chat_area,
            # Waveform visualization
            waveform_container,
            # Status
            ft.Container(
                content=status_text,
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=6, bottom=2),
            ),
            # Confirm buttons
            ft.Container(
                content=confirm_row,
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=4),
            ),
            # Mic button
            mic_button,
        ], expand=True, spacing=0),
    )
