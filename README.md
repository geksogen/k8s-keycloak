# k8s-keycloak

## Configure cluster
#### Install Istio
```BASH
curl -L https://istio.io/downloadIstio | sh
cd istio-1.17.2
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
istioctl operator init --tag 1.6.7
kubectl apply -f 
```
#### Install Kiali
```BASH
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.16/samples/addons/kiali.yaml
kubectl patch svc kiali -n istio-system -p '{"spec": {"type": "NodePort"}}'
```




#### Clear resource
```BASH
# Delete istio
cd <istio folder>
export PATH=$PWD/bin:$PATH
istioctl x uninstall --purge
kubectl delete namespace istio-system
'''