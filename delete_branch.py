import requests

# 定义 API URL 和访问令牌
branch_api_url = "https://gcode.uniview.com/api/v4/projects/27/repository/branches"
delete_branch_api_url = "https://gcode.uniview.com/api/v4/projects/27/repository/branches/"
search_query = "cherry-pick"
access_token = "8Fq_u8axpkZu5iG3XRhk"

# 发起 GET 请求来获取分支信息，并解析返回的数据以获取分支名称
response = requests.get(branch_api_url, params={"search": search_query}, headers={"PRIVATE-TOKEN": access_token}, verify=False)

# 检查请求是否成功
if response.status_code == 200:
    branches_data = response.json()
    # 解析返回的数据以获取分支名称
    branch_names = [branch["name"] for branch in branches_data]

    # 批量删除分支
    for branch_name in branch_names:
        delete_response = requests.delete(delete_branch_api_url + branch_name, headers={"PRIVATE-TOKEN": access_token}, verify=False)
        if delete_response.status_code == 204:
            print(f"分支 {branch_name} 删除成功")
        else:
            print(f"分支 {branch_name} 删除失败: {delete_response.text}")
else:
    print(f"请求失败: {response.status_code}")
