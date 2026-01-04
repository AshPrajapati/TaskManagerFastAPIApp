from datetime import timedelta

from app.core.security import create_access_token


def get_test_token(user_id: int) -> str:
    return create_access_token(
        data={"sub": f"{user_id}"},
        expires_delta=timedelta(minutes=10),
    )
