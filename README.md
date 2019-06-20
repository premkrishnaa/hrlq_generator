### 0-1 HRLQ Generator

Requirement: python3, cplex (python3)

Usage:

```
python3 generate_instance.py <n1> <n2> <k> <cap> <output_path>
```

where n1 is the number of residents, n2 is the number of hospitals, k is the fixed preference list length of all residents, cap is the capacity/upper quota of all hospitals, output_path is the file to which the generated HRLQ instance is written.