import random
from typing import Optional, Tuple
from telegram import ChatMemberUpdated, ChatMember

def assign_role() -> str:
    return random.choice(["Hacker", "Defender"])

def get_event_info() -> str:
    return "Cyberpunk Dance Class: Date TBA, Location: Classified"

def get_mission_briefing() -> str:
    briefings = [
        "Infiltrate the mainframe. Dance is your weapon.",
        "Defend the firewall. Your moves are the last line of defense.",
        "Data corruption detected. Purge the system with your rhythm."
    ]
    return random.choice(briefings)

def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member
