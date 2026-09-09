import math
import sys
import pytest

from types import SimpleNamespace
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)


from gesture_recognizer import (
    detect_gesture,
    calculate_angle,
    calculate_distance,
    is_finger_extended,
    is_thumb_extended,
)


def landmark(x, y, z=0.0):
    """Create a simple MediaPipe-like landmark."""
    return SimpleNamespace(x=x, y=y, z=z)


def rotate_point(point, angle_degrees):
    """
    Rotate a 2D landmark around the origin.

    This is used to verify that geometric calculations remain
    valid when the hand changes orientation.
    """
    angle = math.radians(angle_degrees)

    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    x = (
        point.x * cos_angle
        - point.y * sin_angle
    )

    y = (
        point.x * sin_angle
        + point.y * cos_angle
    )

    return landmark(x, y, point.z)


def test_calculate_angle_straight_line():
    """A straight finger should produce an angle close to 180 degrees."""

    a = landmark(0.0, 0.0)
    b = landmark(1.0, 0.0)
    c = landmark(2.0, 0.0)

    angle = calculate_angle(a, b, c)

    assert angle == pytest.approx(180.0)


def test_calculate_angle_right_angle():
    """Three points forming a right angle should produce 90 degrees."""

    a = landmark(0.0, 0.0)
    b = landmark(1.0, 0.0)
    c = landmark(1.0, 1.0)

    angle = calculate_angle(a, b, c)

    assert angle == pytest.approx(90.0)


def test_calculate_angle_zero_length_vector():
    """Overlapping landmarks should not cause division-by-zero errors."""

    a = landmark(1.0, 1.0)
    b = landmark(1.0, 1.0)
    c = landmark(2.0, 2.0)

    angle = calculate_angle(a, b, c)

    assert angle == 0.0


def test_calculate_distance():
    """Distance calculation should follow Euclidean geometry."""

    a = landmark(0.0, 0.0)
    b = landmark(3.0, 4.0)

    distance = calculate_distance(a, b)

    assert distance == pytest.approx(5.0)


def test_calculate_distance_includes_z():
    """Distance calculation should account for the landmark Z coordinate."""

    a = landmark(0.0, 0.0, 0.0)
    b = landmark(0.0, 0.0, 3.0)

    distance = calculate_distance(a, b)

    assert distance == pytest.approx(3.0)


def test_extended_finger_is_detected():
    """
    A geometrically straight finger should be detected as extended.
    """

    mcp = landmark(0.0, 0.0)
    pip = landmark(0.0, 1.0)
    dip = landmark(0.0, 2.0)
    tip = landmark(0.0, 3.0)

    assert is_finger_extended(
        mcp,
        pip,
        dip,
        tip
    )


def test_folded_finger_is_not_detected_as_extended():
    """
    A bent finger should not be classified as extended.
    """

    mcp = landmark(0.0, 0.0)
    pip = landmark(0.0, 1.0)
    dip = landmark(0.8, 1.5)
    tip = landmark(1.3, 1.2)

    assert not is_finger_extended(
        mcp,
        pip,
        dip,
        tip
    )


def test_extended_finger_remains_extended_when_rotated():
    """
    Core ECSOC26 regression test:

    A straight finger should remain classified as extended
    after rotating all of its landmarks.
    """

    original_points = [
        landmark(0.0, 0.0),
        landmark(0.0, 1.0),
        landmark(0.0, 2.0),
        landmark(0.0, 3.0),
    ]

    for rotation in (0, 30, 45, 60, 90, 135):
        rotated_points = [
            rotate_point(point, rotation)
            for point in original_points
        ]

        assert is_finger_extended(
            rotated_points[0],
            rotated_points[1],
            rotated_points[2],
            rotated_points[3],
        )


