# Disaster Relief Assignment System

## Overview
This system uses computer vision to detect relief camps and injured people from an image, then assigns each person to the most suitable camp based on urgency and distance.

## Tech Stack

### Core Technologies
- **Python 3.7+** - Main programming language
- **OpenCV (cv2)** - Computer vision library for image processing, object detection, and color segmentation
- **NumPy** - Numerical computing library for array operations and mathematical calculations
- **Math** - Standard Python library for distance calculations

### Computer Vision Techniques
- **HSV Color Space Segmentation** - Identifies land, ocean, camps, and casualties by color
- **Hough Circle Transform** - Detects circular camp structures
- **Contour Detection** - Identifies casualty shapes and positions
- **Gaussian Blur** - Reduces noise before circle detection
- **Shape Approximation** - Classifies casualties by geometric shape

### Key Algorithms
- **Priority-Based Greedy Assignment** - Assigns casualties to camps based on urgency and proximity
- **Euclidean Distance Calculation** - Measures spatial proximity between casualties and camps
- **Shape Classification** - Identifies age groups based on geometric shapes (triangles, rectangles, polygons)

## Installation

```bash
pip install opencv-python numpy
```

### Requirements
- Python 3.7 or higher
- OpenCV 4.5.0 or higher
- NumPy 1.19.0 or higher

## Usage

### Basic Usage
```bash
python disaster_relief_simple.py
```

The script will:
1. Load the image from `task_images/4.png`
2. Detect camps and casualties
3. Assign casualties to camps based on priority and distance
4. Save visualization results to the `output/` directory
5. Print a detailed report

### Configuration
All parameters can be adjusted in the `CONFIG` dictionary at the top of the script:

```python
CONFIG = {
    # HSV ranges for segmentation
    'ocean_lower': np.array([90, 50, 50]),
    'ocean_upper': np.array([140, 255, 255]),
    
    # Circle detection parameters
    'hough_param1': 100,
    'hough_param2': 30,
    'hough_minradius': 15,
    'hough_maxradius': 60,
    
    # Camp capacities
    'camp_capacity': {
        "blue": 4,
        "pink": 3,
        "grey": 2
    },
    # ... more parameters
}
```

### Input Image
Place your image at `task_images/4.png` or modify the path in the script:
```python
image = cv2.imread("your_image_path.png")
```

### Output Files
The script generates two output images in the `output/` directory:
- **segmented.png** - Shows land (green) and ocean (blue) segmentation
- **final_assignment.png** - Shows camps and their assigned casualties with colored lines

## How It Works

### Step 1: Image Segmentation
Segments the image into land and ocean regions using HSV color ranges for environmental context.

### Step 2: Camp Detection
Detects circular camps using Hough Circle Transform. Each camp is classified by color:
- **Blue camps**: Capacity 4 people
- **Pink camps**: Capacity 3 people
- **Grey camps**: Capacity 2 people

### Step 3: Casualty Detection
Detects casualties using color and shape analysis:

**Color indicates condition (severity):**
- **Red** = Severe (condition score: 3)
- **Yellow** = Mild (condition score: 2)
- **Green** = Safe (condition score: 1)

**Shape indicates age group:**
- **Triangle** = Elderly (age score: 2)
- **Rectangle** = Adult (age score: 1)
- **Other shapes** = Child (age score: 3)

### Step 4: Priority Assignment
Each casualty receives a priority score:
```
Priority = Age Score × Condition Score
```

Examples:
- Elderly + Severe = 2 × 3 = **6** (highest priority)
- Child + Mild = 3 × 2 = **6** (highest priority)
- Adult + Safe = 1 × 1 = **1** (lowest priority)

### Step 5: Camp Assignment Algorithm
Uses a greedy algorithm to assign casualties to camps:

1. Sort all casualties by priority (highest first)
2. For each casualty:
   - Calculate assignment score for each available camp:
     ```
     Score = Priority / (Distance + 1)
     ```
   - Assign to the camp with highest score
3. Continue until all casualties are assigned or camps are full

This balances urgency with proximity - high priority casualties get preference, but distance is also considered.

### Step 6: Generate Report
Prints a detailed report showing:
- Number of camps detected
- Number of casualties found
- Assignment details per camp
- Total priority scores
- Rescue ratio (effectiveness metric)

## Output Report Example

```
Detected 3 camps
Detected 12 casualties

Camp Details:
Camp 0: blue at (150, 200), assigned: 4/4
Camp 1: pink at (300, 250), assigned: 3/3
Camp 2: grey at (450, 180), assigned: 2/2

Camp Priority Totals: [18, 12, 8]
Rescue Ratio: 4.22

Output saved to output/ directory
```

## Understanding the Results

### Rescue Ratio
The rescue ratio is calculated as:
```
Rescue Ratio = Total Priority / Total People Assigned
```

Higher rescue ratio means more high-priority casualties were successfully assigned.

### Camp Totals
Shows the sum of priority scores for all casualties assigned to each camp. Higher numbers indicate camps handling more urgent cases.

## Customization

### Adding New Camp Colors
Add to the camp detection function:
```python
def detect_camp_color(x, y):
    # Add your color detection logic
    if your_condition:
        return "your_color"
```

Update capacity:
```python
CONFIG['camp_capacity'] = {
    "blue": 4,
    "pink": 3,
    "grey": 2,
    "your_color": 5  # Add new camp type
}
```

### Adjusting Detection Sensitivity
Modify HSV ranges in CONFIG:
```python
CONFIG = {
    'severe_lower1': np.array([0, 70, 50]),   # Adjust these values
    'severe_upper1': np.array([10, 255, 255]),
    # ... adjust other ranges
}
```

### Changing Circle Detection
Tune Hough Circle parameters:
```python
CONFIG = {
    'hough_param1': 100,      # Edge detection threshold
    'hough_param2': 30,       # Circle detection threshold (lower = more circles)
    'hough_minradius': 15,    # Minimum circle size
    'hough_maxradius': 60,    # Maximum circle size
}
```

## Troubleshooting

### No camps detected
- Adjust `hough_param2` (lower value detects more circles)
- Check if camps are actually circular in the image
- Verify image path is correct

### No casualties detected
- Check HSV color ranges match your image
- Adjust `min_contour_area` if shapes are too small
- Verify casualty colors match expected red/yellow/green

### Poor assignments
- Adjust camp capacities in CONFIG
- Modify priority scoring in `casualty_priority()` function
- Check if distance calculation needs adjustment

## Design Philosophy

The system balances two competing factors:
1. **Urgency** - High priority casualties should be rescued first
2. **Efficiency** - Nearby camps are preferred to reduce response time

The scoring formula `Priority / (Distance + 1)` achieves this balance by:
- Giving strong preference to high-priority casualties
- Slightly favoring closer camps when priorities are equal
- Avoiding division by zero with the "+1"

## Future Enhancements

Potential improvements:
- Batch processing for multiple images
- Real-time video stream analysis
- Optimal assignment using Hungarian algorithm
- Geospatial coordinate support
- Web-based interface
- Machine learning for better detection
- Adjustable priority weights
