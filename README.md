# k8s-keycloak

## Configure cluster
#### Install Istio
```BASH
curl -L https://istio.io/downloadIstio | sh
cd istio-1.17.2
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
istioctl operator init --tag 1.6.7
kubectl apply -f https://raw.githubusercontent.com/geksogen/k8s-keycloak/master/k8s-cluster/istio-operator.yaml
```
#### Install Kiali
```BASH
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.16/samples/addons/kiali.yaml
kubectl patch svc kiali -n istio-system -p '{"spec": {"type": "NodePort"}}'
```

#### Install Keycloak
```BASH
kubectl create -f https://raw.githubusercontent.com/keycloak/keycloak-quickstarts/latest/kubernetes-examples/keycloak.yaml
kubectl patch svc keycloak --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
```
#### Get the Keycloak token for admin rights
```BASH
export TKN=$(curl --location --request POST http://217.28.220.13:32668/realms/master/protocol/openid-connect/token  \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=admin" \
 -d 'password=admin' \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')
```
#### Create the client called “test”
```BASH
curl --location --request POST  http://217.28.220.13:32668/realms/master/clients-registrations/default \
 -H "authorization: Bearer $TKN" \
 -H "Content-Type: application/json" \
 --data \
 '{
    "id": "test",
    "name": "test",
    "redirectUris": ["*"]
 }' 
 # "error":"invalid_token","error_description":"Failed decode token"
```

#### Get the client secret
```BASH
export CLIENT_SECRET=$(curl --insecure  https://keycloak.217.28.220.13.nip.io/auth/admin/realms/master/clients/test/client-secret \
 -H "authorization: Bearer ${TKN}" \
 -H "Content-Type: application/json" | jq -r '.value')
```

#### Clear resource
```BASH
# Delete istio
cd <istio folder>
export PATH=$PWD/bin:$PATH
istioctl x uninstall --purge
kubectl delete namespace istio-system

# Delete keycloak
kubectl delete all -l app=keycloak
'''