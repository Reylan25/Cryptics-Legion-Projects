# src/utils/biometric.py
"""
Cross-platform biometric authentication module.
Supports Windows Hello and Android BiometricPrompt.
"""

import platform
import threading
from typing import Callable, Optional

# Platform detection
PLATFORM = platform.system()
IS_WINDOWS = PLATFORM == "Windows"
IS_ANDROID = PLATFORM == "Linux" and hasattr(platform, 'java_ver')

# Import platform-specific modules
if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes
    print("✓ Windows biometric support available")

if IS_ANDROID:
    try:
        from jnius import autoclass, cast
        from jnius import PythonJavaClass, java_method
        print("✓ Android biometric support available")
    except ImportError:
        print("⚠ Android biometric requires Pyjnius (will use passcode fallback)")


class BiometricManager:
    """Unified biometric authentication manager for Windows and Android."""
    
    def __init__(self):
        self.is_available = self._check_availability()
        self.last_error = None
    
    def _check_availability(self) -> bool:
        """Check if biometric is available on this platform."""
        if IS_WINDOWS:
            try:
                ctypes.windll.credui
                return True
            except:
                return False
        
        if IS_ANDROID:
            try:
                from jnius import autoclass
                BiometricPrompt = autoclass('androidx.biometric.BiometricPrompt')
                return True
            except:
                return False
        
        return False
    
    def authenticate(self, user_name: str, on_success: Callable, on_error: Callable):
        """
        Trigger biometric authentication.
        
        Args:
            user_name: User's display name
            on_success: Callback function when authentication succeeds
            on_error: Callback function when authentication fails (receives error message)
        """
        if not self.is_available:
            on_error("Biometric not available on this device")
            return
        
        if IS_WINDOWS:
            self._authenticate_windows(user_name, on_success, on_error)
        elif IS_ANDROID:
            self._authenticate_android(user_name, on_success, on_error)
        else:
            on_error("Unsupported platform")
    
    def _authenticate_windows(self, user_name: str, on_success: Callable, on_error: Callable):
        """Windows Hello authentication using CredUI."""
        def auth_thread():
            try:
                import ctypes
                from ctypes import wintypes
                
                # CredUI flags for biometric support
                CREDUI_FLAGS_ALWAYS_SHOW_UI = 0x00000080
                CREDUI_FLAGS_GENERIC_CREDENTIALS = 0x00000001
                CREDUI_FLAGS_SHOW_SAVE_CHECK_BOX = 0x00000002
                
                flags = (CREDUI_FLAGS_ALWAYS_SHOW_UI | 
                        CREDUI_FLAGS_GENERIC_CREDENTIALS |
                        CREDUI_FLAGS_SHOW_SAVE_CHECK_BOX)
                
                # Create character buffers
                max_username_len = 513
                max_password_len = 256
                
                username_buffer = ctypes.create_unicode_buffer(max_username_len)
                password_buffer = ctypes.create_unicode_buffer(max_password_len)
                save_creds = wintypes.BOOL()
                
                # Get credui function
                credui_dll = ctypes.windll.credui
                
                # Prepare parameters
                title = "Expense Tracker - Biometric Authentication"
                message = f"Authenticate using Windows Hello\n{user_name}'s Account"
                
                # Call Windows Credential Dialog
                result = credui_dll.CredUIPromptForCredentialsW(
                    None,
                    ctypes.c_wchar_p(title),
                    ctypes.c_wchar_p(message),
                    0,
                    ctypes.byref(username_buffer),
                    max_username_len,
                    ctypes.byref(password_buffer),
                    max_password_len,
                    ctypes.byref(save_creds),
                    flags
                )
                
                # Result: 0 = success, 1223 = cancelled, other = error
                if result == 0:
                    on_success()
                elif result == 1223:
                    on_error("Authentication cancelled")
                else:
                    on_error(f"Authentication failed (code: {result})")
            
            except Exception as e:
                self.last_error = str(e)
                on_error(f"Error: {str(e)[:50]}")
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def _authenticate_android(self, user_name: str, on_success: Callable, on_error: Callable):
        """Android BiometricPrompt authentication."""
        def auth_thread():
            try:
                from jnius import autoclass, PythonJavaClass, java_method, cast
                
                # Android classes
                BiometricPrompt = autoclass('androidx.biometric.BiometricPrompt')
                BiometricPrompt_PromptInfo = autoclass('androidx.biometric.BiometricPrompt$PromptInfo')
                CancellationSignal = autoclass('android.os.CancellationSignal')
                Executor = autoclass('java.util.concurrent.Executor')
                Activity = autoclass('android.app.Activity')
                
                # Get current activity
                try:
                    from jnius import autoclass as ac
                    PythonActivity = ac('org.kivy.android.PythonActivity')
                    activity = PythonActivity.mActivity
                except:
                    on_error("Cannot access Android activity")
                    return
                
                # Create biometric callback
                class BiometricCallback(PythonJavaClass):
                    __javainterfaces__ = ('androidx/biometric/BiometricPrompt$AuthenticationCallback',)
                    
                    def __init__(self, on_success, on_error):
                        super().__init__()
                        self.on_success = on_success
                        self.on_error = on_error
                    
                    @java_method('(Landroidx/biometric/BiometricPrompt$AuthenticationResult;)V')
                    def onAuthenticationSucceeded(self, result):
                        """Called when biometric is authenticated."""
                        self.on_success()
                    
                    @java_method('(I)V')
                    def onAuthenticationError(self, error_code):
                        """Called when authentication error occurs."""
                        error_messages = {
                            1: "Biometric operation cancelled",
                            2: "Signal not found (timeout)",
                            3: "Not enrolled",
                            4: "User cancelled",
                            5: "Device credentials not available",
                            6: "Security update required",
                            7: "Biometric hardware unavailable",
                            8: "Negative button pressed",
                        }
                        msg = error_messages.get(error_code, f"Auth failed (code {error_code})")
                        self.on_error(msg)
                    
                    @java_method('(I)V')
                    def onAuthenticationFailed(self):
                        """Called when authentication attempt fails."""
                        self.on_error("Fingerprint not recognized. Try again.")
                
                # Create prompt info
                prompt_info = BiometricPrompt_PromptInfo.Builder()
                prompt_info = prompt_info.setTitle("Biometric Unlock")
                prompt_info = prompt_info.setSubtitle(f"Unlock {user_name}'s Expense Tracker")
                prompt_info = prompt_info.setDescription("Use your fingerprint, face, or pattern to authenticate")
                prompt_info = prompt_info.setNegativeButtonText("Cancel")
                prompt_info = prompt_info.build()
                
                # Create executor
                class SimpleExecutor(PythonJavaClass):
                    __javainterfaces__ = ('java/util/concurrent/Executor',)
                    
                    @java_method('(Ljava/lang/Runnable;)V')
                    def execute(self, command):
                        try:
                            command.run()
                        except:
                            pass
                
                executor = SimpleExecutor()
                
                # Create biometric prompt
                biometric = BiometricPrompt(activity, executor, BiometricCallback(on_success, on_error))
                
                # Start authentication
                biometric.authenticate(prompt_info)
            
            except ImportError:
                on_error("Biometric module not available. Use passcode.")
            except Exception as e:
                self.last_error = str(e)
                on_error(f"Biometric error: {str(e)[:40]}")
        
        threading.Thread(target=auth_thread, daemon=True).start()


# Global instance
biometric_manager = BiometricManager()


def is_biometric_available() -> bool:
    """Check if biometric authentication is available."""
    return biometric_manager.is_available


def authenticate_biometric(user_name: str, on_success: Callable, on_error: Callable):
    """
    Trigger biometric authentication.
    
    Args:
        user_name: User's display name
        on_success: Callback when authentication succeeds
        on_error: Callback when authentication fails (receives error message)
    """
    biometric_manager.authenticate(user_name, on_success, on_error)


def get_last_error() -> Optional[str]:
    """Get the last biometric error."""
    return biometric_manager.last_error
