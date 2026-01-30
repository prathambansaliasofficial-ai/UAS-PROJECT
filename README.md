# Disaster Relief Assignment System - Refactored

## Overview
This is a refactored version of the disaster relief camp assignment system that uses computer vision to detect camps and casualties, then optimally assigns people to camps based on priority and proximity.

## Major Improvements

### 1. ✅ Configuration Management
**Before:** Magic numbers scattered throughout code
```python
lower_blue = np.array([90, 50, 50])
param1=100, param2=30, minRadius=15
```

**After:** Centralized Config class
```python
class Config:
    OCEAN_HSV_RANGE = {
        'lower': np.array([90, 50, 50]),
        'upper': np.array([140, 255, 255])
    }
    CIRCLE_DETECTION = {
        'param1': 100,
        'param2': 30,
        ...
    }
```
- All parameters in one place
- Easy to tune without touching code
- Self-documenting configuration

### 2. ✅ Unified HSV-Based Color Detection
**Before:** Mixed BGR and HSV detection methods
```python
b, g, r = image[y, x]
if b > 150 and g < 100:
    camp_color = "blue"
```

**After:** Pure HSV detection with proper ranges
```python
def detect_camp_color_hsv(self, x: int, y: int) -> str:
    h, s, v = self.hsv_image[y, x]
    
    if s < self.config.CAMP_COLORS['grey']['saturation_max']:
        return 'grey'
    
    blue_range = self.config.CAMP_COLORS['blue']['hue_range']
    if blue_range[0] <= h <= blue_range[1]:
        return 'blue'
```
- Consistent color detection approach
- More robust to lighting variations
- Properly configured color ranges

### 3. ✅ Removed Code Duplication
**Before:** `casualty_priority()` defined twice, redundant color detection

**After:** 
- Single `Casualty.priority()` method
- Single `detect_camp_color_hsv()` method
- DRY principle applied throughout

### 4. ✅ Proper Error Handling
**Before:** 
```python
if circles is None:
    print("No camps detected")
    exit()  # Kills entire program
```

**After:**
```python
if circles is None:
    logger.error("No camps detected in the image")
    return False  # Graceful failure

try:
    # Pipeline execution
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    return False
```
- No abrupt `exit()` calls
- Proper exception handling
- Graceful degradation

### 5. ✅ Object-Oriented Design with Dataclasses
**Before:** Dictionaries with loose typing
```python
camps.append({
    "color": color,
    "capacity": camp_capacity[color],
    "position": (x, y),
    "assigned": []
})
```

**After:** Type-safe dataclasses
```python
@dataclass
class Camp:
    color: str
    capacity: int
    position: Tuple[int, int]
    assigned: List[Casualty] = field(default_factory=list)
    
    def is_full(self) -> bool:
        return len(self.assigned) >= self.capacity
```
- Type hints for clarity
- Methods attached to data
- Better IDE support

### 6. ✅ Modular Architecture
**Before:** Single monolithic script with everything in one place

**After:** Clean separation of concerns
```
DisasterReliefAssignment (Main Class)
├── load_image()
├── segment_land_ocean()
├── detect_camps()
│   └── detect_camp_color_hsv()
├── detect_casualties()
│   └── detect_casualties_from_mask()
├── assign_casualties_to_camps()
├── calculate_metrics()
└── save_outputs()
```

### 7. ✅ Professional Logging
**Before:** `print()` statements everywhere

**After:** Structured logging
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger.info("Detected 3 camps")
logger.warning("No available camp for casualty")
logger.error("Failed to load image", exc_info=True)
```

### 8. ✅ Input Validation
**Before:** No validation, potential crashes

**After:** 
```python
# Bounds checking
if not (0 <= y < self.hsv_image.shape[0] and 0 <= x < self.hsv_image.shape[1]):
    logger.warning(f"Position ({x}, {y}) out of bounds")
    return 'grey'

# Null checks
if M["m00"] == 0:
    continue

# Empty result handling
if len(self.casualties) == 0:
    logger.warning("No casualties detected")
    return False
```

### 9. ✅ Fixed Dead/Unused Code
**Before:**
```python
image_scores = []
image_scores.append((image, rescue_ratio))
ranked_images = [name for name, _ in image_scores]  # Never used
```

**After:** Removed entirely (or would be properly implemented for multi-image processing)

### 10. ✅ Configurable Output Paths
**Before:** Hardcoded "_1" suffix
```python
cv2.imwrite("output/segmented_1.png", segmented)
```

**After:** Configurable paths using pathlib
```python
OUTPUT_DIR = Path("output")
SEGMENTED_FILENAME = "segmented.png"

