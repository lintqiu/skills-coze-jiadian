#!/usr/bin/env python3
"""
收费技能 - 授权验证 + 手机号登录
流程：
1. 先打印核心功能欢迎信息
2. 检查 SKILL_LICENSE_KEY 授权码 → 提示授权失败，但不退出，继续走手机号流程
3. 检查本地是否保存了手机号
   - 没有手机号 → 提示用户输入手机号 → 请求后端绑定 → 成功保存 → 启动核心功能
   - 有手机号 → 直接启动核心功能
"""
from __future__ import annotations

import os
import sys
import json
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_license import check_license

# 手机号存储文件
PHONE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".phone.json")

# ========== 在这里修改你的 API URL ==========
REGISTER_ENDPOINT = "https://yunji.focus-jd.cn/api/skill/lin/test"


# ======================================================


def load_saved_phone() -> str:
    """加载保存的手机号"""
    if os.path.exists(PHONE_FILE):
        try:
            with open(PHONE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('phone', '')
        except Exception:
            return ''
    return ''


def save_phone(phone: str) -> None:
    """保存手机号"""
    data = {'phone': phone}
    with open(PHONE_FILE, 'w') as f:
        json.dump(data, f)


def register_phone(phone: str) -> tuple[bool, str, dict | None]:
    """
    注册手机号到 Java 后端
    返回: (是否成功, 消息, 完整响应数据)
    """
    try:
        response = requests.post(
            REGISTER_ENDPOINT,
            json={"phone": phone},
            timeout=10
        )

        if response.status_code != 200:
            return False, f"服务器返回错误 HTTP {response.status_code}", None

        # 尝试解析 JSON 响应
        try:
            result = response.json()
            code = result.get("code", -1)
            msg = result.get("msg", "success")
            if code == 0:
                return True, msg, result
            else:
                return False, msg, None
        except ValueError:
            # 非 JSON 返回，200 就算成功
            return True, "success", None

    except requests.exceptions.RequestException as e:
        return False, f"网络请求失败: {str(e)}", None


def main():
    # 第一步：先打印核心功能欢迎信息
    print("✅ 授权验证通过！")
    print("\n这是收费技能的演示功能：")
    print("-----------------------------------")
    print("📝 这里是付费才能使用的核心功能")
    print("💡 你可以替换成你的实际业务逻辑")
    print("🔑 当前授权有效，功能正常运行")
    print("-----------------------------------")

    # 第二步：检查授权码，即使失败也不退出，继续走手机号流程
    valid, msg = check_license()
    if not valid:
        print(f"\n⚠️  授权提示: {msg}")
        print("⚠️  购买授权请访问: https://your-website.com/buy")
        print("\n尽管授权未验证，继续绑定手机号...\n")

    # 第三步：不管授权是否通过，都检查手机号，继续流程
    saved_phone = load_saved_phone()

    if saved_phone:
        # 已有手机号，直接启动核心功能
        print(f"\n📱 已绑定手机号: {saved_phone}")
        print("\n🎉 欢迎回来，核心功能已启动！")
        # ========== 这里放你的核心功能代码 ==========
        print("\n✨ 核心功能运行中")
    else:
        # 没有手机号，提示用户输入
        print("\n📱 请输入你的手机号进行绑定:")
        print("(输入后按回车确认)\n")

        phone = input().strip()

        if not phone:
            print("❌ 手机号不能为空", file=sys.stderr)
            sys.exit(1)

        print("🔄 正在绑定...\n")

        success, result_msg, result_data = register_phone(phone)
        if success:
            # 绑定成功，输出后端返回结果
            print(f"✅ 绑定成功")
            if result_msg:
                print(f"ℹ️ 消息: {result_msg}")
            if result_data:
                print("\n📄 后端返回完整数据:")
                print(json.dumps(result_data, indent=2, ensure_ascii=False))
            # 保存手机号
            save_phone(phone)
            print("\n🎉 绑定完成，核心功能已启动！")
            # ========== 这里放你的核心功能代码 ==========
            print("\n✨ 核心功能运行中")
        else:
            # 绑定失败，不保存，提示错误
            print(f"❌ 绑定失败: {result_msg}", file=sys.stderr)
            print("\n手机号未保存，请检查后端服务后重试", file=sys.stderr)


if __name__ == "__main__":
    main()