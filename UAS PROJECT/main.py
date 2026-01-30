import cv2
import numpy as np
import math

try:
    # Step-1 Image loading
    image = cv2.imread("task_images/1.png")

    if image is None:
        raise Exception("Image could not be loaded. Check file path or format.")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Step 2: Land Ocean Detection
    lower_blue = np.array([90, 50, 50])   # Ocean color range
    upper_blue = np.array([140, 255, 255])

    lower_green = np.array([35, 40, 40])  # Land color range
    upper_green = np.array([85, 255, 255])

    mask_ocean = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_land = cv2.inRange(hsv, lower_green, upper_green)

    segmented = image.copy()
    segmented[mask_ocean > 0] = [255, 0, 0]
    segmented[mask_land > 0] = [0, 255, 0]

    #Step3 Camp Detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 1.5)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,          # resolution ratio
        minDist=50,    # minimum distance between circles
        param1=100,    # Canny edge threshold
        param2=30,     # center detection threshold
        minRadius=15,  # minimum expected camp size
        maxRadius=60   # maximum expected camp size
    )

    if circles is None:
        raise Exception("No rescue camps detected.")

    circles = circles[0]

    camp_capacity = {
        "blue": 4,
        "pink": 3,
        "grey": 2
    }


    def detect_color(x, y):
        try:
            hsv_pixel = hsv[int(y), int(x)]
            h, s, v = hsv_pixel

            if s < 40:
                return "grey"
            elif 90 <= h <= 140:
                return "blue"
            else:
                return "pink"
        except:
            return "unknown"

    camps = []

    for (x, y, r) in circles:
        color = detect_color(x, y)
        camps.append({
            "color": color,
            "capacity": camp_capacity.get(color, 1),
            "position": (int(x), int(y)),
            "assigned": []
        })

    if len(camps) == 0:
        raise Exception("No camps available for assignment.")

    #Step 4 Casuality Detection 
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + \
               cv2.inRange(hsv, lower_red2, upper_red2)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    def detect_casualties(mask, condition, score):
        casualties = []

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area < 100:  # ignore noise
                continue

            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            epsilon = 0.04 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            corners = len(approx)

            if corners == 3:
                age = "elderly"
                age_score = 2
            elif corners == 4:
                age = "adult"
                age_score = 1
            else:
                age = "child"
                age_score = 3

            casualties.append({
                "position": (cx, cy),
                "age_score": age_score,
                "condition_score": score
            })

        return casualties

    casualties = []
    casualties += detect_casualties(mask_red, "severe", 3)
    casualties += detect_casualties(mask_yellow, "mild", 2)
    casualties += detect_casualties(mask_green, "safe", 1)

    if len(casualties) == 0:
        raise Exception("No casualties detected.")

    #STEP 5: Algorithm Used
    def casualty_priority(c):
        return c["age_score"] * c["condition_score"]

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def final_score(casualty, camp):
        return casualty_priority(casualty) / (distance(casualty["position"], camp["position"]) + 1)

    casualties.sort(key=lambda c: casualty_priority(c), reverse=True)

    for casualty in casualties:
        best_camp = None
        best_score = -1

        for camp in camps:
            if len(camp["assigned"]) >= camp["capacity"]:
                continue

            score = final_score(casualty, camp)

            if score > best_score:
                best_score = score
                best_camp = camp

        if best_camp:
            best_camp["assigned"].append(casualty)

    # Step 6: Output 
    final_output = image.copy()

    color_map = {
        "blue": (255, 0, 0),
        "pink": (255, 0, 255),
        "grey": (128, 128, 128)
    }

    for camp in camps:
        cx, cy = camp["position"]
        camp_color = color_map[camp["color"]]

        cv2.circle(final_output, (cx, cy), 20, camp_color, 2)

        for c in camp["assigned"]:
            px, py = c["position"]
            cv2.line(final_output, (px, py), (cx, cy), camp_color, 2)

    saved = cv2.imwrite("output/final_assignment_1.png", final_output)

    if not saved:
        raise Exception("Failed to save output image.")

    print("Assignment Completed Successfully.")

except Exception as e:
    print("\nCode Failed")
    print("Error:", e)
