from enum import Enum


class ProjectRole(str, Enum):
    OWNER = "owner"
    PARTICIPANT = "paticipant"