# CHIDS

| CHIDS is an unsupervised anomaly-based host intrusion detection system for containers. CHIDS relies on monitoring heterogeneous properties of system calls (syscalls). The development of CHIDS is based on the premise that malicious activities can be accurately uncovered when various syscall properties (e.g., frequency, arguments) are inspected jointly within their context. In detail, CHIDS learns container "normal" behavior and flags deviations in production. | ![ContainerHIDS](https://i0.wp.com/foxutech.com/wp-content/uploads/2017/03/Docker-Security.png?fit=820%2C407&ssl=1 "ContainerHIDS") |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------:|

## CHIDS Architecture
![Architecture](https://github.com/Asbatel/testhere/blob/master/figures/architecture.png "ContainerHIDS")

- **Syscalls Chunking.**
We divide the ongoing flow of system calls into short captures *scaps*, defined as *syscall sequences*. 

- **Syscalls Encoding.** 
We transform each syscall sequence into a *syscall sequence graph* *(SSG)*, from which we extract three features forming the *anomaly vector* *(AV)*. 

- **Model Training.**  We feed the anomaly vector into an unsupervised auto-encoder neural network for training. This training aims to minimize the reconstruction loss and generate a behavioral baseline that represents a given container's normal behavior.

- **Anomaly Detection.**
We classify an anomaly vector based on the trained model and a selected threshold in production.

## Get Training Elements

The training elements are the following:
   - previously seen syscalls
   - previously seen args
   - the max SSG training size or (max len of training sequences)
   - the thresholds list
   - the trained model
```
$> python3 main.py baseline  --td training_dir --od output_dir
```
### Example: Brute-Force Login (CWE-307) Training Summary

![(Brute-Force Login Example)](https://github.com/Asbatel/testhere/blob/master/figures/screenshots/training_results.png "ContainerHIDS")


## Get Evaluation Results 

The evaluation script takes as inputs the following elements: 
   - previously seen syscalls
   - previously seen args
   - the max SSG training size or (max len of training sequences)
   - the thresholds list
   - the trained model
```
$> python3 main.py evaluate --ss output_dir/seen_syscalls.pkl --sa output_dir/seen_args.pkl --fm  output_dir/max_freq.pkl --tm  output_dir/model.h5 --tl output_dir/thresh_list.pkl --ns normal_scaps --ms malicious_scaps 
```

### Example: Brute-Force Login (CWE-307) Evaluation Summary

![(Brute-Force Login Example)](https://github.com/Asbatel/testhere/blob/master/figures/screenshots/evaluation_results.png)
