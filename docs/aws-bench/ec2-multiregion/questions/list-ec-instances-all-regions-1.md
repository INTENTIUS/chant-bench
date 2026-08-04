# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

4 commands, from `chant-p3`.

```sh
cd /workspace/chant && chant lifecycle show floci 2>&1 | head -50
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:region=us-west-1 attr:region=us-west-2 attr:internetFacing=true" --at latest --env floci --show PrivateIpAddress,PublicIpAddress,effectiveIngress,region --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show PrivateIpAddress,PublicIpAddress,effectiveIngress,region,internetFacing --explain 2>&1 | grep -A 200 "LOGICAL ID"
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show PrivateIpAddress,PublicIpAddress,effectiveIngress,region,internetFacing --explain
```

## No tool (AWS CLI) — missed

5 commands, from `bare-g3`.

```sh
# Get all EC2 instances across the three regions with their security groups for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" >&2 aws ec2 describe-instances \ --region "$region" \ --output json \ --query 'Reservations[].Instances[].{InstanceId:InstanceId,InstanceType:InstanceType,State:State.Name,PublicIpAddress:PublicIpAddress,LaunchTemplate:LaunchTemplate,SecurityGroups:SecurityGroups[].GroupId}' | \ jq -r ".[] | @json" | while read line; do echo "$region|$line" done done > /tmp/instances.jsonl cat /tmp/instances.jsonl
# Get unique security groups from instances declare -A sg_regions while IFS='|' read -r region json_line; do sg_list=$(echo "$json_line" | jq -r '.SecurityGroups[]?' 2>/dev/null) while read -r sg; do [ -n "$sg" ] && sg_regions["$sg"]="$region" done <<< "$sg_list" done < /tmp/instances.jsonl # Also check for launch templates and their security groups for region in us-east-1 us-west-1 us-west-2; do aws ec2 describe-launch-templates --region "$region" --output json 2>/dev/null | \ jq -r '.LaunchTemplates[]? | "\(.LaunchTemplateName) \(.LaunchTemplateId)"' | while read name id; do if [ -n "$id" ]; then aws ec2 describe-launch-template-versions \ --region "$region" \ --launch-template-id "$id" \ --output json 2>/dev/null | \ jq -r '.LaunchTemplateVersions[]? | .LaunchTemplateData.SecurityGroupIds[]?' | \ while read sg; do [ -n "$sg" ] && sg_regions["$sg"]="$region" done fi done done # Get all unique security groups and their regions echo "Checking security groups for SSH access from internet..." declare -A ssh_exposed for sg_region in "${!sg_regions[@]}"; do region="${sg_regions[$sg_region]}" aws ec2 describe-security-groups \ --region "$region" \ --group-ids "$sg_region" \ --output json 2>/dev/null | \ jq -r ".SecurityGroups[] | {GroupId: .GroupId, GroupName: .GroupName, Region: \"$region\", Rules: [.IpPermissions[] | select(.FromPort == 22 or .FromPort == null or ((.FromPort | tonumber) <= 22 and (.ToPort | tonumber) >= 22)) | {FromPort: .FromPort, ToPort: .ToPort, IpRanges: [.IpRanges[] | select(.CidrIp == \"0.0.0.0/0\") | .CidrIp]}]}" | \ jq -r "@json" > /tmp/sg_rules_${region}.jsonl 2>/dev/null done # Combine all results cat /tmp/sg_rules_*.jsonl 2>/dev/null | sort -u
# Parse instances and identify which are using the exposed security group exposed_sg="sg-3e992d174410193e1" echo "Instances reachable via SSH from the internet:" echo "================================================" echo "" while IFS='|' read -r region json_line; do instance_id=$(echo "$json_line" | jq -r '.InstanceId') public_ip=$(echo "$json_line" | jq -r '.PublicIpAddress // empty') state=$(echo "$json_line" | jq -r '.State') instance_type=$(echo "$json_line" | jq -r '.InstanceType') sg_list=$(echo "$json_line" | jq -r '.SecurityGroups[]?') # Check if this instance uses the exposed security group if echo "$sg_list" | grep -q "$exposed_sg"; then if [ -n "$public_ip" ] && [ "$state" = "running" ]; then echo "Instance ID: $instance_id" echo "Region: $region" echo "Public IP: $public_ip" echo "Instance Type: $instance_type" echo "Security Group: $exposed_sg (allows SSH from 0.0.0.0/0)" echo "State: $state" echo "" fi fi done < /tmp/instances.jsonl # Also check for any instances with default security group that might allow SSH echo "" echo "Checking default security groups for SSH rules..." echo "================================================" for region in us-east-1 us-west-1 us-west-2; do aws ec2 describe-security-groups \ --region "$region" \ --filters "Name=group-name,Values=default" \ --output json 2>/dev/null | \ jq -r '.SecurityGroups[] | select(.IpPermissions[] | select(.FromPort == 22 and (.IpRanges[] | select(.CidrIp == "0.0.0.0/0") | .CidrIp))) | {GroupId: .GroupId, Region: "'$region'"}' > /tmp/default_sg_ssh_${region}.json 2>/dev/null done cat /tmp/default_sg_ssh_*.json 2>/dev/null | jq -s 'if length > 0 then . else [] end'
# Comprehensive check: gather ALL security groups in use and their complete rules echo "Complete security group analysis..." echo "" for region in us-east-1 us-west-1 us-west-2; do echo "Region: $region" # Get all security groups aws ec2 describe-security-groups \ --region "$region" \ --output json 2>/dev/null | \ jq -r '.SecurityGroups[] | select(.IpPermissions | length > 0) | select(.IpPermissions[] | select( (.FromPort == 22 or .ToPort == 22 or ((.FromPort | tonumber? // 0) <= 22 and (.ToPort | tonumber? // 65535) >= 22)) and (.IpRanges[]? | select(.CidrIp == "0.0.0.0/0")) and .IpProtocol == "tcp" )) | {GroupId, GroupName, Rules: [.IpPermissions[] | select(.IpRanges[] | select(.CidrIp == "0.0.0.0/0")) | {FromPort, ToPort, Protocol: .IpProtocol}]}' > /tmp/ssh_sgs_${region}.json 2>/dev/null if [ -s /tmp/ssh_sgs_${region}.json ]; then cat /tmp/ssh_sgs_${region}.json | jq -r 'if type == "object" then "\(.GroupId) (\(.GroupName)): Port 22 SSH allowed from 0.0.0.0/0" else empty end' fi done echo "" echo "Final list of instances reachable via SSH from internet:" echo "========================================================" # Create comprehensive instance list with all their security groups for region in us-east-1 us-west-1 us-west-2; do aws ec2 describe-instances \ --region "$region" \ --filters "Name=instance-state-name,Values=running" \ --output json 2>/dev/null | \ jq -r '.Reservations[].Instances[] | select(.PublicIpAddress != null) | { InstanceId, PublicIpAddress, Region: "'$region'", InstanceType, SecurityGroups: [.SecurityGroups[].GroupId], LaunchTemplate: (.LaunchTemplate.LaunchTemplateId // "none") } | @json' > /tmp/running_instances_${region}.jsonl 2>/dev/null done # Check which running instances with public IPs use exposed security groups exposed_sgs=$(cat /tmp/ssh_sgs_*.json 2>/dev/null | jq -r '.GroupId' | sort -u) if [ -n "$exposed_sgs" ]; then cat /tmp/running_instances_*.jsonl 2>/dev/null | while read line; do instance=$(echo "$line" | jq .) instance_id=$(echo "$instance" | jq -r '.InstanceId') public_ip=$(echo "$instance" | jq -r '.PublicIpAddress') region=$(echo "$instance" | jq -r '.Region') instance_type=$(echo "$instance" | jq -r '.InstanceType') sgs=$(echo "$instance" | jq -r '.SecurityGroups[]?') # Check if any of this instance's security groups is in the exposed list for sg in $sgs; do if echo "$exposed_sgs" | grep -q "^$sg$"; then echo "✗ $instance_id | $public_ip | $region | $instance_type | $sg" break fi done done else echo "No security groups found allowing SSH from 0.0.0.0/0" fi
# Get detailed info about the exposed instance region="us-east-1" instance_id="i-ce170d8eeade8435a" sg_id="sg-3e992d174410193e1" echo "Detailed information about exposed instance:" echo "" aws ec2 describe-instances \ --region "$region" \ --instance-ids "$instance_id" \ --output json 2>/dev/null | \ jq '.Reservations[].Instances[] | { InstanceId, InstanceType, PublicIpAddress, PrivateIpAddress, LaunchTime: .LaunchTime, State: .State.Name, VpcId, SubnetId, SecurityGroups: [.SecurityGroups[] | {GroupId, GroupName}], Tags: (.Tags | map({Key, Value}) | from_entries) }' echo "" echo "Security Group Rules:" echo "" aws ec2 describe-security-groups \ --region "$region" \ --group-ids "$sg_id" \ --output json 2>/dev/null | \ jq '.SecurityGroups[] | { GroupId, GroupName, Description, IngressRules: [.IpPermissions[] | select(.FromPort == 22 or ((.FromPort | tonumber? // 0) <= 22 and (.ToPort | tonumber? // 65535) >= 22)) | { Protocol: .IpProtocol, FromPort, ToPort, IpRanges: [.IpRanges[].CidrIp], Ipv6Ranges: [.Ipv6Ranges[].CidrIpv6] }] }'
```

