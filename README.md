# DDoS_Prediction_with_ML_ThrtInt

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

The code of the training and prediction part is also placed in our cloud infrastructure and it is used in real time to be adapted with the new logs that come towards our environment.

The dataset used was renamed in this repo.
