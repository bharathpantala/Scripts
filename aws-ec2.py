#!/bin/sh

# You don't need these, assign the servers to a role instead
export AWS_ACCESS_KEY=<aws-access-key>
export AWS_SECRET_KEY=<aws-secret-key>


export PATH=$PATH:/opt/aws/bin
export JAVA_HOME=/usr/lib/jvm/jre
export EC2_HOME=/opt/aws/apitools/ec2

DATE=`date +%Y-%m-%d`
TIME=`date +'%R:%S'`

# find availability zone, for example eu-west-1b
EC2_AVAILABILITY_ZONE=`curl http://169.254.169.254/latest/meta-data/placement/availability-zone`

# remove last letter to get region
EC2_REGION="${EC2_AVAILABILITY_ZONE%?}"
# set EC2_URL environment variable. We ignore it by using the --region switch directly
# export EC2_URL=ec2.$EC2_REGION.amazonaws.com

# find this instance id
EC2_INSTANCE_ID=`curl http://169.254.169.254/latest/meta-data/instance-id/`

# find this volume. only works for single volume servers.
ec2string=`ec2-describe-instance-attribute  --region $EC2_REGION  $EC2_INSTANCE_ID -b`
ec2arr=($ec2string)
EC2_VOLUME=${ec2arr[2]}

# send backup and get snapshot id
echo ec2-create-snapshot  --region $EC2_REGION  $EC2_VOLUME -d "Weekly backup $DATE.$TIME"

ec2string=`ec2-create-snapshot  --region $EC2_REGION  $EC2_VOLUME -d "Weekly backup $DATE.$TIME"`
ec2arr=($ec2string)
EC2_SNAPSHOT=${ec2arr[1]}


# get Name attribute
echo ec2-describe-tags --region $EC2_REGION --filter "resource-id=$EC2_INSTANCE_ID" --filter "key=Name"

ec2string=`ec2-describe-tags --region $EC2_REGION --filter resource-id=$EC2_INSTANCE_ID --filter key=Name`
ec2arr=($ec2string)
EC2_INSTANCE_NAME=${ec2arr[4]}

# create Name tag for snapshot
echo ec2-create-tags  --region $EC2_REGION  $EC2_SNAPSHOT --tag "Name=$EC2_INSTANCE_NAME"
ec2-create-tags  --region $EC2_REGION  $EC2_SNAPSHOT --tag "Name=$EC2_INSTANCE_NAME"
