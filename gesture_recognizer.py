import math
import mediapipe as mp

mp_hands = mp.solutions.hands

# Existing project thresholds - kept unchanged.
OK_THRESHOLD = 0.04

# New thresholds required for orientation-independent
# finger detection using joint angles.
FINGER_ANGLE_THRESHOLD = 155.0
THUMB_ANGLE_THRESHOLD = 150.0
ANGLE_EPSILON = 1e-8


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC in degrees.

    The angle is calculated using vectors BA and BC.

    A ---- B ---- C  -> angle close to 180 degrees

    A
     \
      B
       \
        C            -> smaller angle

    Using the angle between landmarks instead of their absolute
    image coordinates makes finger detection less dependent on
    the orientation of the hand.

    Args:
        a: First MediaPipe landmark.
        b: Middle MediaPipe landmark (vertex of the angle).
        c: Third MediaPipe landmark.

    Returns:
        float: Angle in degrees in the range [0, 180].
    """

    # Vector from B to A.
    ba_x = a.x - b.x
    ba_y = a.y - b.y
    ba_z = getattr(a, "z", 0.0) - getattr(b, "z", 0.0)

    # Vector from B to C.
    bc_x = c.x - b.x
    bc_y = c.y - b.y
    bc_z = getattr(c, "z", 0.0) - getattr(b, "z", 0.0)

    # Magnitudes of the two vectors.
    ba_length = math.sqrt(
        ba_x ** 2 +
        ba_y ** 2 +
        ba_z ** 2
    )

    bc_length = math.sqrt(
        bc_x ** 2 +
        bc_y ** 2 +
        bc_z ** 2
    )

    # Prevent division by zero if landmarks overlap.
    if ba_length < ANGLE_EPSILON or bc_length < ANGLE_EPSILON:
        return 0.0

    # Dot product of BA and BC.
    dot_product = (
        ba_x * bc_x +
        ba_y * bc_y +
        ba_z * bc_z
    )

    # Calculate cosine of the angle.
    cosine_angle = dot_product / (ba_length * bc_length)

    # Protect against floating-point values slightly outside
    # the valid range of acos().
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    return math.degrees(math.acos(cosine_angle))


def calculate_distance(a, b):
    """
    Calculate Euclidean distance between two MediaPipe landmarks.

    Uses x, y and z coordinates when available.

    Args:
        a: First MediaPipe landmark.
        b: Second MediaPipe landmark.

    Returns:
        float: Euclidean distance between the landmarks.
    """

    dx = a.x - b.x
    dy = a.y - b.y
    dz = getattr(a, "z", 0.0) - getattr(b, "z", 0.0)

    return math.sqrt(
        dx ** 2 +
        dy ** 2 +
        dz ** 2
    )


def is_finger_extended(mcp, pip, dip, tip):
    """
    Determine whether a finger is extended using joint geometry.

    The previous implementation relied on the Y-axis relationship
    between the fingertip and PIP joint. That approach assumes the
    hand is approximately upright.

    This implementation uses the angles at the PIP and DIP joints.
    A relatively straight finger produces angles close to 180
    degrees regardless of whether the hand is vertical, tilted,
    or horizontally oriented.

    Args:
        mcp: Metacarpophalangeal joint landmark.
        pip: Proximal interphalangeal joint landmark.
        dip: Distal interphalangeal joint landmark.
        tip: Fingertip landmark.

    Returns:
        bool: True if the finger is considered extended.
    """

    pip_angle = calculate_angle(
        mcp,
        pip,
        dip
    )

    dip_angle = calculate_angle(
        pip,
        dip,
        tip
    )

    return (
        pip_angle >= FINGER_ANGLE_THRESHOLD
        and dip_angle >= FINGER_ANGLE_THRESHOLD
    )


def is_thumb_extended(mcp, ip, tip):
    """
    Determine whether the thumb is extended using joint geometry.

    The thumb is evaluated using the angle formed by its MCP,
    IP and TIP landmarks rather than relying on the thumb's
    absolute X/Y position.

    Args:
        mcp: Thumb MCP landmark.
        ip: Thumb IP landmark.
        tip: Thumb tip landmark.

    Returns:
        bool: True if the thumb is considered extended.
    """

    thumb_angle = calculate_angle(
        mcp,
        ip,
        tip
    )

    return thumb_angle >= THUMB_ANGLE_THRESHOLD


def detect_gesture(hand_landmarks, handedness):
    """
    Detect hand gesture from MediaPipe landmarks.

    Uses landmark geometry and joint angles to reduce dependence
    on the absolute orientation of the hand in the camera frame.

    The existing gesture set is preserved:

        "ok"
        "peace"
        "fist"
        "open_palm"
        None

    Priority order:

        ok > peace > fist > open_palm

    Args:
        hand_landmarks: MediaPipe hand landmark result.
        handedness: Handedness returned by MediaPipe. The argument
                    is retained for compatibility with the existing
                    application interface.

    Returns:
        str or None: Detected gesture.
    """

    landmarks = hand_landmarks.landmark

    # ---------------------------------------------------------
    # Thumb landmarks
    # ---------------------------------------------------------

    thumb_tip = landmarks[
        mp_hands.HandLandmark.THUMB_TIP
    ]

    thumb_ip = landmarks[
        mp_hands.HandLandmark.THUMB_IP
    ]

    thumb_mcp = landmarks[
        mp_hands.HandLandmark.THUMB_MCP
    ]

    # ---------------------------------------------------------
    # Index finger landmarks
    # ---------------------------------------------------------

    index_tip = landmarks[
        mp_hands.HandLandmark.INDEX_FINGER_TIP
    ]

    index_dip = landmarks[
        mp_hands.HandLandmark.INDEX_FINGER_DIP
    ]

    index_pip = landmarks[
        mp_hands.HandLandmark.INDEX_FINGER_PIP
    ]

    index_mcp = landmarks[
        mp_hands.HandLandmark.INDEX_FINGER_MCP
    ]

    # ---------------------------------------------------------
    # Middle finger landmarks
    # ---------------------------------------------------------

    middle_tip = landmarks[
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP
    ]

    middle_dip = landmarks[
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP
    ]

    middle_pip = landmarks[
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP
    ]

    middle_mcp = landmarks[
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP
    ]

    # ---------------------------------------------------------
    # Ring finger landmarks
    # ---------------------------------------------------------

    ring_tip = landmarks[
        mp_hands.HandLandmark.RING_FINGER_TIP
    ]

    ring_dip = landmarks[
        mp_hands.HandLandmark.RING_FINGER_DIP
    ]

    ring_pip = landmarks[
        mp_hands.HandLandmark.RING_FINGER_PIP
    ]

    ring_mcp = landmarks[
        mp_hands.HandLandmark.RING_FINGER_MCP
    ]

    # ---------------------------------------------------------
    # Pinky landmarks
    # ---------------------------------------------------------

    pinky_tip = landmarks[
        mp_hands.HandLandmark.PINKY_TIP
    ]

    pinky_dip = landmarks[
        mp_hands.HandLandmark.PINKY_DIP
    ]

    pinky_pip = landmarks[
        mp_hands.HandLandmark.PINKY_PIP
    ]

    pinky_mcp = landmarks[
        mp_hands.HandLandmark.PINKY_MCP
    ]

    # ---------------------------------------------------------
    # Finger states
    # ---------------------------------------------------------

    index_extended = is_finger_extended(
        index_mcp,
        index_pip,
        index_dip,
        index_tip
    )

    middle_extended = is_finger_extended(
        middle_mcp,
        middle_pip,
        middle_dip,
        middle_tip
    )

    ring_extended = is_finger_extended(
        ring_mcp,
        ring_pip,
        ring_dip,
        ring_tip
    )

    pinky_extended = is_finger_extended(
        pinky_mcp,
        pinky_pip,
        pinky_dip,
        pinky_tip
    )

    # A finger that does not satisfy the extension geometry is
    # considered folded.
    index_folded = not index_extended
    middle_folded = not middle_extended
    ring_folded = not ring_extended
    pinky_folded = not pinky_extended

    # ---------------------------------------------------------
    # Thumb state
    # ---------------------------------------------------------

    thumb_extended = is_thumb_extended(
        thumb_mcp,
        thumb_ip,
        thumb_tip
    )

    # ---------------------------------------------------------
    # OK gesture
    # ---------------------------------------------------------
    #
    # Keep the original project's OK_THRESHOLD unchanged.
    #
    # The thumb tip and index tip must be sufficiently close,
    # while the remaining three fingers are extended.
    # ---------------------------------------------------------

    thumb_index_dist = (
        (thumb_tip.x - index_tip.x) ** 2
        + (thumb_tip.y - index_tip.y) ** 2
    ) ** 0.5

    if (
        thumb_index_dist < OK_THRESHOLD
        and middle_extended
        and ring_extended
        and pinky_extended
    ):
        return "ok"

    # ---------------------------------------------------------
    # Peace gesture
    # ---------------------------------------------------------
    #
    # Index + middle extended
    # Ring + pinky folded
    #
    # No absolute thumb direction is required here, which avoids
    # the previous orientation-dependent thumb check.
    # ---------------------------------------------------------

    if (
        index_extended
        and middle_extended
        and ring_folded
        and pinky_folded
    ):
        return "peace"

    # ---------------------------------------------------------
    # Open palm
    # ---------------------------------------------------------

    if (
        thumb_extended
        and index_extended
        and middle_extended
        and ring_extended
        and pinky_extended
    ):
        return "open_palm"

    # ---------------------------------------------------------
    # Fist
    # ---------------------------------------------------------

    if (
        index_folded
        and middle_folded
        and ring_folded
        and pinky_folded
        and not thumb_extended
    ):
        return "fist"

    return None
