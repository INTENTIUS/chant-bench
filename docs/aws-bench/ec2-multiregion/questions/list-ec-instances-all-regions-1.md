# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

5 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant lifecycle show floci
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true" --at latest --env floci --show PrivateIpAddress,PublicIpAddress,effectiveIngress --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:effectiveIngress=*tcp:22:0.0.0.0/0*" --at latest --env floci --show region,PrivateIpAddress,PublicIpAddress --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress,PublicIpAddress,effectiveIngress
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress,PublicIpAddress,internetFacing,effectiveIngress
```

## No tool (AWS CLI) — missed

2 commands, from `bare-m3`.

```sh
# Collect all instances and their security groups across regions # and determine which ones allow SSH from the internet REGIONS=("us-east-1" "us-west-1" "us-west-2") declare -A all_instances declare -A sg_details # Function to get security groups for an instance (direct + from launch template) get_instance_sgs() { local region=$1 local instance_id=$2 local sgs=() # Get directly attached security groups direct_sgs=$(aws ec2 describe-instances --region "$region" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].SecurityGroups[*].GroupId' --output json) while IFS= read -r sg; do sg=$(echo "$sg" | tr -d '"') if [ -n "$sg" ]; then sgs+=("$sg") fi done < <(echo "$direct_sgs" | jq -r '.[]') # Get security groups from launch template if present lt_id=$(aws ec2 describe-instances --region "$region" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].LaunchTemplate.LaunchTemplateId' --output text 2>/dev/null) if [ "$lt_id" != "None" ] && [ -n "$lt_id" ]; then template_sgs=$(aws ec2 describe-launch-template-versions --region "$region" --launch-template-id "$lt_id" --query 'LaunchTemplateVersions[0].LaunchTemplateData.SecurityGroupIds[]' --output json 2>/dev/null) while IFS= read -r sg; do sg=$(echo "$sg" | tr -d '"') if [ -n "$sg" ] && [[ ! " ${sgs[@]} " =~ " ${sg} " ]]; then sgs+=("$sg") fi done < <(echo "$template_sgs" | jq -r '.[]' 2>/dev/null) fi echo "${sgs[@]}" } # Function to check if a security group allows SSH from the internet allows_ssh_from_internet() { local region=$1 local sg_id=$2 # Check for rules allowing port 22 from 0.0.0.0/0 or ::/0 ssh_rules=$(aws ec2 describe-security-groups --region "$region" --group-ids "$sg_id" --query 'SecurityGroups[0].IpPermissions[?FromPort<=`22` && ToPort>=`22`]' --output json) echo "$ssh_rules" | jq -r '.[] | select((.IpRanges[]?.CidrIp == "0.0.0.0/0") or (.Ipv6Ranges[]?.CidrIpv6 == "::/0")) | "true"' | grep -q "true" } echo "Scanning for SSH-accessible instances..." echo "" # Collect all instances for region in "${REGIONS[@]}"; do echo "Querying $region..." aws ec2 describe-instances --region "$region" --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0],LaunchTemplate.LaunchTemplateId]' --output json > /tmp/instances_$region.json done # Process instances and check for SSH accessibility echo "" echo "Checking security groups for internet-facing SSH..." echo "" ssh_accessible=() for region in "${REGIONS[@]}"; do instances=$(jq -r '.[][] | @json' /tmp/instances_$region.json) while IFS= read -r instance_json; do instance=$(echo "$instance_json" | jq -r '.[0]') state=$(echo "$instance_json" | jq -r '.[1]') name=$(echo "$instance_json" | jq -r '.[2] // "N/A"') if [ "$state" != "terminated" ]; then sgs=$(get_instance_sgs "$region" "$instance") # Check if any security group allows SSH from internet ssh_open=false for sg in $sgs; do if allows_ssh_from_internet "$region" "$sg"; then ssh_open=true break fi done if [ "$ssh_open" = true ]; then ssh_accessible+=("$instance|$region|$name|$state|$sgs") fi fi done < <(echo "$instances") done # Output results echo "SSH-Accessible Instances from the Internet:" echo "===========================================" echo "" if [ ${#ssh_accessible[@]} -eq 0 ]; then echo "No instances found that allow SSH access from the internet (0.0.0.0/0)." else echo "Instance ID | Region | Name | State | Security Groups" echo "------|--------|------|-------|------------------" for item in "${ssh_accessible[@]}"; do IFS='|' read -r instance_id region name state sgs <<< "$item" echo "$instance_id | $region | $name | $state | $sgs" done fi
# Get detailed information about the SSH-accessible instance instance_id="i-c78c5d862cbbd5c3e" region="us-east-1" sg_id="sg-2aa9650a4a37f8428" echo "Instance Details:" echo "=================" aws ec2 describe-instances --region "$region" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].[InstanceId,InstanceType,State.Name,Tags[?Key==`Name`].Value|[0],PrivateIpAddress,PublicIpAddress,LaunchTemplate]' --output json | jq '.' echo "" echo "Security Group Configuration:" echo "=============================" aws ec2 describe-security-groups --region "$region" --group-ids "$sg_id" --output json | jq '.SecurityGroups[0] | {GroupId, GroupName, VpcId, IpPermissions}' echo "" echo "SSH Rule Details (0.0.0.0/0):" echo "=============================" aws ec2 describe-security-groups --region "$region" --group-ids "$sg_id" --query 'SecurityGroups[0].IpPermissions[?FromPort<=`22` && ToPort>=`22`]' --output json | jq '.'
```

## Terraform — answered

14 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform show -json | head -100
cd /workspace/terraform && ./terraform show -json > /tmp/terraform_state.json 2>&1 && echo "State saved successfully"
cd /tmp && jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, region: .values.availability_zone[:-1], instance_id: .values.id, security_groups: .values.security_groups, vpc_security_group_ids: .values.vpc_security_group_ids}' terraform_state.json | head -200
cd /tmp && jq '.values.root_module.resources[] | select(.type == "aws_instance")' terraform_state.json
cd /tmp && jq '.values.root_module.resources[].type' terraform_state.json | sort | uniq
cd /tmp && jq '.values.root_module | keys' terraform_state.json
cd /tmp && jq '.values.root_module.child_modules[] | .address' terraform_state.json
cd /tmp && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_instance" or .type == "aws_security_group" or .type == "aws_launch_template")' terraform_state.json
cd /tmp && jq '.values.root_module.child_modules[] | select(.address == "module.west1" or .address == "module.west2") | {module: .address, resources: [.resources[] | select(.type == "aws_instance" or .type == "aws_security_group" or .type == "aws_launch_template") | {type, address, id: .values.id, sg: .values.vpc_security_group_ids, security_groups: .values.security_groups, ingress: .values.ingress, public_ip: .values.public_ip}]}' terraform_state.json
cd /tmp && jq '.values.root_module.child_modules[] | select(.address == "module.west1" or .address == "module.west2") | {module: .address, security_groups: [.resources[] | select(.type == "aws_security_group")]}' terraform_state.json
cd /tmp && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_default_security_group")' terraform_state.json
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_security_group.default' 2>/dev/null || echo "No data source for default security group"
# … 2 more
```

