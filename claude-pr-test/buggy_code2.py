"""
User authentication module with intentional bugs for testing Claude PR review. Minor update
"""

import re
from typing import Optional


class UserManager:
    """Manages user accounts with several intentional issues."""
    
    def __init__(self):
        self.users = {}
        self.api_key = "sk-1234567890abcdef"  # BUG: Hardcoded API key
        self.password_salt = "salt123"  # BUG: Weak/hardcoded salt
    
    def register_user(self, email: str, password: str) -> bool:
        """
        Register a new user.
        BUG: No validation, SQL injection risk, no error handling
        """
        # BUG: No email validation
        if email in self.users:
            return False
        
        # BUG: Password stored in plain text (major security issue)
        self.users[email] = {
            "password": password,
            "created_at": None,  # BUG: Never set
            "verified": False
        }
        return True
    
    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """
        Authenticate a user.
        BUG: No password hashing, timing attack vulnerable
        """
        if email not in self.users:
            return None
        
        # BUG: Direct string comparison (timing attack vulnerability)
        if self.users[email]["password"] == password:
            return self.users[email]
        
        return None
    
    def send_email(self, email: str, subject: str, body: str) -> bool:
        """
        Send email to user.
        BUG: No actual implementation, missing error handling
        """
        # TODO: Implement email sending
        # This will always return True without doing anything
        print(f"Sending email to {email}")
        return True
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format.
        BUG: Overly permissive regex, missing TLD validation
        """
        # BUG: This regex allows invalid emails like "user@domain"
        pattern = r"^[a-zA-Z0-9@.]*$"
        return bool(re.match(pattern, email))
    
    def reset_password(self, email: str, new_password: str) -> bool:
        """
        Reset user password.
        BUG: No verification token, race condition possible
        """
        if email not in self.users:
            return False
        
        # BUG: Direct password update without verification
        self.users[email]["password"] = new_password
        return True
    
    def get_user_count(self):
        """
        Get number of registered users.
        BUG: Type hint missing, inconsistent return
        """
        # BUG: Sometimes returns int, sometimes returns None
        if len(self.users) == 0:
            return None
        return len(self.users)
    
    def delete_user(self, email):
        """
        Delete a user account.
        BUG: No backup, irreversible, missing audit log
        """
        # BUG: No verification, anyone could delete accounts
        del self.users[email]
    
    def list_all_users(self):
        """
        List all users.
        BUG: Privacy violation, returns passwords
        """
        # BUG: Returns all user data including passwords
        return self.users


def process_user_data(users_list: list) -> dict:
    """
    Process list of users.
    BUG: No error handling, inefficient algorithm
    """
    results = {}
    
    # BUG: O(n²) algorithm, inefficient
    for user1 in users_list:
        for user2 in users_list:
            if user1["email"] == user2["email"] and user1 != user2:
                results[user1["email"]] = "duplicate"
    
    # BUG: What if users_list is empty? IndexError possible
    # BUG: No validation of required fields
    return results


class SessionManager:
    """Manage user sessions.
    BUG: Multiple thread-safety issues
    """
    
    def __init__(self):
        self.sessions = {}  # BUG: No thread lock
        self.session_timeout = 3600
    
    def create_session(self, user_id: str) -> str:
        """Create a new session."""
        # BUG: Weak session ID (predictable)
        session_id = str(len(self.sessions) + 1)
        self.sessions[session_id] = user_id
        return session_id
    
    def get_session(self, session_id: str):
        """Get session details."""
        # BUG: No bounds checking, could expose other sessions
        return self.sessions[session_id]
    
    def clear_expired_sessions(self):
        """Clear expired sessions."""
        # BUG: Not implemented
        pass


# BUG: Test code left in production
if __name__ == "__main__":
    manager = UserManager()
    manager.register_user("test@example.com", "password123")
    print("User registered!")  # BUG: No actual test assertions