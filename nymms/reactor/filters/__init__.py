import logging

logger = logging.getLogger(__name__)

from nymms import results


def hard_state(result, previous_state):
    if result.state_type == results.HARD:
        logger.debug("%s state_type is HARD.", result.id)
        return True
    return False


def changed_state(result, previous_state):
    """ Only alert if the state is new or has either changed state or
    state_type.
    """
    if not previous_state:
        logger.debug("No previous state found.")
        return True
    if not previous_state.state == result.state:
        logger.debug("Previous state (%s) does not match current "
                     "state (%s).", previous_state.state_name,
                     result.state_name)
        return True
    if not previous_state.state_type == result.state_type:
        logger.debug("Previous state_type (%s) does not match current "
                     "state_type (%s).",
                     previous_state.state_type_name,
                     result.state_type_name)
        return True
    return False


def ok_state(result, previous_state):
    if result.state == results.OK:
        return True
    return False


def warning_state(result, previous_state):
    if result.state == results.WARNING:
        return True
    return False


def critical_state(result, previous_state):
    if result.state == results.CRITICAL:
        return True
    return False


def unknown_state(result, previous_state):
    if result.state >= results.UNKNOWN:
        return True
    return False
