# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region
```

## AWS CDK — answered

8 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-east-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-2", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
```
