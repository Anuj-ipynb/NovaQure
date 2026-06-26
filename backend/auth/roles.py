from enum import Enum


class UserRole(str, Enum):
    RESEARCHER = "researcher"
    ADMIN = "admin"
    SYSTEM = "system"