## Terraform — answered

18 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq . > /tmp/state.json && echo "State JSON saved"
cd /workspace/terraform && jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, values: .values}' /tmp/state.json | head -200
jq '.values.root_module.resources | length' /tmp/state.json
jq '.values.root_module.resources[] | {type, address}' /tmp/state.json
jq '.values.root_module.child_modules | length' /tmp/state.json
jq '.values.root_module.child_modules[] | {address: .address, resource_count: (.resources | length)}' /tmp/state.json
jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_instance") | {address, id: .values.id, region: .values.availability_zone}' /tmp/state.json
jq '.values.root_module.child_modules[] | select(.address == "module.west1" or .address == "module.west2") | {module: .address, instances: [.resources[] | select(.type == "aws_instance") | {address, id: .values.id, region: .values.availability_zone}]}' /tmp/state.json
jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_instance") | {address, id: .values.id, region: .values.availability_zone, vpc_security_group_ids: .values.vpc_security_group_ids}' /tmp/state.json
jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_security_group" or .type == "aws_security_group_rule") | {address, type, id: .values.id, name: .values.name}' /tmp/state.json | head -50
jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_security_group") | {address, id: .values.id, name: .values.name, ingress: .values.ingress, egress: .values.egress}' /tmp/state.json
jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_launch_template") | {address, id: .values.id, vpc_security_group_ids: .values.vpc_security_group_ids}' /tmp/state.json
# … 6 more
```

## Pulumi — answered

11 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && cat /tmp/pulumi-state.json | jq '.deployment.resources | length'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone, instanceId: .outputs.id}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], instanceId: .outputs.id, securityGroups: .outputs.securityGroups, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds, launchTemplate: .outputs.launchTemplate}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | {id: .outputs.id, name: .outputs.name, ingress: .outputs.ingress}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.outputs.id == "sg-default") | {id: .outputs.id, name: .outputs.name, ingress: .outputs.ingress}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | .outputs.id'
cd /workspace/pulumi && cat > /tmp/analyze.jq << 'EOF' # Get all EC2 instances with their details .deployment.resources[] as $res | select($res.type == "aws:ec2/instance:Instance") | { name: ($res.urn | split("::")[-1]), instanceId: $res.outputs.id, region: ($res.outputs.availabilityZone | split("")[:9] | join("")), subnetId: $res.outputs.subnetId, vpcSecurityGroupIds: $res.outputs.vpcSecurityGroupIds, launchTemplateId: (if $res.outputs.launchTemplate then $res.outputs.launchTemplate.id else null end), launchTemplateVersion: (if $res.outputs.launchTemplate then $res.outputs.launchTemplate.version else null end) } EOF jq -f /tmp/analyze.jq /tmp/pulumi-state.json
cd /workspace/pulumi && cat > /tmp/sg_ssh_rules.jq << 'EOF' # Get security groups and filter for those with SSH access from 0.0.0.0/0 .deployment.resources[] as $res | select($res.type == "aws:ec2/securityGroup:SecurityGroup") | { id: $res.outputs.id, name: $res.outputs.name, vpcId: $res.outputs.vpcId, hasSshFromInternet: ( $res.outputs.ingress | map(select(.fromPort == 22 and (.cidrBlocks | map(select(. == "0.0.0.0/0")) | length > 0))) | length > 0 ), sshRules: ( $res.outputs.ingress | map(select(.fromPort == 22)) ) } EOF jq -f /tmp/sg_ssh_rules.jq /tmp/pulumi-state.json
cd /workspace/pulumi && cat > /tmp/subnet_routes.jq << 'EOF' # Get subnets and their internet connectivity .deployment.resources[] as $res | select($res.type == "aws:ec2/subnet:Subnet") | { id: $res.outputs.id, vpcId: $res.outputs.vpcId, cidrBlock: $res.outputs.cidrBlock, mapPublicIpOnLaunch: $res.outputs.mapPublicIpOnLaunch, tags: $res.outputs.tags } EOF jq -f /tmp/subnet_routes.jq /tmp/pulumi-state.json
cd /workspace/pulumi && cat > /tmp/routes.jq << 'EOF' # Get route tables and their routes .deployment.resources[] as $res | select($res.type == "aws:ec2/route:Route") | { destinationCidrBlock: $res.outputs.destinationCidrBlock, gatewayId: $res.outputs.gatewayId, routeTableId: $res.outputs.routeTableId } EOF jq -f /tmp/routes.jq /tmp/pulumi-state.json
cd /workspace/pulumi && cat > /tmp/rt_assoc.jq << 'EOF' # Get route table associations .deployment.resources[] as $res | select($res.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | { subnetId: $res.outputs.subnetId, routeTableId: $res.outputs.routeTableId } EOF jq -f /tmp/rt_assoc.jq /tmp/pulumi-state.json
```

