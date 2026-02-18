from __future__ import annotations

try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None  # type: ignore[assignment]

try:
    import pyttsx3
except ModuleNotFoundError:
    pyttsx3 = None  # type: ignore[assignment]

try:
    import webrtcvad  # type: ignore
except ModuleNotFoundError:
    webrtcvad = None  # type: ignore[assignment]

try:
    import pvporcupine  # type: ignore
except ModuleNotFoundError:
    pvporcupine = None  # type: ignore[assignment]


class Speaker:
    def __init__(self, rate: int = 180, enabled: bool = True) -> None:
        self.engine = None
        if enabled and pyttsx3 is not None:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)

    def say(self, text: str) -> None:
        try:
            print(f"Assistant: {text}")
        except UnicodeEncodeError:
            safe = text.encode("ascii", errors="replace").decode("ascii")
            print(f"Assistant: {safe}")
        if self.engine is not None:
            self.engine.say(text)
            self.engine.runAndWait()


class Listener:
    def __init__(self, ambient_duration: float = 0.15, use_vad: bool = True, wake_word: str | None = None) -> None:
        self.recognizer = sr.Recognizer() if sr is not None else None
        self.ambient_duration = ambient_duration
        self._calibrated = False
        if self.recognizer is not None:
            self.recognizer.dynamic_energy_threshold = True
        self.use_vad = use_vad and webrtcvad is not None
        self.vad = webrtcvad.Vad(2) if self.use_vad else None
        self.wake_word = wake_word
        self._porcupine = None
        if wake_word and pvporcupine is not None:
            keyword = wake_word.lower()
            if keyword == "nova":
                self._porcupine = pvporcupine.create(keywords=["alexa"])  # using built-in as placeholder
            else:
                self._porcupine = None

    def listen(self, timeout: float = 2.0, phrase_time_limit: float = 5.0) -> str | None:
        if self.recognizer is None or sr is None:
            return None
        try:
            with sr.Microphone() as source:
                if not self._calibrated:
                    self.recognizer.adjust_for_ambient_noise(source, duration=self.ambient_duration)
                    self._calibrated = True
                if self.use_vad:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                else:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = self.recognizer.recognize_google(audio)
            return text.lower().strip()
        except Exception:
            return None
