from telegram import ChatMemberAdministrator, ChatMemberRestricted, ChatMember

ADMIN_PERMS = [
    ("can_delete_messages", "Delete Messages"),
    ("can_restrict_members", "Ban Users"),
    ("can_invite_users", "Invite Users"),
    ("can_promote_members", "Add New Admins"),
    ("can_pin_messages", "Pin Messages"),
    ("can_manage_video_chats", "Manage Video Chats"),
    ("can_manage_topics", "Manage Topics"),
]

def format_admin_perms(member: ChatMemberAdministrator) -> str:
    lines = []
    for attr, label in ADMIN_PERMS:
        val = getattr(member, attr, None)
        if val is None:
            continue
        icon = "✅" if val else "❌"
        lines.append(f"{icon} {label}")
    return "\n".join(lines)

def format_restrictions(member: ChatMemberRestricted) -> str:
    perms = [
        ("can_send_messages", "Send Messages"),
        ("can_send_media_messages", "Send Media"),
        ("can_send_stickers", "Send Stickers"),
        ("can_send_polls", "Send Polls"),
        ("can_add_web_page_previews", "Web Previews"),
    ]
    lines = []
    for attr, label in perms:
        val = getattr(member, attr, None)
        if val is None:
            continue
        icon = "❌" if not val else "✅"
        lines.append(f"{icon} {label}")
    return "\n".join(lines)

def diff_members(old: ChatMember, new: ChatMember) -> dict:
    changes = {}
    for attr in dir(old):
        if attr.startswith("_") or attr == "user":
            continue
        old_v = getattr(old, attr, None)
        new_v = getattr(new, attr, None)
        if old_v != new_v:
            changes[attr] = (old_v, new_v)
    return changes
