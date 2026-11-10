
import logging

from app.database import get_connection
from app.security import verify_password, create_access_token

logger = logging.getLogger(__name__)


def authenticate_user(email: str, password: str):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT user_id, email, password_hash, role, is_active
            FROM dbo.Users
            WHERE email = ?
            """,
            (email,),
        )

        user = cursor.fetchone()

        # Use a generic failure response for invalid credentials.
        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token = create_access_token(
            subject=str(user.user_id),
            role=user.role,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 30 * 60,
        }

    except Exception:
        logger.exception("Authentication service failed")
        raise

    finally:
        if connection is not None:
            connection.close()

def get_user_profile(user_id: int):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT user_id, email, role, is_active
            FROM dbo.Users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        user = cursor.fetchone()

        # Deleted or deactivated users lose access immediately.
        if user is None or not user.is_active:
            return None

        return {
            "user_id": int(user.user_id),
            "email": user.email,
            "role": user.role,
        }

    finally:
        if connection is not None:
            connection.close()