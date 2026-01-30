
# Disaster Relief Assignment System – Refactored

## Overview
This project is a cleaner, more reliable version of a disaster relief assignment system that uses computer vision to detect relief camps and injured people from an image, then assigns each person to the most suitable camp based on urgency and distance.

The refactored version focuses on clarity, stability, and flexibility. It is easier to understand, easier to modify, and much more reliable than the original version.

## Tech Stack

### Core Technologies
- **Python 3.7+** - Main programming language
- **OpenCV (cv2)** - Computer vision library for image processing, object detection, and color segmentation
- **NumPy** - Numerical computing library for array operations and mathematical calculations
- **Math** - Standard Python library for distance calculations

### Computer Vision Techniques Used
- **HSV Color Space Segmentation** - For identifying land, ocean, camps, and casualties by color
- **Hough Circle Transform** - For detecting circular camp structures
- **Contour Detection** - For identifying casualty shapes and positions
- **Gaussian Blur** - For noise reduction before circle detection
- **Morphological Operations** - For shape approximation and classification

### Key Algorithms
- **Priority-Based Greedy Assignment** - Assigns casualties to camps based on urgency and proximity
- **Euclidean Distance Calculation** - Measures spatial proximity between casualties and camps
- **Shape Classification** - Identifies age groups based on geometric shape (triangles, rectangles, polygons)

### No External Dependencies Beyond Standard Stack
The project intentionally uses only widely-available, stable libraries:
- ✅ No machine learning frameworks
- ✅ No web frameworks
- ✅ No database systems
- ✅ Minimal dependencies for maximum portability

This keeps the system lightweight, fast, and easy to deploy in resource-constrained disaster relief scenarios.

## What Changed and Why It Matters

### Centralized Configuration
Earlier, important values like detection ranges and thresholds were scattered throughout the project, making it difficult to adjust or debug. Now, everything is organized in one place. This makes tuning the system faster and reduces mistakes.

### Improved Color Detection
The system now uses a consistent method for recognizing colors, which makes it more accurate under different lighting conditions. This improves how camps and casualties are identified and reduces errors.

### No More Duplicate Logic
Previously, some calculations and detection methods were repeated in multiple places. Now, each task has one clear implementation. This makes the system easier to maintain and less prone to bugs.

### Better Error Handling
Instead of abruptly stopping when something goes wrong, the system now handles issues gracefully. If camps or casualties cannot be detected, the program reports the issue clearly and continues safely where possible.

### Structured, Object-Oriented Design
The project now uses clearly defined components for camps, casualties, and the overall assignment process. This improves readability and makes the system easier to extend in the future.

### Modular Architecture
Each part of the workflow has its own responsibility. Image loading, segmentation, detection, assignment, reporting, and saving results are all handled separately. This makes debugging simpler and future upgrades smoother.

### Professional Logging
Instead of random print statements, the system now provides structured progress updates. You can clearly see what is happening at each step and identify problems quickly.

### Input Validation
The system now checks for invalid data before processing. This prevents crashes and ensures the output remains reliable even when inputs are imperfect.

### Removed Unused Code
Old or unnecessary parts that added confusion have been removed. The result is a cleaner and more efficient system.

### Flexible Output Management
Output files are now organized in a consistent way, making results easier to access and manage across different environments.

### Detailed Reporting
After processing, the system provides a clear summary showing:
* Number of camps detected
* Number of casualties found
* How many were successfully assigned
* Camp capacity usage
* Overall rescue effectiveness

This makes the results easy to understand for both technical and non-technical users.

## Design Philosophy
The assignment process balances urgency and distance. People with higher priority are matched with the nearest available camp, ensuring the most effective use of limited resources.

## Extensibility
The system is designed so that new camp types, casualty conditions, or scoring rules can be added easily. This allows it to adapt to different disaster scenarios without major restructuring.

## Testing and Reliability
Because the system is modular, individual parts can be tested independently. This improves confidence in results and makes future development safer.

## Performance
The current method works efficiently for typical disaster scenarios. For very large datasets, future versions could include more advanced optimization techniques to further improve speed and accuracy.

## Future Improvements
Potential upgrades include:
* Processing multiple images at once
* Real-time video analysis
* Learning from past data to improve assignments
* Web-based interface for easier access
* Integration with mapping systems
* Adjustable priority weighting

## Requirements

### Installation
```bash
pip install opencv-python numpy
```

### Minimum Requirements
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

### Output Files
- `output/segmented.png` - Land and ocean segmentation visualization
- `output/final_assignment.png` - Final assignment visualization showing camps and assigned casualties

## How It Works

### Step 1: Image Segmentation
The system segments the image into land and ocean regions using HSV color ranges. This provides environmental context for the disaster scenario.

### Step 2: Camp Detection
Circular camps are detected using the Hough Circle Transform. Each camp is then classified by color (blue, pink, or grey) which determines its capacity:
- Blue camps: 4 people
- Pink camps: 3 people
- Grey camps: 2 people

### Step 3: Casualty Detection
Casualties are detected using color-based segmentation and shape analysis:
- **Color indicates condition:**
  - Red = Severe (priority: 3)
  - Yellow = Mild (priority: 2)
  - Green = Safe (priority: 1)
- **Shape indicates age:**
  - Triangle = Elderly (priority: 2)
  - Rectangle = Adult (priority: 1)
  - Other shapes = Child (priority: 3)

### Step 4: Assignment Algorithm
Each casualty is assigned to a camp using a priority-based greedy algorithm:
1. Calculate priority = age_score × condition_score
2. Sort casualties by priority (highest first)
3. For each casualty, find the best available camp based on:
   - Assignment score = priority / (distance + 1)
4. Assign to the camp with highest score

### Step 5: Reporting
The system generates a detailed report showing:
- Camp locations and capacities
- Number of assigned casualties per camp
- Total priority scores
- Rescue ratio (effectiveness metric)
