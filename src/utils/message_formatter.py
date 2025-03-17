def get_formatted_profile(user):
    profile_text = (
        f"*👤 Profile:*\n"
        f"*Name:* {user["username"]}\n"
        f"*NU ID:* {user["nu_id"] if user["nu_id"] else "n/a"}\n"
        f"*Gender:* {user["age"]}\n"
        f"*Gender:* {user["gender"]}\n"
        f"*Looking for:* {user["preference"]}\n"
        f"*Course:* {user["course"]} year\n"
        f"*Description:* {user["description"]}\n"
    )

    return profile_text


def get_formatted_anketa(user):
    anketa_text = (
        f"{user['username']}, {user['course']} year\n"
        f"{user['description']}"
    )
    return anketa_text
