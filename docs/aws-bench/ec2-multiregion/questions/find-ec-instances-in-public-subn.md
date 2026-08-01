# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
```

## AWS CDK — answered

23 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::RouteTable" or .value.Type == "AWS::EC2::Route") | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -50
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SubnetRouteTableAssociation") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, subnetTags: .value.Properties.Tags}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, subnetTags: .value.Properties.Tags}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, subnet: .Metadata.SubnetId}'
aws ec2 describe-instances --instance-ids i-99224a9cff337e5b0 i-5fdf2028dd5a7a28d i-f5d8c3aa998285b73 i-754790856a4ef8150 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, subnetId: .SubnetId, vpcId: .VpcId, tags: .Tags}'
aws ec2 describe-subnets --subnet-ids subnet-default-a subnet-ed687450 subnet-71ad586d --region us-east-1 2>/dev/null | jq '.Subnets[] | {subnetId: .SubnetId, cidr: .CidrBlock, mapPublicIp: .MapPublicIpOnLaunch, tags: .Tags}'
# … 11 more
```