output_path = self.config.OUTPUT_DIR / self.config.SEGMENTED_FILENAME
cv2.imwrite(str(output_path), segmented)
```

### 11. ✅ Comprehensive Reporting
**Before:** Basic print statements

**After:** Detailed formatted report
```
===========================================================
DISASTER RELIEF ASSIGNMENT REPORT
===========================================================

Image: task_images/4.png
Total Camps: 3
Total Casualties Detected: 12
Casualties Assigned: 11
Casualties Unassigned: 1

-----------------------------------------------------------
CAMP DETAILS:
-----------------------------------------------------------

Camp 1 (BLUE):
  Position: (150, 200)
  Capacity: 4
  Assigned: 4/4
  Priority Total: 18
  Casualties:
    1. Elderly - Severe (Priority: 6)
    2. Child - Mild (Priority: 6)
    ...
```

### 12. ✅ Better Algorithm Documentation
Clear scoring formula with explanation:
```python
def calculate_assignment_score(self, casualty: Casualty, camp: Camp) -> float:
    """
    Calculate assignment score for a casualty-camp pair.
    
    Score = Priority / (Distance + 1)
    
    Higher priority and shorter distance = better score
    """
    priority = casualty.priority()
    distance = self.calculate_distance(casualty.position, camp.position)
    return priority / (distance + 1.0)
```

## Additional Features

### Type Safety
- Full type hints throughout
- Type-checked dataclasses
- Better IDE autocomplete

### Pathlib for File Handling
- Cross-platform path handling
- Cleaner path operations
- Automatic directory creation

### Extensibility
Easy to extend:
```python
# Add new casualty condition
Config.CASUALTY_COLORS['critical'] = {
    'ranges': [...],
    'score': 4
}

# Add new camp type
Config.CAMP_COLORS['red'] = {
    'hue_range': (0, 10),
    'capacity': 5
}
```

### Better Testing Support
Modular design makes unit testing easy:
```python
def test_priority_calculation():
    casualty = Casualty(
        position=(0, 0),
        age='elderly',
        age_score=2,
        condition='severe',
        condition_score=3
    )
    assert casualty.priority() == 6
```

## Usage

### Basic Usage
```python
from disaster_relief_refactored import DisasterReliefAssignment

# Run with default configuration
system = DisasterReliefAssignment("task_images/4.png")
system.run()
```

### Custom Configuration
```python
# Create custom config
custom_config = Config()
custom_config.CIRCLE_DETECTION['min_radius'] = 20
custom_config.CIRCLE_DETECTION['max_radius'] = 80

system = DisasterReliefAssignment("image.png", config=custom_config)
system.run()
```

### Advanced Usage
```python
system = DisasterReliefAssignment("image.png")

# Run step by step
system.load_image()
system.detect_camps()
system.detect_casualties()
system.assign_casualties_to_camps()

# Get metrics
metrics = system.calculate_metrics()
print(f"Rescue ratio: {metrics['rescue_ratio']}")

# Custom visualization
system.save_assignment_visualization()
```

## Code Quality Metrics

| Metric | Before | After |
|--------|--------|-------|
| Lines of Code | ~280 | ~550 |
| Functions | ~5 | ~20 |
| Classes | 0 | 4 |
| Type Hints | 0% | 100% |
| Documentation | Minimal | Comprehensive |
| Error Handling | Poor | Robust |
| Configuration | Scattered | Centralized |
| Testability | Low | High |

## Performance Considerations

The algorithm remains O(n*m) for casualty-camp assignment where:
- n = number of casualties
- m = number of camps

For better performance with large datasets, consider:
1. **Hungarian Algorithm** for optimal assignment (O(n³))
2. **Spatial Indexing** (KD-tree) for distance queries
3. **Parallel Processing** for independent operations

Example optimization:
```python
from scipy.optimize import linear_sum_assignment

def optimal_assign(self):
    # Create cost matrix (negative score for minimization)
    cost_matrix = np.zeros((len(casualties), len(camps)))
    for i, casualty in enumerate(casualties):
        for j, camp in enumerate(camps):
            cost_matrix[i, j] = -self.calculate_assignment_score(casualty, camp)
    
    # Solve assignment problem
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
```

## Future Enhancements

1. **Multi-image Processing**: Batch processing with ranking
2. **Real-time Processing**: Video stream analysis
3. **Machine Learning**: Learn optimal assignment from historical data
4. **Web Interface**: Flask/FastAPI REST API
5. **Database Integration**: Store results in SQL/NoSQL database
6. **Geospatial Analysis**: Real GPS coordinates support
7. **Priority Weights**: Configurable weights for age vs condition

## Requirements

```
opencv-python>=4.5.0
numpy>=1.19.0
python>=3.7
```
