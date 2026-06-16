# Document your edge case here

## Edge Case: Some Students Have No Marks (mark is None)

### 1) Identified Edge Case
When there are students in the system who have no marks (mark is None), how the /stats endpoint handles this data is an edge case that needs to be considered. Possible questions include:
- Should we ignore students without marks when calculating statistics?
- Should count represent the total number of students or the number of students with marks?
- What should the statistics return if all students have no marks?

### 2) My Approach
In the implementation of the /stats endpoint, I adopted the following strategies:
1. **Filter valid marks**: Only count marks where mark is not None
2. **count definition**: count represents the number of students with marks, not the total number of students
3. **Empty data handling**: When there are no valid marks, return count as 0, with average, min, and max as None

This approach ensures:
- Accuracy of statistics (calculated only based on students with marks)
- Robustness of the endpoint (won't crash due to missing data)
- Consistency of statistics (count, average, min, max are all based on the same dataset)