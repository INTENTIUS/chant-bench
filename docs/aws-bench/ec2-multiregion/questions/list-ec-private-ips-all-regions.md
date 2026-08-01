# List all of my EC2 and their private ip in a table.

`list-ec-private-ips-all-regions` · the answer aws-bench grades against: **6 instances with private IPs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1" --at latest --env floci --show PrivateIpAddress,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1" --at latest --env floci --show PrivateIpAddress,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2" --at latest --env floci --show PrivateIpAddress,region --explain
```

## AWS CDK — answered

11 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys[] as $k | select(.Resources[$k].Type == "AWS::EC2::Instance") | .Resources[$k]' 2>/dev/null || npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {id: .key, resource: .value}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/template-us-east-1.json && cat /tmp/template-us-east-1.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/template-us-west-1.json && cat /tmp/template-us-west-1.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/template-us-west-2.json && cat /tmp/template-us-west-2.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-99224a9cff337e5b0 i-5fdf2028dd5a7a28d i-f5d8c3aa998285b73 i-754790856a4ef8150 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
aws ec2 describe-instances --instance-ids i-c52758030f5620e05 --region us-west-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
aws ec2 describe-instances --instance-ids i-e1c4d75f234795b0a --region us-west-2 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, PrivateIp: .PrivateIpAddress, State: .State.Name, InstanceType: .InstanceType}'
```
