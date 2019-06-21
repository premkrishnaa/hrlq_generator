### 0-1 HRLQ Generator

Requirement: python3, cplex (python3)

Usage:

```
python3 generate_instance.py <n1> <n2> <k> <cap> <output_path> <option>
```

where n1 is the number of residents, n2 is the number of hospitals, k is the fixed preference list length of all residents, cap is the capacity/upper quota of all hospitals, output_path is the file to which the generated HRLQ instance is written. 

When option=0, there is no restriction on the MCM LP,
When option=1, we add artificial LQ constraints in the MCM LP so that |M_c(h)| >= |M_s(h)|