## Pulumi — answered

16 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq '.deployment.resources | length' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | split("-")[:-1] | join("-"), launchTemplate: .inputs.launchTemplate, securityGroups: .inputs.securityGroups, outputs: {id: .outputs.id, subnetId: .outputs.subnetId}}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], az: .outputs.availabilityZone, instanceId: .outputs.id, launchTemplateId: .inputs.launchTemplate.id, securityGroupIds: .inputs.securityGroups, vpcSecurityGroups: .outputs.vpcSecurityGroups}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' /tmp/pulumi-state.json | head -200
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup")' /tmp/pulumi-state.json | jq -r '.id, .outputs.vpcId, .outputs.ingress' | head -100
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | {id: .id, groupId: .outputs.id, groupName: .outputs.name, vpcId: .outputs.vpcId, ingressRules: [.outputs.ingress[] | select(.fromPort == 22 or .toPort == 22)]}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroupIngress:SecurityGroupIngress")' /tmp/pulumi-state.json | jq -r '.id, .inputs' | head -150
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], az: .outputs.availabilityZone, instanceId: .outputs.id, publicIp: .outputs.publicIp, securityGroupIds: .outputs.vpcSecurityGroupIds, launchTemplateId: .inputs.launchTemplate.id}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("SecurityGroup")) | select(.outputs.name == "default" or .id == "sg-default")' /tmp/pulumi-state.json | jq '{id: .id, name: .outputs.name, ingress: .outputs.ingress}'
cd /workspace/pulumi && jq '.deployment.resources[] | select(.outputs.securityGroups? | contains(["default"]))' /tmp/pulumi-state.json | jq '.outputs | {id: .id, securityGroups: .securityGroups}' | head -20
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type | contains("Vpc")) | {id: .id, vpcId: .outputs.id, defaultSecurityGroupId: .outputs.defaultSecurityGroupId}' /tmp/pulumi-state.json
cd /workspace/pulumi && jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | select(.id | IN("sg-fba3692107247a7d2", "sg-ce9e6997a20a3e6cd", "sg-ec37bb9634ae50a5b"))' /tmp/pulumi-state.json | jq '{id: .id, name: .outputs.name, ingress: .outputs.ingress}'
# … 4 more
```

## AWS CDK — answered

12 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq . > /tmp/qaroles.json && echo "QARoles template synthesized"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq . > /tmp/ec2_us_east_1.json && echo "EC2 us-east-1 template synthesized"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq . > /tmp/ec2_us_west_1.json && echo "EC2 us-west-1 template synthesized"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq . > /tmp/ec2_us_west_2.json && echo "EC2 us-west-2 template synthesized"
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].[LogicalResourceId,PhysicalResourceId]' --output table
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].[LogicalResourceId,PhysicalResourceId]' --output table
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::SecurityGroup`].[LogicalResourceId,PhysicalResourceId]' --output table
aws ec2 describe-security-groups --group-ids sg-4288aced345ff2f57 --region us-east-1 --query 'SecurityGroups[0].IpPermissions' --output table
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

