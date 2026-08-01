# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PublicIpAddress,PrivateIpAddress,effectiveIngress,internetFacing 2>&1
```

## No tool (AWS CLI) — missed

3 commands, from `bare-m2`.

```sh
for region in us-east-1 us-west-1 us-west-2; do echo "=== $region ===" aws ec2 describe-instances --region "$region" --output json --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name,SecurityGroups[].GroupId,LaunchTemplate]' | jq -c '.[]' done
for region in us-east-1 us-west-1 us-west-2; do echo "=== $region Security Groups ===" aws ec2 describe-security-groups --region "$region" --output json | jq -c '.SecurityGroups[] | select(.GroupName == "default" or .GroupId == "sg-ad116af2c9fab45df") | {GroupId: .GroupId, GroupName: .GroupName, IpPermissions: .IpPermissions}' done
aws ec2 describe-instances --region us-east-1 --instance-ids i-e722b733ce65157b5 --output json | jq '.Reservations[].Instances[] | {InstanceId, InstanceType, State: .State.Name, PublicIpAddress, PublicDnsName, SecurityGroups, LaunchTime}'
```

## Terraform — answered

15 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module' > /tmp/state.json && cat /tmp/state.json | head -100
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance" or .type == "aws_security_group" or .type == "aws_security_group_rule" or .type == "aws_launch_template") | {address, type, values: {id: .values.id, region: .values.region, availability_zone: .values.availability_zone, security_groups: .values.security_groups, vpc_security_group_ids: .values.vpc_security_group_ids, launch_template: .values.launch_template, ingress: .values.ingress, tags: .values.tags}}' 2>/dev/null
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_security_group|aws_launch_template'
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.launch_template_server
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.private_server
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.web_server
cd /workspace/terraform && ./terraform state show module.west1.aws_instance.server
cd /workspace/terraform && ./terraform state show module.west2.aws_instance.server
cd /workspace/terraform && ./terraform state show module.primary.aws_security_group.web
cd /workspace/terraform && ./terraform state show module.primary.aws_security_group.unused
cd /workspace/terraform && ./terraform state show module.primary.aws_launch_template.this
# … 3 more
```

## Pulumi — answered

10 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq '.deployment.resources | length' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {id: .outputs.id, vpc_security_group_ids: .outputs.vpc_security_group_ids, availability_zone: .outputs.availability_zone}, inputs: {vpc_security_group_ids: .inputs.vpc_security_group_ids, associate_public_ip_address: .inputs.associate_public_ip_address, launch_template: .inputs.launch_template}}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: .outputs, dependencies: .dependencies}' /tmp/pulumi-state.json | head -100
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, id: .outputs.id, region: (.outputs.arn | split(":")[3]), availabilityZone: .outputs.availabilityZone, securityGroups: .outputs.securityGroups, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds, publicIp: .outputs.publicIp, associatePublicIpAddress: .outputs.associatePublicIpAddress, launchTemplate: .outputs.launchTemplate}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("SecurityGroup")) | {urn, id: .outputs.id, outputs: .outputs}' /tmp/pulumi-state.json | head -200
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("SecurityGroup")) | {name: .outputs.name, id: .outputs.id, region: (.outputs.arn | split(":")[3]), ingress: .outputs.ingress}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("LaunchTemplate")) | {urn, outputs: {id: .outputs.id, securityGroupNames: .outputs.securityGroupNames, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds}}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance" and .outputs.id == "i-78e8a59ba46fb6c42") | {urn, inputs: .inputs, outputs: {id: .outputs.id, launchTemplate: .outputs.launchTemplate, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds}}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("SecurityGroupRule")) | {type, id: .outputs.id, groupId: .outputs.groupId, ingressRule: (.outputs | select(.isEgress == false)), egressRule: (.outputs | select(.isEgress == true))}' /tmp/pulumi-state.json
cat > /tmp/analysis.txt << 'EOF' ANALYSIS OF EC2 INSTANCES REACHABLE VIA SSH FROM THE INTERNET Instance Summary: 1. defaultVpcServer (i-9ba197454f1e877e8) - us-east-1 - Public IP: 54.144.201.147 - Security Group: default (AWS default VPC security group) - SSH Reachable: NO - default VPC SG does not allow SSH from internet 2. privateServer (i-a7c4a355f370bbbb6) - us-east-1 - Public IP: NONE (private subnet) - SSH Reachable: NO - no public IP 3. webServer (i-74619d8f0954593db) - us-east-1 - Public IP: 54.144.16.191 - Security Group: sg-d17e6bf064b23680f (webSg) - Ingress Rules: * Port 22 (SSH) from 0.0.0.0/0 ✓ * Port 80 (HTTP) from 0.0.0.0/0 * Port 443 (HTTPS) from 0.0.0.0/0 - SSH Reachable: YES ✓ 4. ltServer (i-78e8a59ba46fb6c42) - us-east-1 - Public IP: 54.144.181.75 - Security Group: sg-d17e6bf064b23680f (inherited from launch template lt) - Same security group as webServer (webSg) - SSH Reachable: YES ✓ 5. usw1-server (i-7da3b7c91f5e6f842) - us-west-1 - Public IP: 54.144.147.201 - Security Group: default (AWS default VPC security group) - SSH Reachable: NO - default VPC SG does not allow SSH from internet 6. usw2-server (i-49228acd82333760d) - us-west-2 - Public IP: 54.144.153.4 - Security Group: default (AWS default VPC security group) - SSH Reachable: NO - default VPC SG does not allow SSH from internet EOF cat /tmp/analysis.txt
```

## AWS CDK — answered

11 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance_name: .value.Properties.Tags[0].Value, security_groups: .value.Properties.SecurityGroupIds}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroup") | {name: .key, ingress: .value.Properties.SecurityGroupIngress}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.LaunchTemplateInstance'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.key | contains("LaunchTemplate")) | {name: .key, type: .value.Type, properties: .value.Properties}'
```

