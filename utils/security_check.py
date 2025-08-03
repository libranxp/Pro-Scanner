def check_token_security(token_info):
    return (
        token_info.get("sniffer_score", 0) >= 80 and
        token_info.get("renounced") is True and
        token_info.get("honeypot") is False
    )

