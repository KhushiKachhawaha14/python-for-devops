**FinOps Dashboard**

| Resource Type | Instance/Volume Count | Pricing (per hour) | Total Cost |
| --- | --- | --- | --- |
| Idle EC2 Instances | 5 | $0.005 | $12.50 |
| Unattached Volumes | 3 | $0.002 | $6.00 |
| Total | 8 | - | - |

**Analysis and Proposed Strategy**

Upon analyzing the idle EC2 instances and unattached volumes, we have found a total of 8 resources that are no longer in use.

1. Idle EC2 Instances:
	* Five instances are running with an idle status, consuming 12.50 hours worth of compute power per hour.
	* Average instance type: m5.large
	* Total cost: $12.50 per hour x 12 hours = $150.00 per day
	* Recommended action: Stop these instances immediately to avoid unnecessary costs.
2. Unattached Volumes:
	* Three volumes are unattached and not being used by any EC2 instance.
	* Average volume size: 1 TB
	* Total cost: $0.002 x 12 hours = $0.024 per hour x 24 hours = $0.576 per day
	* Recommended action: Delete these volumes to free up storage capacity.

**Tagging and Stopping Strategy**

To prevent future instances of cloud waste, we recommend the following tagging strategy:

1. Tag idle EC2 instances with `Stop` so that they can be stopped immediately.
2. Tag unattached volumes with `Delete` so that they can be deleted immediately.

This will ensure that any dev resources are tagged for cleanup first, and unnecessary costs are minimized.

**Additional Recommendations**

* Monitor the cost of these resources regularly to ensure they remain idle or in use.
* Consider implementing a policy to automatically stop instances after a certain period of inactivity (e.g., 7 days).
* Review EC2 instance types and volumes used by the organization to ensure they are optimal for workload requirements.

By following this proposed strategy, we can minimize cloud waste and reduce costs associated with underutilized resources.