## Alchemy — answered

20 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for instance in instance defaultVpcServer ltServer private privateServer webServer usw1-server usw2-server; do echo "=== alchemy-ec2-multiregion/bench/$instance ===" alchemy state get "alchemy-ec2-multiregion/bench/$instance" 2>/dev/null | jq -c '{kind, region: .output.region, vpc_id: .output.vpc_id, security_group_ids: .output.security_group_ids, launch_template_id: .output.launch_template_id}' done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/webServer" | head -100
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/defaultVpcServer" | jq '.output | {InstanceId, region, SecurityGroupIds}'
cd /workspace/alchemy && alchemy state list | grep -E '(Instance|LaunchTemplate)' | head -20
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *.json; do kind=$(jq -r '.kind // "unknown"' "$f" 2>/dev/null) if [[ "$kind" == "AWS::EC2::Instance" ]]; then echo "=== $(basename "$f" .json) ===" jq -c '{kind: .kind, region: .output.region, InstanceId: .output.InstanceId, SecurityGroupIds: .output.SecurityGroupIds, LaunchTemplateId: .output.LaunchTemplateId}' "$f" 2>/dev/null fi done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *.json; do kind=$(jq -r '.kind // "unknown"' "$f" 2>/dev/null) if [[ "$kind" == "AWS::EC2::SecurityGroup" ]]; then echo "=== $(basename "$f" .json) ===" jq -c '{kind: .kind, GroupId: .output.GroupId, GroupName: .output.GroupName, region: .output.region}' "$f" 2>/dev/null fi done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *.json; do kind=$(jq -r '.kind // "unknown"' "$f" 2>/dev/null) if [[ "$kind" == *"SecurityGroup"* ]]; then echo "=== $(basename "$f" .json) ===" jq -c '{kind: .kind, id: .id}' "$f" 2>/dev/null fi done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/web" | jq '.'
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/web-ssh" | jq '.'
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *.json; do jq -r 'select(.kind == "aws::SecurityGroupRule" and (.output.securityGroup.groupName // "" | contains("default")) or (.output.cidrBlocks[]? == "0.0.0.0/0")) | .id + " | " + (.output.type // "N/A") + " | " + (.output.protocol // "N/A") + " | " + ((.output.fromPort // "N/A") | tostring) + ":" + ((.output.toPort // "N/A") | tostring) + " | " + (.output.cidrBlocks[]? // "N/A")' "$f" 2>/dev/null done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in *.json; do kind=$(jq -r '.kind // "unknown"' "$f" 2>/dev/null) if [[ "$kind" == "aws::SecurityGroupRule" ]]; then echo "=== $(basename "$f" .json) ===" jq -c '{type: .output.type, protocol: .output.protocol, fromPort: .output.fromPort, toPort: .output.toPort, cidrBlocks: .output.cidrBlocks, groupName: .output.securityGroup.groupName, region: .output.securityGroup.region}' "$f" 2>/dev/null fi done
# … 8 more
```
