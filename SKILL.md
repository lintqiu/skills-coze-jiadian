---
name: skills-coze-jiadian
description: 收费技能示例 - 授权验证 + 手机号绑定
license: MIT
---

# skills-coze-jiadian

收费技能示例，演示如何在 ClawHub 发布带授权验证和手机号绑定的付费技能。

## 隐私说明

本技能会：
1. **收集手机号** - 需要用户输入手机号进行绑定
2. **发送到后端** - 手机号会 POST 到 `https://yunji.focus-jd.cn/api/skill/lin/test`
3. **本地存储** - 绑定成功后，手机号会保存在技能目录下的 `.phone.json` 文件中，方便下次直接使用

使用本技能即表示你同意上述隐私政策。

## 配置

### 必需环境变量

```bash
export SKILL_LICENSE_KEY=你的授权码
```

购买授权码请访问：https://your-website.com/buy

## When to use

- 用户触发付费技能
- 需要授权验证 + 手机号绑定
- 授权通过后保存手机号，下次直接使用

## Instructions

1. 用户触发技能
2. 打印欢迎信息
3. 检查 `SKILL_LICENSE_KEY` 授权 → 提示购买，不阻止手机号绑定
4. 检查本地是否已有手机号 → 有直接使用，没有提示输入
5. 发送手机号到后端 → 成功保存，失败提示

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 否 | 测试消息 |
