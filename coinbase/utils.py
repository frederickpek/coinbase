def get_query_params_str(params: dict):
    if not params:
        return ""
    return "?" + "&".join(f"{k}={v}" for k, v in params.items())
