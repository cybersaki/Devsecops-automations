Firewall Automation for Network Traffic on AWS configures the AWS resources needed to filter network traffic. 
This solution saves you time by automating the process of provisioning a centralized AWS Network Firewall to inspect traffic between your Amazon Virtual Private Clouds 
(Amazon VPCs).

1) Create an S3 bucket with the bucket appended with the region in which the deployment is to be made. example, if the deployment is to be made in us-east-1 create a bucket name as [BUCKET_NAME]-us-east-1.
2) Create the distribution files using the script provided in the build section above.
3) Create the S3 Key in the bucket network-firewall-automation/[VERSION_ID]/
4) Create the S3 Key in the bucket network-firewall-automation/latest/
5) Copy the file ./deployment/regional-s3-assets/network-firewall-automation.zip to the location s3://[BUCKET_NAME]-[REGION]/network-firewall-automation/[VERSION_ID]/
6) Copy the file ./deployment/regional-s3-assets/network-firewall-configuration.zip to the location s3://[BUCKET_NAME]-[REGION]/network-firewall-automation/latest/
7) Once the above steps are completed, use the file ./deployment/global-s3-assets/firewall-automation-for-network-traffic-on-aws.template to create a stack in CloudFormation.

Full source code and original repo : https://github.com/aws-solutions/firewall-automation-for-network-traffic-on-aws
