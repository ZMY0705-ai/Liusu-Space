import urllib.request
import json

# 测试注册接口
url = 'http://127.0.0.1:8000/users/register'
data = {
    'account': 'testuser001',
    'password': '123456',
    'nickname': '测试用户'
}

try:
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode(), 
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print(f'✅ 注册成功！')
    print(f'状态码: {resp.status}')
    print(f'用户ID: {result["id"]}')
    print(f'账号: {result["account"]}')
    print(f'昵称: {result["nickname"]}')
except Exception as e:
    print(f'❌ 注册失败: {e}')
