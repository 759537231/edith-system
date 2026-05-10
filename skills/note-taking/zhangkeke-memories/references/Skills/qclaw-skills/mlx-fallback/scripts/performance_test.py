#!/usr/bin/env python3
"""
本地模型性能测试脚本
用于测试和评估本地模型的质量、速度和稳定性
"""

import requests
import json
import time
from typing import Dict, List, Optional

LOCAL_API = "http://127.0.0.1:8080/v1/chat/completions"

# 测试任务集
TEST_TASKS = {
    "推理": [
        {
            "id": "reason_1",
            "prompt": "小明比小红大3岁，小红比小华大2岁。如果小华10岁，小明多少岁？",
            "expected": "15",
            "difficulty": "easy"
        },
        {
            "id": "reason_2",
            "prompt": "一个房间里有3盏灯和3个开关。你在房间外，只能进入房间一次。如何确定每个开关控制哪盏灯？",
            "expected_keywords": ["开", "关", "温度", "热"],
            "difficulty": "medium"
        }
    ],
    "创意": [
        {
            "id": "creative_1",
            "prompt": "用一句话描述春天的美景。",
            "expected_keywords": ["花", "绿", "温暖", "春"],
            "difficulty": "easy"
        },
        {
            "id": "creative_2",
            "prompt": "写一个50字以内的科幻故事开头。",
            "expected_keywords": ["星", "未", "时间", "宇宙"],
            "difficulty": "medium"
        }
    ],
    "代码": [
        {
            "id": "code_1",
            "prompt": "用Python写一个函数，计算斐波那契数列的第n项。",
            "expected_keywords": ["def", "fibonacci", "return"],
            "difficulty": "easy"
        }
    ],
    "问答": [
        {
            "id": "qa_1",
            "prompt": "什么是机器学习？用一句话解释。",
            "expected_keywords": ["数据", "学习", "模式"],
            "difficulty": "easy"
        }
    ]
}

# 角色配置
ROLES = ["default", "expert", "teacher", "creative"]


def call_model(prompt: str, role: str = "default", max_tokens: int = 300) -> Dict:
    """
    调用本地模型
    
    Args:
        prompt: 用户提示
        role: 角色类型
        max_tokens: 最大 token 数
        
    Returns:
        包含响应信息的字典
    """
    try:
        start_time = time.time()
        response = requests.post(LOCAL_API, json={
            "model": "local",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "role": role
        }, timeout=60)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            tokens = data['usage']['completion_tokens']
            
            return {
                "success": True,
                "content": content,
                "tokens": tokens,
                "time": elapsed,
                "speed": tokens / elapsed if elapsed > 0 else 0
            }
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def evaluate_response(content: str, expected_keywords: Optional[List[str]] = None, expected: Optional[str] = None) -> float:
    """
    评估响应质量
    
    Args:
        content: 模型响应内容
        expected_keywords: 预期关键词列表
        expected: 预期精确答案
        
    Returns:
        质量评分（0-1）
    """
    if not content:
        return 0
    
    content_lower = content.lower()
    
    # 精确匹配
    if expected and expected.lower() in content_lower:
        return 1.0
    
    # 关键词匹配
    if expected_keywords:
        hits = sum(1 for kw in expected_keywords if kw.lower() in content_lower)
        return hits / len(expected_keywords)
    
    # 长度评分
    length = len(content)
    if length < 10:
        return 0.3
    elif length < 50:
        return 0.7
    elif length < 200:
        return 1.0
    else:
        return 0.8


def run_benchmark() -> Dict:
    """
    运行性能基准测试
    
    Returns:
        测试结果字典
    """
    print("🧪 本地模型性能测试")
    print("=" * 60)
    print("参数: temperature=0.65, top_p=0.85, min_p=0.05")
    print("角色: default, expert, teacher, creative")
    print()
    
    results = {}
    total_score = 0
    total_tasks = 0
    total_time = 0
    total_tokens = 0
    
    for category, tasks in TEST_TASKS.items():
        print(f"\n📝 测试类别: {category}")
        print("-" * 40)
        
        category_scores = []
        category_times = []
        category_speeds = []
        
        for task in tasks:
            print(f"\n任务 {task['id']} ({task['difficulty']}):")
            print(f"  提示: {task['prompt'][:50]}...")
            
            # 测试不同角色
            best_score = 0
            best_role = "default"
            best_response = None
            
            for role in ROLES:
                response = call_model(task['prompt'], role=role)
                
                if response["success"]:
                    score = evaluate_response(
                        response['content'],
                        task.get('expected_keywords'),
                        task.get('expected')
                    )
                    
                    if score > best_score:
                        best_score = score
                        best_role = role
                        best_response = response
            
            if best_response:
                category_scores.append(best_score)
                category_times.append(best_response['time'])
                category_speeds.append(best_response['speed'])
                
                print(f"  ✅ 最佳角色: {best_role}")
                print(f"  🎯 质量: {best_score:.2f}")
                print(f"  ⏱️  耗时: {best_response['time']:.2f}s")
                print(f"  🚀 速度: {best_response['speed']:.1f} tok/s")
                print(f"  📝 响应: {best_response['content'][:100]}...")
                
                total_score += best_score
                total_time += best_response['time']
                total_tokens += best_response['tokens']
            else:
                print(f"  ❌ 失败")
                category_scores.append(0)
            
            total_tasks += 1
        
        # 类别统计
        if category_scores:
            avg_score = sum(category_scores) / len(category_scores)
            avg_time = sum(category_times) / len(category_times) if category_times else 0
            avg_speed = sum(category_speeds) / len(category_speeds) if category_speeds else 0
            
            results[category] = {
                "avg_score": avg_score,
                "avg_time": avg_time,
                "avg_speed": avg_speed,
                "tasks": len(tasks)
            }
            
            print(f"\n  📊 {category} 统计:")
            print(f"    平均质量: {avg_score:.2f}")
            print(f"    平均耗时: {avg_time:.2f}s")
            print(f"    平均速度: {avg_speed:.1f} tok/s")
    
    # 总体统计
    print("\n" + "=" * 60)
    print("📊 总体统计")
    print("=" * 60)
    
    if total_tasks > 0:
        avg_score = total_score / total_tasks
        avg_time = total_time / total_tasks
        avg_speed = total_tokens / total_time if total_time > 0 else 0
        
        print(f"总任务数: {total_tasks}")
        print(f"平均质量: {avg_score:.2f}")
        print(f"平均耗时: {avg_time:.2f}s")
        print(f"平均速度: {avg_speed:.1f} tok/s")
        print(f"总Token数: {total_tokens}")
        print(f"总耗时: {total_time:.2f}s")
        
        # 按类别展示
        print(f"\n📈 各类别表现:")
        for category, stats in results.items():
            print(f"  {category}: 质量={stats['avg_score']:.2f}, 速度={stats['avg_speed']:.1f} tok/s")
    
    return results


def save_results(results: Dict, filename: str = "local_model_test_results.json"):
    """
    保存测试结果
    
    Args:
        results: 测试结果字典
        filename: 保存文件名
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 测试结果已保存到: {filename}")


if __name__ == "__main__":
    results = run_benchmark()
    save_results(results)
