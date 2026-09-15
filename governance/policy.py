ALLOWED_ACTIONS = {
    "investigate",
    "recommend",
    "summarise"
}

BLOCKED_ACTIONS = {
    "delete",
    "shutdown",
    "modify_production",
    "restart_service"
}


def check_action(action):

    if action in BLOCKED_ACTIONS:
        return {
            "allowed": False,
            "reason": f"Action '{action}' requires human approval."
        }

    if action not in ALLOWED_ACTIONS:
        return {
            "allowed": False,
            "reason": f"Unknown action '{action}'."
        }

    return {
        "allowed": True,
        "reason": "Action permitted."
    }