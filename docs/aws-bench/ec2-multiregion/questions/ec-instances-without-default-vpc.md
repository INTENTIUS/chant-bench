# Which of my EC2 instances don't have a default VPC?

`ec-instances-without-default-vpc` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

4 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show providerDefault
cd /workspace/chant && chant search "kind:EC2::Instance !->kind:EC2::VPC ->attr:providerDefault=true" --at latest --env floci --show VpcId,region
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain | grep -v "vpc-default"
```

## AWS CDK — answered

10 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, instanceName: (.value.Properties.Tags[]? | select(.Key=="Name") | .Value), subnetId: (.value.Properties.SubnetId | if type == "object" then "VPC_REF" else . end)}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, instanceName: (.value.Properties.Tags[]? | select(.Key=="Name") | .Value), subnetId: (.value.Properties.SubnetId | if type == "object" then "VPC_REF" else . end)}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, instanceName: (.value.Properties.Tags[]? | select(.Key=="Name") | .Value), subnetId: (.value.Properties.SubnetId | if type == "object" then "VPC_REF" else . end)}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {logicalId: .key, type: .value.Type, vpcId: (.value.Properties.VpcId // "N/A"), cidr: (.value.Properties.CidrBlock // "N/A")}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {logicalId: .key, type: .value.Type, cidr: (.value.Properties.CidrBlock // "N/A")}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {logicalId: .key, type: .value.Type, cidr: (.value.Properties.CidrBlock // "N/A")}'
cat > /tmp/analyze_instances.sh << 'EOF' #!/bin/bash cd /workspace/cdk_app echo "=== ANALYZING ALL EC2 INSTANCES ===" echo "" STACKS=( "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2" ) for stack in "${STACKS[@]}"; do echo "Processing stack: $stack" region=$(echo $stack | grep -oE '(us-east-1|us-west-1|us-west-2)$') # Get all instances with their subnet info npx cdk synth "$stack" --json 2>/dev/null | jq -r " . as \$root | .Resources | to_entries[] | select(.value.Type == \"AWS::EC2::Instance\") | { region: \"$region\", logicalId: .key, instanceName: (.value.Properties.Tags[]? | select(.Key==\"Name\") | .Value), subnetId: .value.Properties.SubnetId, subnetRef: (.value.Properties.SubnetId | type) } | .subnetIdStr = ( if .subnetRef == \"object\" then \"CloudFormation Reference\" else .subnetId end ) | {region, logicalId, instanceName, subnetIdStr} " echo "" done EOF bash /tmp/analyze_instances.sh
find /workspace/cdk_app -type f -name "*.ts" | head -20
```
