# DDos_Prediction_with_ML_ThrtInt

All the infrastructure was created in AWS Cloud Environment.

Wazuh node configuration:

```
module(load="imudp")
input(type="imudp" port="514")

if $fromhost-ip == '<pfSense-IP>' then {
    action(type="omfile" file="/var/log/pfsense.log")
    stop
}
```

Logs forwarding from replicas to pfSense:

```
cat <<EOF | sudo tee /etc/rsyslog.d/50-
replica-logs.conf
*.* @<pfSense-IP>:514
```

This configuration is placed in all replicas.
