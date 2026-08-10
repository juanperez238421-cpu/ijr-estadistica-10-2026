# Runtime compatibility adapter for the exact user source.
# The user source file is never edited; its SHA-256 remains verified separately.

from manim import Mobject, VGroup as ManimVGroup
import physics9_motion_exact_user as source


class CompatVGroup(ManimVGroup):
    """Accept structured JP helper returns by unwrapping their `.group` Mobject."""

    def __init__(self, *items, **kwargs):
        normalized = []
        for item in items:
            if not isinstance(item, Mobject) and hasattr(item, "group"):
                item = item.group
            normalized.append(item)
        super().__init__(*normalized, **kwargs)


# Patch only the source module's VGroup symbol at runtime.
# No source bytes, pedagogy, geometry, timing, values, or animations are modified.
source.VGroup = CompatVGroup


class Physics9MotionAchillesFull(source.Physics9MotionAchillesFull):
    pass