## AWS CDK — answered

21 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | keys | .[]' | head -20
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | contains("Instance") or contains("SecurityGroup")) | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources[] | select(.Type == "AWS::EC2::LaunchTemplate")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, instanceType: .value.Properties.InstanceType, securityGroups: .value.Properties.SecurityGroupIds, subnet: .value.Properties.SubnetId}' | jq -s '.'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources[] | select(.Type == "AWS::EC2::SecurityGroup") | {logicalId: .logicalId, GroupDescription: .Properties.GroupDescription, SecurityGroupIngress: .Properties.SecurityGroupIngress}' | jq -s 'map(select(.SecurityGroupIngress) | select(.SecurityGroupIngress | any(.FromPort == 22)))'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroup") | {logicalId: .key, description: .value.Properties.GroupDescription, ingress: .value.Properties.SecurityGroupIngress}' | jq -s 'map(select(.ingress) | select(.ingress | any(.FromPort == 22)))'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, securityGroups: .value.Properties.SecurityGroupIds, subnet: .value.Properties.SubnetId}' | jq -s 'length, .[0:3]'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroup") | {logicalId: .key, description: .value.Properties.GroupDescription, ingress: .value.Properties.SecurityGroupIngress}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, securityGroups: .value.Properties.SecurityGroupIds} | jq -s 'length, .[0:3]'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, securityGroups: .value.Properties.SecurityGroupIds}' | jq -s '.'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroup") | {logicalId: .key, description: .value.Properties.GroupDescription, ingress: .value.Properties.SecurityGroupIngress}'
# … 9 more
```

## Alchemy — answered

20 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list | head -30
cd /workspace/alchemy && alchemy state tree
cd /workspace/alchemy && alchemy state list | grep -E "instance|ltServer|Server" | grep -v "exp-"
cd /workspace/alchemy && alchemy state list | grep -E "usw1-server|usw2-server"
cd /workspace/alchemy && for instance in defaultVpcServer instance ltServer privateServer webServer usw1-server usw2-server; do echo "=== $instance ==="; alchemy state get "alchemy-ec2-multiregion/bench/$instance"; done
cd /workspace/alchemy && alchemy state list | grep -E "SecurityGroup|web-ssh" | head -20
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/web-ssh"
cd /workspace/alchemy && alchemy state list | grep -i "launch"
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l "lt-67ed2e3464ca35ddb" 2>/dev/null
cd /workspace/alchemy && alchemy state list | grep -i "rule\|ssh\|http" | head -30
cd /workspace/alchemy && for rule in web-http web-https; do echo "=== $rule ==="; alchemy state get "alchemy-ec2-multiregion/bench/$rule"; done
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l "SecurityGroupRule" 2>/dev/null
# … 8 more
```

