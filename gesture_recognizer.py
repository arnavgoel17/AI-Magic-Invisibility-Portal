import mediapipe as mp

mp_hands = mp.solutions.hands

EPSILON = 0.02
OK_THRESHOLD = 0.04


def is_extended(tip, pip):
    """Check if finger is extended (tip clearly above pip)."""
    return tip.y < pip.y - EPSILON


def is_folded(tip, pip):
    """Check if finger is folded (tip clearly below pip)."""
    return tip.y > pip.y + EPSILON


def detect_gesture(hand_landmarks, handedness):
    """
    Detect hand gesture from MediaPipe landmarks.
    Uses handedness to disambiguate thumb direction.
    Returns one of: "ok", "peace", "fist", "open_palm", or None

    Priority order: ok > peace > fist > open_palm
    """
    landmarks = hand_landmarks.landmark

    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]

    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP]

    is_right_hand = handedness == "Right"

    # Thumb direction: used to prevent peace/fist conflict with thumb-up
    thumb_upward = thumb_tip.y < thumb_ip.y
    if is_right_hand:
        thumb_up = thumb_upward and thumb_tip.x < landmarks[mp_hands.HandLandmark.THUMB_MCP].x
    else:
        thumb_up = thumb_upward and thumb_tip.x > landmarks[mp_hands.HandLandmark.THUMB_MCP].x

    # Finger states
    middle_extended = is_extended(middle_tip, middle_pip)
    ring_extended = is_extended(ring_tip, ring_pip)
    pinky_extended = is_extended(pinky_tip, pinky_pip)

    index_extended = is_extended(index_tip, index_pip)
    middle_folded = is_folded(middle_tip, middle_pip)
    ring_folded = is_folded(ring_tip, ring_pip)
    pinky_folded = is_folded(pinky_tip, pinky_pip)

    # OK Sign: thumb tip and index tip close together, other fingers extended
    thumb_index_dist = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    if thumb_index_dist < OK_THRESHOLD and middle_extended and ring_extended and pinky_extended:
        return "ok"

    # Peace Sign: index and middle extended, ring and pinky folded
    if index_extended and middle_extended and ring_folded and pinky_folded and not thumb_up:
        return "peace"

    # Open Palm: all fingers extended
    if thumb_up and index_extended and middle_extended and ring_extended and pinky_extended:
        return "open_palm"

    # Fist: all non-thumb fingers folded
    if not index_extended and not middle_extended and not ring_extended and not pinky_extended and not thumb_up:
        return "fist"

    return None