## Alchemy v2 (Effect) — answered

16 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local 2>/dev/null | head -20
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ===" && alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>/dev/null; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== Instance details for $stack ===" && alchemy state get --stack "$stack" --stage bench --fqn "WebServer" us-west-1.run.ts --local 2>/dev/null | jq '.'; done
cd /workspace/alchemy && for resource in "LaunchTemplateServer" "PrivateServer"; do echo "=== $resource ===" && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "$resource" us-west-1.run.ts --local 2>/dev/null | jq '.'; done
cd /workspace/alchemy && for resource in "WebSecurityGroup" "WebLaunchTemplate"; do echo "=== $resource ===" && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "$resource" us-west-1.run.ts --local 2>/dev/null | jq '.'; done
cd /workspace/alchemy && aws ec2 describe-security-groups --group-ids sg-default --region us-west-1 2>/dev/null | jq '.SecurityGroups[0].IpPermissions[] | select(.FromPort == 22 or .FromPort == null)' && echo "---" && aws ec2 describe-security-groups --group-ids sg-default --region us-west-2 2>/dev/null | jq '.SecurityGroups[0].IpPermissions[] | select(.FromPort == 22 or .FromPort == null)'
cd /workspace/alchemy && find .alchemy/state -type f -name "*.json" | xargs grep -l "SecurityGroup\|securityGroupIds" | head -20
cd /workspace/alchemy && cat .alchemy/state/alchemy-effect-ec2-multiregion-us-west-1/bench/WebServer.json | jq '.attr.securityGroupIds, .props'
cd /workspace/alchemy && alchemy state resources --stack "alchemy-effect-ec2-multiregion-us-west-1" --stage bench us-west-1.run.ts --local 2>/dev/null | grep -i security
cd /workspace/alchemy && find .alchemy/state -type f -name "*.json" -exec grep -l '"resourceType".*"Instance"' {} \; | while read f; do echo "=== $f ===" && jq '.fqn, .attr | {instanceId, instanceId: .instanceId, publicIpAddress: .publicIpAddress, securityGroupIds: .securityGroupIds}' "$f"; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ===" && find ".alchemy/state/$stack/bench" -type f -name "*.json" -exec jq -r 'select(.resourceType | contains("Instance")) | "\(.fqn): \(.attr.instanceId // "N/A") - Public IP: \(.attr.publicIpAddress // "N/A") - SGs: \(.attr.securityGroupIds | join(","))"' {} \; 2>/dev/null; done
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "DefaultVpcServer" us-west-1.run.ts --local 2>/dev/null | jq '{fqn: .fqn, instanceId: .attr.instanceId, publicIp: .attr.publicIpAddress, securityGroupIds: .attr.securityGroupIds, isExternal: .props.isExternal}'
# … 4 more
```
