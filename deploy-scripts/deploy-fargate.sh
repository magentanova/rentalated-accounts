CURRENTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && cd ../ && pwd )"

## SET UP ROLE && ATTACHED POLICY(IES) FOR THIS TASK

# create a role, and give it a policy such that it is permitted to "AssumeRole" (a 60-minute time window which allows this role to assume other roles ...?)
aws iam --region us-east-2 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://$CURRENTDIR/task-execution-assume-role.json

# attach a "role policy" to the role we just created, one which allows it to execute ECS tasks, which means it's able to pull ECS images from the registry 
    # and also to write log files to CloudWatch
aws iam --region us-east-2 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy


## CONFIGURE THE ECS CLI

# create a cluster configuration
ecs-cli configure --cluster listings --region us-east-2 --default-launch-type FARGATE --config-name listings

# create a cli profile for the cluster  
ecs-cli configure profile


## CREATE A CLUSTER AND SECURITY GROUP

# create a cluster
    # "Because you specified Fargate as your default launch type in the cluster configuration,
    # this command creates an empty cluster and a VPC configured with two public subnets."
ecs-cli up 

## (this should be handled differently. maybe get a vpc id at a different point and hardcode it into the above command.)
VPCID=vpc-0d8dd1ffa36db3207

## (same as above)
SGID=sg-0f6dad2af091a5bd3

# create a security group 
aws ec2 create-security-group --group-name "rentalated-sg" --description "Security group for rentalated ec2s" --vpc-id $VPCID

# add a rule to allow all traffic to port 80
aws ec2 authorize-security-group-ingress --group-id $SGID --protocol tcp --port 80 --cidr 0.0.0.0/0

##  DEPLOY COMPOSE FILES TO THE CLUSTER

ecs-cli compose --file $CURRENTDIR/docker-compose.prod.yml --ecs-params $CURRENTDIR/ecs-params.yml 
    --project-name listings service up --create-log-groups --cluster-config listings 
