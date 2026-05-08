import urllib.request
import json
import sys

BASE_URL = 'http://127.0.0.1:8000'

def make_request(method, url, data=None, headers=None):
    """发送 HTTP 请求"""
    try:
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read().decode())
        return resp.status, result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP {e.code}: {error_body}")
        return e.code, json.loads(error_body) if error_body else None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None, None

def test_all():
    print("=" * 60)
    print("流俗地 API 全面测试")
    print("=" * 60)
    
    # 1. 测试注册
    print("\n[1/10] 测试用户注册...")
    status, result = make_request('POST', f'{BASE_URL}/users/register', {
        'account': 'testuser002',
        'password': '123456',
        'nickname': '测试用户2号'
    })
    if status == 200:
        print(f"✅ 注册成功 - 用户ID: {result['id']}")
    elif status == 400:
        print(f"⚠️ 用户已存在，跳过")
    else:
        print("❌ 注册失败")
        return
    
    # 2. 测试登录
    print("\n[2/10] 测试用户登录...")
    status, result = make_request('POST', f'{BASE_URL}/users/login', {
        'account': 'testuser002',
        'password': '123456'
    })
    if status == 200:
        token = result['access_token']
        print(f"✅ 登录成功 - Token: {token[:30]}...")
        auth_headers = {'Authorization': f'Bearer {token}'}
    else:
        print("❌ 登录失败")
        return
    
    # 3. 测试获取当前用户信息
    print("\n[3/10] 测试获取用户信息...")
    status, result = make_request('GET', f'{BASE_URL}/users/me', headers=auth_headers)
    if status == 200:
        print(f"✅ 获取用户信息成功 - 昵称: {result['nickname']}")
    else:
        print("❌ 获取用户信息失败")
    
    # 4. 测试创建作品
    print("\n[4/10] 测试创建作品...")
    status, result = make_request('POST', f'{BASE_URL}/works/', {
        'title': '测试作品',
        'content': '这是测试作品的内容',
        'status': 1
    }, auth_headers)
    if status == 200:
        work_id = result['id']
        print(f"✅ 创建作品成功 - 作品ID: {work_id}")
    else:
        print("❌ 创建作品失败")
        return
    
    # 5. 测试获取作品列表
    print("\n[5/10] 测试获取作品列表...")
    status, result = make_request('GET', f'{BASE_URL}/works/')
    if status == 200:
        print(f"✅ 获取作品列表成功 - 作品数量: {len(result)}")
    else:
        print("❌ 获取作品列表失败")
    
    # 6. 测试获取作品详情
    print("\n[6/10] 测试获取作品详情...")
    status, result = make_request('GET', f'{BASE_URL}/works/{work_id}')
    if status == 200:
        print(f"✅ 获取作品详情成功 - 标题: {result['title']}")
    else:
        print("❌ 获取作品详情失败")
    
    # 7. 测试点赞作品
    print("\n[7/10] 测试点赞作品...")
    status, result = make_request('POST', f'{BASE_URL}/works/{work_id}/like', headers=auth_headers)
    if status == 200:
        print(f"✅ 点赞成功 - 点赞数: {result['count']}")
    else:
        print("❌ 点赞失败")
    
    # 8. 测试评论作品
    print("\n[8/10] 测试评论作品...")
    status, result = make_request('POST', f'{BASE_URL}/works/{work_id}/comments', {
        'content': '这是一条测试评论'
    }, auth_headers)
    if status == 200:
        print("✅ 评论成功")
    else:
        print("❌ 评论失败")
    
    # 9. 测试获取通知
    print("\n[9/10] 测试获取通知...")
    status, result = make_request('GET', f'{BASE_URL}/notifications/', headers=auth_headers)
    if status == 200:
        print(f"✅ 获取通知成功 - 通知数量: {len(result)}")
    else:
        print("❌ 获取通知失败")
    
    # 10. 测试创建论坛帖子
    print("\n[10/10] 测试创建论坛帖子...")
    status, result = make_request('POST', f'{BASE_URL}/forum/posts', {
        'title': '测试帖子',
        'content': '这是测试帖子的内容'
    }, auth_headers)
    if status == 200:
        print(f"✅ 创建论坛帖子成功 - 帖子ID: {result['id']}")
    else:
        print("❌ 创建论坛帖子失败")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == '__main__':
    test_all()
