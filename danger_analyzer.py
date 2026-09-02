import cv2
from datetime import datetime


class DangerAnalyzer:

    def __init__(self):
        pass

    # =========================================================
    # ANALYZE DANGER
    # =========================================================

    def analyze(self, fire_count, smoke_count, people_count):

        total_detections = fire_count + smoke_count

        # No fire or smoke
        if total_detections == 0:

            level = "SAFE"
            color = (0, 255, 0)

        # One detection
        elif total_detections == 1:

            if people_count == 0:
                level = "LOW RISK"
                color = (0, 255, 255)

            else:
                level = "MEDIUM RISK"
                color = (0, 165, 255)

        # Multiple detections
        else:

            if people_count == 0:

                level = "HIGH RISK"
                color = (0, 0, 255)

            elif people_count <= 3:

                level = "VERY HIGH RISK"
                color = (0, 0, 255)

            else:

                level = "CRITICAL"
                color = (0, 0, 180)

        return level, color


    # =========================================================
    # DRAW MACMS STYLE UI
    # =========================================================

    def draw_panel(
        self,
        image,
        fire_count,
        smoke_count,
        people_count,
        danger_level,
        color
    ):

        # -----------------------------------------------------
        # Get image size
        # -----------------------------------------------------

        h, w = image.shape[:2]

        # -----------------------------------------------------
        # Height of dashboard
        # -----------------------------------------------------

        header_height = 115

        # -----------------------------------------------------
        # Create dark dashboard area above image
        # -----------------------------------------------------

        dashboard = 30 * (
            __import__("numpy").ones(
                (header_height, w, 3),
                dtype="uint8"
            )
        )

        dashboard = dashboard.astype("uint8")

        # -----------------------------------------------------
        # Create final image
        # -----------------------------------------------------

        final_image = __import__("numpy").vstack(
            [dashboard, image]
        )

        # =====================================================
        # TOP HEADER
        # =====================================================

        # Main title
        cv2.putText(
            final_image,
            "MACMS",
            (25, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Room
        cv2.putText(
            final_image,
            "ROOM 1",
            (230, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Vertical separator
        cv2.line(
            final_image,
            (345, 15),
            (345, 55),
            (100, 100, 100),
            1
        )

        # REC indicator
        cv2.circle(
            final_image,
            (395, 32),
            7,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            final_image,
            "REC",
            (412, 39),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # -----------------------------------------------------
        # Current time
        # -----------------------------------------------------

        now = datetime.now()

        time_text = now.strftime("%H:%M:%S")
        date_text = now.strftime("%d/%m/%Y")

        cv2.putText(
            final_image,
            time_text,
            (w // 2 - 50, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Date
        cv2.putText(
            final_image,
            date_text,
            (w - 130, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (220, 220, 220),
            1,
            cv2.LINE_AA
        )

        # =====================================================
        # SEPARATOR
        # =====================================================

        cv2.line(
            final_image,
            (0, 60),
            (w, 60),
            (90, 90, 90),
            1
        )

        # =====================================================
        # SECOND STATUS BAR
        # =====================================================

        status_y = 93

        # -----------------------------------------------------
        # FIRE
        # -----------------------------------------------------

        cv2.putText(
            final_image,
            f"FIRE: {fire_count}",
            (25, status_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (0, 0, 255),
            2,
            cv2.LINE_AA
        )

        # Separator
        cv2.line(
            final_image,
            (175, 68),
            (175, 105),
            (90, 90, 90),
            1
        )

        # -----------------------------------------------------
        # SMOKE
        # -----------------------------------------------------

        cv2.putText(
            final_image,
            f"SMOKE: {smoke_count}",
            (195, status_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Separator
        cv2.line(
            final_image,
            (365, 68),
            (365, 105),
            (90, 90, 90),
            1
        )

        # -----------------------------------------------------
        # PEOPLE
        # -----------------------------------------------------

        cv2.putText(
            final_image,
            f"PEOPLE: {people_count}",
            (385, status_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        # Separator
        cv2.line(
            final_image,
            (570, 68),
            (570, 105),
            (90, 90, 90),
            1
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        cv2.putText(
            final_image,
            "STATUS:",
            (590, status_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Status value
        cv2.putText(
            final_image,
            danger_level,
            (690, status_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            color,
            2,
            cv2.LINE_AA
        )

        # =====================================================
        # RETURN FINAL IMAGE
        # =====================================================

        return final_image