def test_folded_finger_remains_folded_when_rotated():
    """
    A folded finger should remain classified as folded after
    changing its orientation.
    """

    original_points = [
        landmark(0.0, 0.0),
        landmark(0.0, 1.0),
        landmark(0.8, 1.5),
        landmark(1.3, 1.2),
    ]

    for rotation in (0, 30, 45, 60, 90, 135):
        rotated_points = [
            rotate_point(point, rotation)
            for point in original_points
        ]

        assert not is_finger_extended(
            rotated_points[0],
            rotated_points[1],
            rotated_points[2],
            rotated_points[3],
        )


def test_thumb_extension_uses_joint_geometry():
    """A straight thumb should be recognized as extended."""

    mcp = landmark(0.0, 0.0)
    ip = landmark(1.0, 0.0)
    tip = landmark(2.0, 0.0)

    assert is_thumb_extended(
        mcp,
        ip,
        tip
    )


def test_thumb_extension_is_rotation_robust():
    """
    Thumb extension should remain valid after rotating
    the complete thumb geometry.
    """

    original_points = [
        landmark(0.0, 0.0),
        landmark(1.0, 0.0),
        landmark(2.0, 0.0),
    ]

    for rotation in (0, 30, 45, 60, 90, 135):
        rotated_points = [
            rotate_point(point, rotation)
            for point in original_points
        ]

        assert is_thumb_extended(
            rotated_points[0],
            rotated_points[1],
            rotated_points[2],
        )



def create_hand_landmarks(
    thumb_extended=True,
    index_extended=True,
    middle_extended=True,
    ring_extended=True,
    pinky_extended=True,
    ok_gesture=False,
):
    """
    Create synthetic MediaPipe-style hand landmarks.

    The landmarks are arranged in a simple geometric hand model
    suitable for testing the gesture classifier.
    """

    landmarks = [
        landmark(0.0, 0.0) for _ in range(21)
    ]

    # ---------------------------------------------------------
    # Wrist
    # ---------------------------------------------------------

    landmarks[0] = landmark(0.0, 0.0)

    # ---------------------------------------------------------
    # Thumb
    # ---------------------------------------------------------

    if thumb_extended:
        landmarks[1] = landmark(-0.4, -0.1)   # THUMB_CMC
        landmarks[2] = landmark(-0.7, -0.2)   # THUMB_MCP
        landmarks[3] = landmark(-1.0, -0.3)   # THUMB_IP
        landmarks[4] = landmark(-1.3, -0.4)   # THUMB_TIP
    else:
        landmarks[1] = landmark(-0.3, 0.1)
        landmarks[2] = landmark(-0.5, 0.2)
        landmarks[3] = landmark(-0.4, 0.5)
        landmarks[4] = landmark(-0.2, 0.6)

    # ---------------------------------------------------------
    # Index finger
    # ---------------------------------------------------------

    if index_extended:
        landmarks[5] = landmark(-0.3, -0.5)   # INDEX_MCP
        landmarks[6] = landmark(-0.3, -1.0)   # INDEX_PIP
        landmarks[7] = landmark(-0.3, -1.5)   # INDEX_DIP
        landmarks[8] = landmark(-0.3, -2.0)   # INDEX_TIP
    else:
        landmarks[5] = landmark(-0.3, -0.5)
        landmarks[6] = landmark(-0.3, -0.8)
        landmarks[7] = landmark(0.0, -0.9)
        landmarks[8] = landmark(0.3, -0.7)

    # ---------------------------------------------------------
    # Middle finger
    # ---------------------------------------------------------

    if middle_extended:
        landmarks[9] = landmark(0.0, -0.5)     # MIDDLE_MCP
        landmarks[10] = landmark(0.0, -1.1)    # MIDDLE_PIP
        landmarks[11] = landmark(0.0, -1.7)    # MIDDLE_DIP
        landmarks[12] = landmark(0.0, -2.3)    # MIDDLE_TIP
    else:
        landmarks[9] = landmark(0.0, -0.5)
        landmarks[10] = landmark(0.0, -0.8)
        landmarks[11] = landmark(0.3, -0.9)
        landmarks[12] = landmark(0.5, -0.7)

    # ---------------------------------------------------------
    # Ring finger
    # ---------------------------------------------------------

    if ring_extended:
        landmarks[13] = landmark(0.3, -0.5)    # RING_MCP
        landmarks[14] = landmark(0.3, -1.0)    # RING_PIP
        landmarks[15] = landmark(0.3, -1.5)    # RING_DIP
        landmarks[16] = landmark(0.3, -2.0)    # RING_TIP
    else:
        landmarks[13] = landmark(0.3, -0.5)
        landmarks[14] = landmark(0.3, -0.8)
        landmarks[15] = landmark(0.6, -0.9)
        landmarks[16] = landmark(0.8, -0.7)

    # ---------------------------------------------------------
    # Pinky
    # ---------------------------------------------------------

    if pinky_extended:
        landmarks[17] = landmark(0.6, -0.5)    # PINKY_MCP
        landmarks[18] = landmark(0.6, -0.9)    # PINKY_PIP
        landmarks[19] = landmark(0.6, -1.3)    # PINKY_DIP
        landmarks[20] = landmark(0.6, -1.7)    # PINKY_TIP
    else:
        landmarks[17] = landmark(0.6, -0.5)
        landmarks[18] = landmark(0.6, -0.8)
        landmarks[19] = landmark(0.9, -0.9)
        landmarks[20] = landmark(1.1, -0.7)

    return SimpleNamespace(landmark=landmarks)


