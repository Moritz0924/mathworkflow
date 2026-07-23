from __future__ import annotations

from collections.abc import Callable, Iterable


Interval = tuple[float, float]


def _refine_transition(
    predicate: Callable[[float], bool],
    left: float,
    right: float,
    left_value: bool,
    tolerance_s: float,
) -> float:
    while right - left > tolerance_s:
        midpoint = (left + right) / 2.0
        if predicate(midpoint) == left_value:
            left = midpoint
        else:
            right = midpoint
    return (left + right) / 2.0


def find_true_intervals(
    predicate: Callable[[float], bool],
    start_s: float,
    end_s: float,
    *,
    scan_step_s: float,
    tolerance_s: float,
) -> list[Interval]:
    if end_s < start_s:
        raise ValueError("end_s must not precede start_s")
    if scan_step_s <= 0.0 or tolerance_s <= 0.0:
        raise ValueError("scan_step_s and tolerance_s must be positive")

    times = [float(start_s)]
    while times[-1] + scan_step_s < end_s:
        times.append(times[-1] + scan_step_s)
    if times[-1] != end_s:
        times.append(float(end_s))

    intervals: list[Interval] = []
    previous_time = times[0]
    previous_value = bool(predicate(previous_time))
    active_start = previous_time if previous_value else None

    for current_time in times[1:]:
        current_value = bool(predicate(current_time))
        if current_value != previous_value:
            boundary = _refine_transition(predicate, previous_time, current_time, previous_value, tolerance_s)
            if current_value:
                active_start = boundary
            elif active_start is not None:
                intervals.append((active_start, boundary))
                active_start = None
        previous_time = current_time
        previous_value = current_value

    if active_start is not None:
        intervals.append((active_start, float(end_s)))
    return intervals


def find_true_intervals_fixed_grid(
    predicate: Callable[[float], bool],
    start_s: float,
    end_s: float,
    *,
    scan_step_s: float,
) -> list[Interval]:
    """Approximate true intervals from fixed-width midpoint samples, without root refinement."""
    if end_s < start_s:
        raise ValueError("end_s must not precede start_s")
    if scan_step_s <= 0.0:
        raise ValueError("scan_step_s must be positive")
    intervals: list[Interval] = []
    left = float(start_s)
    while left < end_s:
        right = min(left + scan_step_s, float(end_s))
        if predicate((left + right) / 2.0):
            intervals.append((left, right))
        left = right
    return merge_intervals(intervals)


def merge_intervals(intervals: Iterable[Interval], *, tolerance_s: float = 0.0) -> list[Interval]:
    ordered = sorted((float(start), float(end)) for start, end in intervals if end >= start)
    if not ordered:
        return []
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        current_start, current_end = merged[-1]
        if start <= current_end + tolerance_s:
            merged[-1] = (current_start, max(current_end, end))
        else:
            merged.append((start, end))
    return merged


def interval_duration(intervals: Iterable[Interval]) -> float:
    return sum(max(0.0, end - start) for start, end in merge_intervals(intervals))
