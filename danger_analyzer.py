import cv2

class DangerAnalyzer:

    def __init__(self):
        pass

    def analyze(self, fire_count, smoke_count, people_count):

        total_detections = fire_count + smoke_count

       
        # Danger Level
        

        if total_detections == 0:
            level = "SAFE"
            color = (0,255,0)

        elif total_detections == 1:

            if people_count == 0:
                level = "LOW RISK"
                color = (0,255,255)
            else:
                level = "MEDIUM RISK"
                color = (0,165,255)

        else:

            if people_count == 0:
                level = "HIGH RISK"
                color = (0,0,255)
            elif people_count <= 3:
                level = "VERY HIGH RISK"
                color = (0,0,255)
            else:
                level = "CRITICAL"
                color = (0,0,180)

        return level, color

    def draw_panel(self,
                   image,
                   fire_count,
                   smoke_count,
                   people_count,
                   danger_level,
                   color):

        h, w = image.shape[:2]

        cv2.rectangle(image,
                      (10,10),
                      (390,190),
                      (30,30,30),
                      -1)

        cv2.rectangle(image,
                      (10,10),
                      (390,190),
                      color,
                      2)

        cv2.putText(image,
                    "SMART BUILDING MONITOR",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255,255,255),
                    2)

        cv2.putText(image,
                    f"Fire : {fire_count}",
                    (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,255),
                    2)

        cv2.putText(image,
                    f"Smoke : {smoke_count}",
                    (20,110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,0),
                    2)

        cv2.putText(image,
                    f"People : {people_count}",
                    (20,140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2)

        cv2.putText(image,
                    f"STATUS : {danger_level}",
                    (20,175),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    color,
                    2)

        return image