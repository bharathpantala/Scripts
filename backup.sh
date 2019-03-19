#!/bin/bash 
#################################### 
# 
# Backup to NFS mount script. 
# 
#################################### 
# What to backup. 
backup_source="/etc" 
# Where to backup to. 
destination="/backups" 
# Create archive filename. 
day=$(date +%F%A) 
username=$(whoami) 
archive_file="$username-$day.tar.gz" 
# Print start status message. 
echo "Backing up $backup_source to $destination/$archive_file" 
date 
echo 
# Backup the files using tar. 
tar -czf $destination/$archive_file $backup_source 
# sending file to AWS Ss bbucket 
aws s3 cp $destination/$archive_file s3://linux.packages/linux_packages/ 
# Print end status message. 
echo 
echo "Backup finished" 
date 
# Long listing of files in $dest to check file sizes. 
ls -lh $destination
