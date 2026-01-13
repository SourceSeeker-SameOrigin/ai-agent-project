#!/usr/bin/env python3
"""
验证 OpenAI API 密钥是否配置正确
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print("\n[bold cyan]🔍 验证 API 密钥配置...[/bold cyan]\n")
    
    # 加载环境变量
    load_dotenv()
    
    # 获取 API 密钥
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        console.print(Panel.fit(
            "[bold red]❌ 未找到 API 密钥[/bold red]\n\n"
            "请检查:\n"
            "1. .env 文件是否存在于项目根目录\n"
            "2. .env 文件中是否包含 OPENAI_API_KEY=...\n"
            "3. 密钥格式是否正确（无引号，无空格）",
            title="配置错误",
            border_style="red"
        ))
        return False
    
    # 检查密钥格式
    console.print(f"[green]✅ 找到 API 密钥[/green]")
    console.print(f"[dim]密钥: {api_key[:7]}...{api_key[-4:]}[/dim]")
    console.print(f"[dim]长度: {len(api_key)} 字符[/dim]\n")
    
    # 基本格式检查
    issues = []
    
    if not api_key.startswith("sk-"):
        issues.append("❌ 密钥应以 'sk-' 开头")
    else:
        console.print("[green]✅ 密钥前缀正确 (sk-)[/green]")
    
    if len(api_key) < 40:
        issues.append(f"❌ 密钥太短 ({len(api_key)} 字符)，正常应该 51+ 字符")
    elif len(api_key) > 200:
        issues.append(f"❌ 密钥太长 ({len(api_key)} 字符)，可能包含多余字符")
    else:
        console.print(f"[green]✅ 密钥长度合理 ({len(api_key)} 字符)[/green]")
    
    if " " in api_key:
        issues.append("❌ 密钥中包含空格")
    else:
        console.print("[green]✅ 密钥中无空格[/green]")
    
    if "\n" in api_key or "\r" in api_key:
        issues.append("❌ 密钥中包含换行符")
    else:
        console.print("[green]✅ 密钥中无换行符[/green]")
    
    # 显示问题
    if issues:
        console.print("\n[bold yellow]⚠️  发现问题:[/bold yellow]")
        for issue in issues:
            console.print(f"  {issue}")
        console.print("\n[yellow]请检查 .env 文件中的密钥配置[/yellow]")
        return False
    
    # 测试 API 连接
    console.print("\n[bold cyan]🌐 测试 API 连接...[/bold cyan]\n")
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # 使用便宜的模型测试
            temperature=0,
            api_key=api_key,
            max_tokens=10
        )
        
        # 发送简单测试
        response = llm.invoke("Say 'OK'")
        
        console.print(Panel.fit(
            "[bold green]🎉 API 密钥配置成功！[/bold green]\n\n"
            f"测试响应: {response.content}\n\n"
            "你现在可以开始使用 AI Agent 了！\n\n"
            "[bold]运行命令:[/bold]\n"
            "  python agent.py              # 对话模式\n"
            "  python agent.py --tools      # 查看工具\n"
            "  streamlit run web_ui.py      # Web 界面",
            title="✅ 验证成功",
            border_style="green"
        ))
        return True
        
    except Exception as e:
        error_str = str(e)
        
        if "401" in error_str or "invalid_api_key" in error_str:
            console.print(Panel.fit(
                "[bold red]❌ API 密钥无效[/bold red]\n\n"
                "OpenAI 服务器拒绝了这个密钥\n\n"
                "可能的原因:\n"
                "1. 密钥复制不完整\n"
                "2. 密钥已被撤销或过期\n"
                "3. 密钥格式有误\n\n"
                "解决方案:\n"
                "1. 访问 https://platform.openai.com/api-keys\n"
                "2. 创建新的 API 密钥\n"
                "3. 完整复制密钥并更新 .env 文件",
                title="验证失败",
                border_style="red"
            ))
        elif "429" in error_str or "rate_limit" in error_str:
            console.print(Panel.fit(
                "[bold yellow]⚠️  请求太频繁[/bold yellow]\n\n"
                "密钥有效，但达到速率限制\n"
                "请稍后再试",
                title="速率限制",
                border_style="yellow"
            ))
        elif "insufficient_quota" in error_str:
            console.print(Panel.fit(
                "[bold yellow]⚠️  账户余额不足[/bold yellow]\n\n"
                "密钥有效，但账户没有可用额度\n\n"
                "解决方案:\n"
                "1. 访问 https://platform.openai.com/account/billing\n"
                "2. 充值账户（最低 $5）\n"
                "3. 或使用新账户的免费额度",
                title="余额不足",
                border_style="yellow"
            ))
        else:
            console.print(Panel.fit(
                f"[bold red]❌ API 连接失败[/bold red]\n\n"
                f"错误信息:\n{error_str[:200]}\n\n"
                "请检查:\n"
                "1. 网络连接是否正常\n"
                "2. API 密钥是否正确\n"
                "3. OpenAI 服务是否可用",
                title="连接失败",
                border_style="red"
            ))
        
        return False


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]验证已取消[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[bold red]验证过程出错: {e}[/bold red]")
        exit(1)

