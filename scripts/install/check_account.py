#!/usr/bin/env python3
"""
检查 OpenAI 账户状态和余额
"""

import os
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

console = Console()

def check_account():
    """检查账户信息"""
    console.print("\n[bold cyan]🔍 检查 OpenAI 账户状态...[/bold cyan]\n")
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        console.print("[red]❌ 未找到 API 密钥[/red]")
        return
    
    console.print(f"[dim]使用密钥: {api_key[:7]}...{api_key[-4:]}[/dim]\n")
    
    # OpenAI API 基础 URL
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 尝试简单的模型列表调用来检查 API 状态
    console.print("[cyan]📡 测试 API 连接...[/cyan]")
    
    try:
        # 测试调用
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            console.print("[green]✅ API 密钥有效，连接成功[/green]\n")
            
            # 显示可用模型
            models = response.json()
            console.print(f"[green]✅ 可访问 {len(models.get('data', []))} 个模型[/green]\n")
            
            # 列出主要模型
            table = Table(title="可用的主要模型")
            table.add_column("模型 ID", style="cyan")
            table.add_column("推荐程度", style="green")
            
            model_recommendations = {
                "gpt-3.5-turbo": "⭐⭐⭐⭐⭐ 推荐（便宜快速）",
                "gpt-4o": "⭐⭐⭐⭐ 推荐（性能好）",
                "gpt-4-turbo": "⭐⭐⭐ 较贵",
                "gpt-4": "⭐⭐ 最贵但能力强",
            }
            
            available_models = [m['id'] for m in models.get('data', [])]
            
            for model, rec in model_recommendations.items():
                if any(model in m for m in available_models):
                    table.add_row(model, rec)
            
            console.print(table)
            console.print()
            
        elif response.status_code == 401:
            console.print("[red]❌ API 密钥无效[/red]")
            console.print("[yellow]请检查 .env 文件中的 OPENAI_API_KEY[/yellow]\n")
            return
            
        elif response.status_code == 429:
            console.print("[red]❌ 配额不足（错误 429）[/red]\n")
            
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', '')
            
            console.print(Panel.fit(
                "[bold red]账户额度已用完[/bold red]\n\n"
                f"错误信息:\n{error_msg}\n\n"
                "[bold]需要充值才能继续使用[/bold]",
                title="⚠️  额度不足",
                border_style="red"
            ))
            
        else:
            console.print(f"[yellow]⚠️  API 返回状态码: {response.status_code}[/yellow]")
            console.print(f"[dim]{response.text[:200]}[/dim]\n")
    
    except requests.exceptions.Timeout:
        console.print("[red]❌ 请求超时，请检查网络连接[/red]\n")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ 网络错误: {e}[/red]\n")
    except Exception as e:
        console.print(f"[red]❌ 发生错误: {e}[/red]\n")
    
    # 显示帮助信息
    console.print(Panel.fit(
        "[bold cyan]📋 如何解决额度不足问题[/bold cyan]\n\n"
        "[bold]1. 查看账户余额:[/bold]\n"
        "   https://platform.openai.com/account/usage\n\n"
        "[bold]2. 充值账户:[/bold]\n"
        "   https://platform.openai.com/account/billing/overview\n"
        "   点击 'Add to credit balance'\n"
        "   最低充值: $5\n\n"
        "[bold]3. 查看使用情况:[/bold]\n"
        "   https://platform.openai.com/usage\n\n"
        "[bold]💡 省钱技巧:[/bold]\n"
        "   - 使用 gpt-3.5-turbo (最便宜)\n"
        "   - 减少请求长度\n"
        "   - 设置使用限额提醒\n\n"
        "[bold]💰 参考价格 (gpt-3.5-turbo):[/bold]\n"
        "   输入: $0.0005 / 1K tokens\n"
        "   输出: $0.0015 / 1K tokens\n"
        "   约 $0.002 / 1000 次简单对话",
        title="💡 帮助信息",
        border_style="cyan"
    ))


def main():
    console.print(Panel.fit(
        "[bold green]💰 OpenAI 账户检查工具[/bold green]\n\n"
        "检查你的 API 密钥状态和可用模型",
        title="账户检查",
        border_style="green"
    ))
    
    check_account()
    
    console.print("\n[dim]提示: 如果需要充值，访问 https://platform.openai.com/account/billing[/dim]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]检查已取消[/yellow]")
    except Exception as e:
        console.print(f"\n[red]发生错误: {e}[/red]")

