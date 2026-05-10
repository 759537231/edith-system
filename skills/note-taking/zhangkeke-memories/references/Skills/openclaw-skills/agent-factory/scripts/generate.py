#!/usr/bin/env python3
"""
Agent 工厂 - 文件生成器
用法：
  python generate.py --name "读书笔记" --type conversation --roles 1
  python generate.py --name "法律咨询" --type consultation --roles 3
"""

import argparse
import os
import sys
import json
from datetime import datetime

SKILL_DIR = os.path.expanduser("~/.openclaw/workspace/skills")
FACTORY_DIR = os.path.join(SKILL_DIR, "agent-factory")
TEMPLATES_DIR = os.path.join(FACTORY_DIR, "templates")


def load_template(tmpl_type: str):
    """加载对应模板"""
    sys.path.insert(0, TEMPLATES_DIR)
    if tmpl_type == "conversation":
        from conversation import generate as gen
        return gen
    elif tmpl_type == "consultation":
        from consultation import generate as gen
        return gen
    elif tmpl_type == "task":
        from task import generate as gen
        return gen
    else:
        raise ValueError(f"未知模板类型: {tmpl_type}")


def load_answers(args) -> dict:
    """从命令行参数构建 answers dict"""
    # 如果有 answers.json，优先读取
    answers_file = os.path.join(FACTORY_DIR, "current_answers.json")
    if os.path.exists(answers_file):
        with open(answers_file) as f:
            return json.load(f)

    # 否则用命令行参数构建
    answers = {
        "name": args.name,
        "trigger": args.trigger or args.name,
        "description": args.description or f"{args.name} Agent",
        "capabilities": args.capabilities or "回答用户问题",
        "workflow": args.workflow or "接收消息 → 理解意图 → 回答 → 记录",
        "output_format": args.output_format or "简洁直接回答",
        "style": args.style or "温暖、专业、有耐心",
        "user_info": args.user_info or "基础信息",
    }
    return answers


def create_directories(skill_name: str) -> str:
    """创建新 Agent 的目录结构"""
    skill_path = os.path.join(SKILL_DIR, skill_name)
    os.makedirs(os.path.join(skill_path, "roles"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "protocols"), exist_ok=True)
    return skill_path


def write_files(skill_path: str, files: dict):
    """将文件写入磁盘"""
    for rel_path, content in files.items():
        full_path = os.path.join(skill_path, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ 创建: {rel_path}")


def main():
    parser = argparse.ArgumentParser(description="Agent 工厂 - 生成新 Skill")
    parser.add_argument("--name", required=True, help="Agent 名称（英文或中文）")
    parser.add_argument("--type", default="conversation",
                        choices=["conversation", "consultation", "task"],
                        help="Agent 类型")
    parser.add_argument("--roles", default="1", help="角色数量（1 或 2+）")
    parser.add_argument("--trigger", help="触发词（默认同名称）")
    parser.add_argument("--description", help="一句话描述")
    parser.add_argument("--capabilities", help="核心能力（用 | 分隔多行）")
    parser.add_argument("--workflow", help="工作流程描述")
    parser.add_argument("--output-format", dest="output_format", help="输出格式")
    parser.add_argument("--style", help="Agent 风格")
    parser.add_argument("--user-info", dest="user_info", help="用户信息说明")
    args = parser.parse_args()

    # 验证名称合法性
    skill_name = args.name.strip()
    for c in skill_name:
        if not ("\u4e00" <= c <= "\u9fff" or c.isalnum() or c in "-_"):
            print(f"❌ 名称包含非法字符: {c}", file=sys.stderr)
            sys.exit(1)

    print(f"\n🔧 正在生成 Agent:「{skill_name}」")
    print(f"   类型: {args.type} | 角色数: {args.roles}")

    try:
        # 1. 加载模板
        gen_func = load_template(args.type)
        print("  ✅ 模板加载完成")

        # 2. 收集参数
        answers = load_answers(args)
        if args.capabilities:
            answers["capabilities"] = args.capabilities.replace("|", "\n")

        # 3. 生成文件
        print("  📄 生成文件...")
        files = gen_func(answers)

        # 4. 创建目录并写入
        skill_path = create_directories(skill_name)
        write_files(skill_path, files)

        print(f"\n✅ Agent「{skill_name}」生成完成！")
        print(f"   位置: {skill_path}")
        print(f"   下一步: python {FACTORY_DIR}/scripts/install.py --name \"{skill_name}\"")

        # 清理临时答案文件
        answers_file = os.path.join(FACTORY_DIR, "current_answers.json")
        if os.path.exists(answers_file):
            os.remove(answers_file)

    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
