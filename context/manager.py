import uuid
import time
from threading import Lock
from typing import Optional

SESSION_TTL = 1800  # seconds of inactivity before a session expires


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, dict] = {}
        self._lock = Lock()

    def get_or_create(self, session_id: Optional[str]) -> tuple[str, list]:
        if session_id and self._is_valid(session_id):
            return session_id, self._get_history(session_id)
        new_id = self._create()
        return new_id, []

    def add_messages(self, session_id: str, user_text: str, assistant_text: str):
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session["history"].append({"role": "user", "content": user_text})
                session["history"].append({"role": "assistant", "content": assistant_text})
                session["last_active"] = time.time()

    def clear(self, session_id: str):
        with self._lock:
            self._sessions.pop(session_id, None)

    # -- private --

    def _create(self) -> str:
        session_id = str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = {"history": [], "last_active": time.time()}
        return session_id

    def _is_valid(self, session_id: str) -> bool:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return False
            if time.time() - session["last_active"] > SESSION_TTL:
                del self._sessions[session_id]
                return False
            return True

    def _get_history(self, session_id: str) -> list:
        with self._lock:
            return list(self._sessions[session_id]["history"])


session_manager = SessionManager()
