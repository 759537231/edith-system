#!/usr/bin/env python3
"""
Agent 工厂 - 安装器
将生成的 Skill 自动安装到 OpenClaw

用法：python install.py --name "读书笔记"
"""

import argparse
import os
import sys
import json
import shutil
import subprocess

SKILL_DIR = os.path.expanduser("~/.openclaw/workspace/skills")
FACTORY_DIR = os.path.join(SKILL_DIR, "agent-factory")


def validate_skill(skill_path: str, skill_name: str) -> dict:
    """验证 Skill 文件完整性"""
    issues = []
    warnings = []

    # 必须有 SKILL.md
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        issues.append("缺少 SKILL.md 文件")

    # 检查目录结构
    required_dirs = ["roles"]
    for d in required_dirs:
        if not os.path.exists(os.path.join(skill_path, d)):
            warnings.append(f"缺少 {d}/ 目录")

    # 尝试读取 SKILL.md 验证格式
    if os.path.exists(skill_md):
        try:
            with open(skill_md, encoding="utf-8") as f:
                content = f.read()
                if "# " not in content:
                    issues.append("SKILL.md 缺少标题")
                if "触发词" not in content and "触发" not in content:
                    warnings.append("SKILL.md 未定义触发词")
        except Exception as e:
            issues.append(f"读取 SKILL.md 失败: {e}")

    # 统计信息
    stats = {"files": 0, "roles": 0, "size_kb": 0}
    for root, dirs, files in os.walk(skill_path):
        # 排除 __pycache__
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith(".pyc"):
                continue
            fp = os.path.join(root, f)
            stats["files"] += 1
            stats["size_kb"] += os.path.getsize(fp) / 1024
            if "roles" in fp:
                stats["roles"] += 1

    return {"valid": len(issues) == 0, "issues": issues, "warnings": warnings, "stats": stats}


def main():
    parser = argparse.ArgumentParser(description="Agent 工厂 - 安装 Skill")
    parser.add_argument("--name", required=True, help="要安装的 Agent 名称")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true",
                        help="仅验证，不安装")
    args = parser.parse_args()

    skill_name = args.name.strip()
    skill_path = os.path.join(SKILL_DIR, skill_name)

    print(f"\n🔍 检查 Agent:「{skill_name}」")

    if not os.path.exists(skill_path):
        print(f"❌ 找不到 Skill：{skill_path}")
        print(f"   请先运行: python generate.py --name \"{skill_name}\" --type conversation")
        sys.exit(1)

    # 验证
    result = validate_skill(skill_path, skill_name)
    print(f"   文件数: {result['stats']['files']} | "
          f"角色卡: {result['stats']['roles']} | "
          f"大小: {result['stats']['size_kb']:.1f} KB")

    for w in result["warnings"]:
        print(f"   ⚠️ {w}")

    if not result["valid"]:
        for i in result["issues"]:
            print(f"   ❌ {i}")
        sys.exit(1)

    if args.dry_run:
        print("   ✅ 验证通过（dry-run 模式，未安装）")
        sys.exit(0)

    # 生成 manifest（让 QClaw 能识别）
    manifest_path = os.path.join(skill_path, ".manifest.json")
    manifest = {
        "name": skill_name,
        "version": "0.1.0",
        "installed_at": subprocess.run(
            ["date", "+%Y-%m-%dT%H:%M:%S%z"], capture_output=True, text=True
        ).stdout.strip(),
        "installed_by": "agent-factory",
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 记录到安装清单
    registry_path = os.path.join(SKILL_DIR, ".factory_registry.json")
    registry = {}
    if os.path.exists(registry_path):
        with open(registry_path) as f:
            registry = json.load(f)

    registry[skill_name] = manifest
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 安装完成！Agent「{skill_name}」已就绪")
    print(f"   📂 位置: {skill_path}")
    print(f"   💡 在 QClaw 中搜索「{skill_name}」即可启用")


if __name__ == "__main__":
    main()