def rotate_hand(hand_landmarks, angle_degrees):
    """Rotate all hand landmarks around the wrist."""

    wrist = hand_landmarks.landmark[0]

    rotated = []

    for point in hand_landmarks.landmark:
        translated = landmark(
            point.x - wrist.x,
            point.y - wrist.y,
            point.z
        )

        rotated_point = rotate_point(
            translated,
            angle_degrees
        )

        rotated.append(
            landmark(
                rotated_point.x + wrist.x,
                rotated_point.y + wrist.y,
                rotated_point.z
            )
        )

    return SimpleNamespace(landmark=rotated)


def test_fist_gesture():
    hand = create_hand_landmarks(
        thumb_extended=False,
        index_extended=False,
        middle_extended=False,
        ring_extended=False,
        pinky_extended=False,
    )

    assert detect_gesture(hand, "Right") == "fist"


def test_peace_gesture():
    hand = create_hand_landmarks(
        thumb_extended=False,
        index_extended=True,
        middle_extended=True,
        ring_extended=False,
        pinky_extended=False,
    )

    assert detect_gesture(hand, "Right") == "peace"


def test_open_palm_gesture():
    hand = create_hand_landmarks(
        thumb_extended=True,
        index_extended=True,
        middle_extended=True,
        ring_extended=True,
        pinky_extended=True,
    )

    assert detect_gesture(hand, "Right") == "open_palm"


def test_fist_remains_fist_when_rotated():
    hand = create_hand_landmarks(
        thumb_extended=False,
        index_extended=False,
        middle_extended=False,
        ring_extended=False,
        pinky_extended=False,
    )

    for rotation in (0, 30, 45, 60, 90):
        rotated_hand = rotate_hand(
            hand,
            rotation
        )

        assert detect_gesture(
            rotated_hand,
            "Right"
        ) == "fist"


def test_peace_remains_peace_when_rotated():
    hand = create_hand_landmarks(
        thumb_extended=False,
        index_extended=True,
        middle_extended=True,
        ring_extended=False,
        pinky_extended=False,
    )

    for rotation in (0, 30, 45, 60, 90):
        rotated_hand = rotate_hand(
            hand,
            rotation
        )

        assert detect_gesture(
            rotated_hand,
            "Right"
        ) == "peace"


def test_open_palm_remains_open_palm_when_rotated():
    hand = create_hand_landmarks(
        thumb_extended=True,
        index_extended=True,
        middle_extended=True,
        ring_extended=True,
        pinky_extended=True,
    )

    for rotation in (0, 30, 45, 60, 90):
        rotated_hand = rotate_hand(
            hand,
            rotation
        )

        assert detect_gesture(
            rotated_hand,
            "Right"
        ) == "open_palm"