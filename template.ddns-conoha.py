#echo --- Domain List ---
#curl --include https://dns-service.tyo1.conoha.io/v1/domains \
#-X GET \
#-H "Accept: application/json" \
#-H "Content-Type: application/json" \
#-H "X-Auth-Token: "

#echo --- Domain IP Update ---
#curl --include https://dns-service.tyo1.conoha.io/v1/domains/<tid>/records/<rid> \
#-X GET \
#-H "Accept: application/json" \
#-H "Content-Type: application/json" \
#-H "X-Auth-Token: "

# update_conoha_dns_record.py
# -*- coding: utf-8 -*-
import json
import requests

### Setting ###
# <APIユーザーのユーザー名>
USERNAME = "xxxx0000000"
# <APIユーザのパスワード>
PASSWORD = "PASSWORD00"
# <API情報に記載されているテナントID>
TENANT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# <Domain名(example.net.)>
TARGET_DOMAIN = "example.net"
# <ターゲットのRecord名(target.example.net.)>)
TARGET_RECORD = "target.example.net."
### Setting END ###

# Get my global IP
print("Global IP : ")
url = "https://ifconfig.me"
r = requests.get(url)
if r.status_code != requests.codes.ok:
    raise Exception("request failed {}".format(r.url))
my_ip = r.text
print(my_ip+"\n")

# Get access_token
print("Get Token : ")
url = "https://identity.tyo1.conoha.io/v2.0/tokens"
payload = {
    "auth": {
        "passwordCredentials": {
            "username": USERNAME,
            "password": PASSWORD,
        },
        "tenantId": TENANT_ID
    }
}
headers = {
    "Accept": "application/json"
}
r = requests.post(url, data=json.dumps(payload), headers=headers)
if r.status_code != requests.codes.ok:
    raise Exception("request failed {}".format(r.url))
resp = r.json()
token_id = resp["access"]["token"]["id"]
print("OK\n")

# Get domain id
print("Domain ID : ")
url = "https://dns-service.tyo1.conoha.io/v1/domains"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Auth-Token": token_id,
}
r = requests.get(url, headers=headers)
if r.status_code != requests.codes.ok:
    raise Exception("request failed {}".format(r.url))
resp = r.json()
domain_id = None
for domain in resp["domains"]:
    if domain["name"] == TARGET_DOMAIN:
        domain_id = domain["id"]
        break
else:
    raise Exception("{} is not found".format(TARGET_DOMAIN))
print("OK\n")

# Get record id
print("Record ID : ")
url = "https://dns-service.tyo1.conoha.io/v1/domains/{domain_id}/records".format(domain_id=domain_id)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Auth-Token": token_id,
}
r = requests.get(url, headers=headers)
if r.status_code != requests.codes.ok:
    raise Exception("request failed {}".format(r.url))
resp = r.json()
record_id = None
for record in resp["records"]:
    if record["name"] == TARGET_RECORD and record["type"] == "A":
        record_id = record["id"]
        break
else:
    raise Exception("{} is not found".format(TARGET_RECORD))
print("OK\n")

# Update record
print("Update Record : ")
url = "https://dns-service.tyo1.conoha.io/v1/domains/{domain_id}/records/{record_id}".format(domain_id=domain_id, record_id=record_id)
payload ={
    "name": TARGET_RECORD,
    "type": "A",
    "data": my_ip,
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Auth-Token": token_id
}
r = requests.put(url, data=json.dumps(payload), headers=headers)
if r.status_code != requests.codes.ok:
    raise Exception("request failed {}".format(r.url))
print("OK\n--- DONE! ---\n")
