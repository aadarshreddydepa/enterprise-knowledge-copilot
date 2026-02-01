from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user


def require_roles(*required_roles: str):
    async def role_checker(user = Depends(get_current_user)):
        if not hasattr(user, "roles"):
            raise HTTPException(status_code=403, detail="No roles assigned")

        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return role_checker
