"""Here I will define the utility functions, I will need"""


def getMaxLength(messages):
    ans = 0
    for message in messages:
        ans = max(ans, len(message))
    return ans


def isValid(b: int) -> bool:
    return (65 <= b <= 90) or (97 <= b <= 122)
