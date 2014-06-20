from datetime import datetime
from django.utils.timezone import UTC

def is_xblock_visible_to_students(xblock):
    """
    Checks if the given xblock is visible to a student enrolled in the course
    :param xblock: xblock to check
    :return: true if the xblock is visible
    """
    # If the block is a draft then it's not visible
    if getattr(xblock, 'is_draft', False):
        return False

    # Check start date
    if 'detached' not in xblock._class_tags and xblock.start is not None:
        return datetime.now(UTC()) > xblock.start

    # No start date, so can always load.
    return True