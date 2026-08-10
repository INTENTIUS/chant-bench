# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region
```

## No tool (AWS CLI) — answered

3 commands, from `bare-i3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[*].Instances[*].[InstanceId]' | jq -r '.[][]'
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[*].Instances[*].[InstanceId]' | jq -r '.[][]'
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[*].Instances[*].[InstanceId]' | jq -r '.[][]'
```

## Terraform — answered

8 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | (.. | .resources[]? | select(.type == "aws_instance") | {address: .address, instance_id: .values.id, availability_zone: .values.availability_zone})'
cd /workspace/terraform && ./terraform state show -json module.primary.aws_instance.default_vpc_server | jq '{instance_id: .values.id, availability_zone: .values.availability_zone}'
cd /workspace/terraform && ./terraform show -json | jq '.' | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | (.resources[] | select(.type == "aws_instance") | {address: .address, instance_id: .values.id, availability_zone: .values.availability_zone}) | @base64' | base64 -d
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[].address' | head -20
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address | startswith("module.")) | {module: .address, instances: [.resources[] | select(.type == "aws_instance") | {instance_id: .values.id, availability_zone: .values.availability_zone, region: (.values.availability_zone | sub("[a-z]$"; ""))}]}'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module.child_modules[] | {module: .address, instances: [.resources[] | select(.type == "aws_instance") | {instance_id: .values.id, availability_zone: .values.availability_zone}]} | "\(.module):\n" + (.instances | map(" - \(.instance_id) (\(.availability_zone))") | join("\n")) + "\n"' > /logs/agent/agent-output.txt && cat /logs/agent/agent-output.txt
```

## Pulumi — answered

2 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, id: .outputs.id, region: .outputs.availabilityZone} | {instance_id: .id, arn: .urn, availability_zone: .region}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | [.outputs.id, .outputs.availabilityZone] | @tsv' | sort -k2 > /tmp/instances.txt && cat /tmp/instances.txt
```

## AWS CDK — answered

9 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-east-1"}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-west-1"}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Region: "us-west-2"}'
cat > /logs/agent/agent-output.txt << 'EOF' EC2 Instance IDs by Region ========================== US-EAST-1 (4 instances) ----------------------- Instance Name Instance ID WebServerInstance i-8efe413fb2db04cc6 MyEC2Instance i-7d9001a08d554ad03 PrivateInstance i-c4deff6351c208ad9 LaunchTemplateInstance i-2406a03b9ade076f4 US-WEST-1 (1 instance) ---------------------- Instance Name Instance ID WebServerInstance i-fde88288e4fcb0f27 US-WEST-2 (1 instance) ---------------------- Instance Name Instance ID WebServerInstance i-c18071845f3e04292 TOTAL: 6 EC2 instances across 3 regions EOF cat /logs/agent/agent-output.txt
```

## Alchemy — answered

6 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for resource in instance private privateServer defaultVpcServer ltServer webServer web usw1-server usw2-server; do echo "=== Checking $resource ===" alchemy state get alchemy-ec2-multiregion/bench/$resource 2>/dev/null | jq -r '.kind + ": " + (.output.instance_id // .output.id // "N/A")' done
cd /workspace/alchemy && for resource in privateServer defaultVpcServer ltServer webServer usw1-server usw2-server; do alchemy state get alchemy-ec2-multiregion/bench/$resource 2>/dev/null | jq '{resource: "'$resource'", kind: .kind, instance_id: .output.instance_id, region: .output.availability_zone}' done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/privateServer 2>/dev/null | jq '.output | keys'
cd /workspace/alchemy && for resource in privateServer defaultVpcServer ltServer webServer usw1-server usw2-server; do alchemy state get alchemy-ec2-multiregion/bench/$resource 2>/dev/null | jq '{resource: "'$resource'", instance_id: .output.InstanceId, region: .output.region, availability_zone: .output.AvailabilityZone}' done
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instance IDs by Region ## us-east-1 (4 instances) - i-b0486cc893ddd7bfa (privateServer, us-east-1a) - i-f790634a64f31b54d (defaultVpcServer, us-east-1c) - i-75367a863c9a41c2a (ltServer, us-east-1a) - i-22d6ee20dfcf1a449 (webServer, us-east-1a) ## us-west-1 (1 instance) - i-6bec89de8180a8f42 (usw1-server, us-west-1a) ## us-west-2 (1 instance) - i-df124de17e5a70593 (usw2-server, us-west-2a) ## Summary Total EC2 instances: 6 Regions: us-east-1, us-west-1, us-west-2 EOF cat /logs/agent/agent-output.txt
```

## Alchemy v2 (Effect) — missed

3 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local | jq '.resources[] | select(.state.resourceType == "aws:ec2/instance:Instance") | {stack, stage, instance_id: .state.attr.id, region: .state.attr.availabilityZone}' | head -100
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>&1 | jq '.resources[] | select(.state.resourceType == "aws:ec2/instance:Instance") | {stack, instance_id: .state.attr.id}'
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | head -20
```