## Alchemy v2 (Effect) — answered

16 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== Stack: $stack ===" alchemy state resources --stack "$stack" --stage prod us-west-1.run.ts --local 2>/dev/null | grep -i instance || true done
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== Stack: $stack ===" alchemy state stages --stack "$stack" us-west-1.run.ts --local 2>/dev/null done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== Stack: $stack ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>/dev/null | head -50 done
cd /workspace/alchemy && for region_info in "us-east-1:alchemy-effect-ec2-multiregion-us-east-1" "us-west-1:alchemy-effect-ec2-multiregion-us-west-1" "us-west-2:alchemy-effect-ec2-multiregion-us-west-2"; do IFS=':' read -r region stack <<< "$region_info" echo "=== Region: $region ===" for instance in DefaultVpcServer PrivateServer LaunchTemplateServer WebServer; do alchemy state get --stack "$stack" --stage bench --fqn "$instance" us-west-1.run.ts --local 2>/dev/null | jq . 2>/dev/null | head -100 && echo "---" || true done done
cd /workspace/alchemy && for region_info in "us-east-1:alchemy-effect-ec2-multiregion-us-east-1" "us-west-1:alchemy-effect-ec2-multiregion-us-west-1" "us-west-2:alchemy-effect-ec2-multiregion-us-west-2"; do IFS=':' read -r region stack <<< "$region_info" echo "=== Region: $region - Security Groups ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>/dev/null | grep -i "securitygroup\|group" done
find /workspace/alchemy/.alchemy/state -name "*.json" -type f | head -20
find /workspace/alchemy/.alchemy/state -name "*SecurityGroup*.json" -o -name "*Group*.json" | sort
find /workspace/alchemy/.alchemy/state -type f -name "*.json" | xargs grep -l '"sg-default"' 2>/dev/null | head -5
find /workspace/alchemy/.alchemy/state -type f -name "*.json" | xargs grep -l '"sg-default"' | xargs grep -l '"resourceType".*SecurityGroup'
find /workspace/alchemy/.alchemy/state -type f -name "*.json" -exec grep -l "resourceType.*SecurityGroup" {} \;
# … 4 more
```
