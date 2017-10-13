#!/bin/env bash

AWS_ENV=${AWS_ENV:-/home/ubuntu/aws_env}
source $AWS_ENV/bin/activate
DOCKER_LOGING=`aws ecr get-login --no-include-email --region us-east-1`
sudo docker push 687433828854.dkr.ecr.us-east-1.amazonaws.com/inventory:latest
