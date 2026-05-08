"""
测试无限嵌套评论功能
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_nested_comments():
    print("=" * 60)
    print("测试无限嵌套评论功能")
    print("=" * 60)
    
    # 1. 登录获取token
    print("\n1. 登录获取token...")
    login_response = requests.post(f"{BASE_URL}/users/login", json={
        "account": "testuser001",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ 登录成功")
    
    # 2. 获取一个作品ID
    print("\n2. 获取作品列表...")
    works_response = requests.get(f"{BASE_URL}/works/", params={"skip": 0, "limit": 1})
    if works_response.status_code != 200 or not works_response.json():
        print("❌ 获取作品失败，请先创建作品")
        return
    
    work_id = works_response.json()[0]["id"]
    print(f"✅ 使用作品ID: {work_id}")
    
    # 3. 发表一级评论
    print("\n3. 发表一级评论...")
    comment1_response = requests.post(
        f"{BASE_URL}/works/{work_id}/comments",
        json={"content": "这是一级评论", "parent_id": None},
        headers=headers
    )
    
    if comment1_response.status_code != 200:
        print(f"❌ 发表一级评论失败: {comment1_response.text}")
        return
    
    comment1_id = comment1_response.json()["comment_id"]
    print(f"✅ 一级评论发表成功，ID: {comment1_id}")
    
    # 4. 回复一级评论（二级评论）
    print("\n4. 回复一级评论（二级评论）...")
    comment2_response = requests.post(
        f"{BASE_URL}/works/{work_id}/comments",
        json={"content": "这是对一级评论的回复", "parent_id": comment1_id},
        headers=headers
    )
    
    if comment2_response.status_code != 200:
        print(f"❌ 发表二级评论失败: {comment2_response.text}")
        return
    
    comment2_id = comment2_response.json()["comment_id"]
    print(f"✅ 二级评论发表成功，ID: {comment2_id}")
    
    # 5. 回复二级评论（三级评论）
    print("\n5. 回复二级评论（三级评论）...")
    comment3_response = requests.post(
        f"{BASE_URL}/works/{work_id}/comments",
        json={"content": "这是对二级评论的回复", "parent_id": comment2_id},
        headers=headers
    )
    
    if comment3_response.status_code != 200:
        print(f"❌ 发表三级评论失败: {comment3_response.text}")
        return
    
    comment3_id = comment3_response.json()["comment_id"]
    print(f"✅ 三级评论发表成功，ID: {comment3_id}")
    
    # 6. 获取评论列表（树形结构）
    print("\n6. 获取评论列表（树形结构）...")
    comments_response = requests.get(f"{BASE_URL}/works/{work_id}/comments")
    
    if comments_response.status_code != 200:
        print(f"❌ 获取评论列表失败: {comments_response.text}")
        return
    
    comments = comments_response.json()
    print(f"✅ 获取到 {len(comments)} 条顶级评论")
    
    # 7. 打印评论树
    print("\n7. 评论树结构:")
    def print_comment_tree(comments, level=0):
        for comment in comments:
            indent = "  " * level
            author = comment["user"]["nickname"] if comment["user"] else "匿名"
            print(f"{indent}- [{author}] {comment['content']} (ID: {comment['id']}, Parent: {comment['parent_id']})")
            if comment["replies"]:
                print(f"{indent}  └─ {len(comment['replies'])} 条回复")
                print_comment_tree(comment["replies"], level + 1)
    
    print_comment_tree(comments)
    
    # 8. 验证树形结构
    print("\n8. 验证树形结构...")
    if len(comments) > 0:
        first_comment = comments[0]
        if first_comment["id"] == comment1_id:
            print("✅ 一级评论正确")
            
            if len(first_comment["replies"]) > 0:
                second_comment = first_comment["replies"][0]
                if second_comment["id"] == comment2_id:
                    print("✅ 二级评论正确")
                    
                    if len(second_comment["replies"]) > 0:
                        third_comment = second_comment["replies"][0]
                        if third_comment["id"] == comment3_id:
                            print("✅ 三级评论正确")
                            print("\n🎉 所有测试通过！无限嵌套评论功能正常工作！")
                        else:
                            print("❌ 三级评论不匹配")
                    else:
                        print("❌ 二级评论没有回复")
                else:
                    print("❌ 二级评论不匹配")
            else:
                print("❌ 一级评论没有回复")
        else:
            print("❌ 一级评论不匹配")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_nested_comments()
