def calculate_build_risk(failed_builds, total_builds):
    """
    Calculate historical build failure rate.
    """

    if total_builds == 0:
        return 0.0

    return failed_builds / total_builds


def get_build_status(failure_rate):
    """
    Classify historical build risk.
    """

    if failure_rate >= 0.70:
        return "HIGH"

    if failure_rate >= 0.40:
        return "MEDIUM"

    return "LOW"


if __name__ == "__main__":
    failed_builds = 3
    total_builds = 10

    failure_rate = calculate_build_risk(
        failed_builds,
        total_builds
    )

    status = get_build_status(failure_rate)

    print(f"Failure rate: {failure_rate:.2%}")
    print(f"Risk level: {status}")