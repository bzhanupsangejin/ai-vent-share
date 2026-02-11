"""
AI协作审核 - 咨询豆包和千问关于AI网站的问题
"""
import subprocess
import time
import random
import pyautogui
import pyperclip
from pywinauto.application import Application
from pywinauto import Desktop

def check_app_running(app_keyword):
    """检查应用是否运行"""
    windows = Desktop(backend="uia").windows()
    for window in windows:
        try:
            title = window.window_text()
            if app_keyword in title:
                return True
        except:
            pass
    return False

def start_application(app_name, shortcut_path):
    """启动应用程序"""
    print(f"🚀 正在启动 {app_name}...")
    try:
        subprocess.Popen(['cmd', '/c', 'start', '', shortcut_path], shell=True)
        time.sleep(12)
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def send_to_doubao(message):
    """向豆包发送消息"""
    print("🤖 连接豆包...")
    app = Application(backend="uia").connect(title_re=".*豆包.*", timeout=10)
    window = app.window(title_re=".*豆包.*")
    window.set_focus()
    time.sleep(1)
    
    rect = window.rectangle()
    input_x = rect.left + int(rect.width() * 0.82)
    input_y = rect.bottom - int(rect.height() * 0.10)
    
    pyautogui.click(input_x, input_y)
    time.sleep(0.5)
    
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("✅ 消息已发送")
    return True

def send_to_qianwen(message):
    """向千问发送消息"""
    print("🤖 连接千问...")
    app = Application(backend="uia").connect(title_re=".*千问.*", timeout=10)
    window = app.window(title_re=".*千问.*")
    window.set_focus()
    time.sleep(1)
    
    try:
        new_chat_btn = window.child_window(title="新对话", control_type="Button")
        new_chat_btn.click()
        time.sleep(2)
    except:
        pass
    
    try:
        edit = window.child_window(control_type="Edit")
        rect = edit.rectangle()
        center_x = rect.left + rect.width() // 2
        center_y = rect.top + rect.height() // 2
        pyautogui.click(center_x, center_y)
    except:
        rect = window.rectangle()
        input_x = rect.left + int(rect.width() * 0.57)
        input_y = rect.top + int(rect.height() * 0.55)
        pyautogui.click(input_x, input_y)
    
    time.sleep(0.5)
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("✅ 消息已发送")
    return True

def wait_and_get_answer(wait_time=40):
    """等待回答并获取内容"""
    print(f"⏳ 等待 {wait_time} 秒...")
    
    for i in range(wait_time // 5):
        time.sleep(5)
        print(f"   已等待 {(i+1)*5} 秒...")
    
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'home')
    time.sleep(0.5)
    pyautogui.scroll(-5)
    time.sleep(1)
    
    best_content = ""
    for attempt in range(3):
        pyautogui.click(800, 450)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        content = pyperclip.paste()
        if len(content) > len(best_content):
            best_content = content
    
    print(f"✅ 获取到 {len(best_content)} 字符")
    return best_content

def main():
    print("=" * 80)
    print("AI协作审核 - 咨询豆包和千问")
    print("=" * 80)
    
    # 启动应用
    if not check_app_running("豆包"):
        start_application("豆包", r"C:\Users\HYX\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\豆包.lnk")
    
    if not check_app_running("千问"):
        start_application("千问", r"C:\Users\HYX\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\千问\千问.lnk")
    
    time.sleep(3)
    
    # 向豆包提问
    print("\n" + "=" * 80)
    print("向豆包提问")
    print("=" * 80)
    
    question1 = """
我在审核一个AI资源分享网站，发现了一个问题：

【网站设计】
- 配置文件定义了8种标准资源类型：AI工具、代码模板、FAQ文档、免费API、技术教程、资源分享、部署指南、合规说明
- 目的是标准化和简化分类

【实际情况】
- 数据库中有311条资源
- 但实际有43种不同的类型！比如：API服务、AutoML、MLOps、云平台、伦理规范、公平性工具、可视化工具等等
- 这些类型都不在标准的8种类型里

【网站精神】
"人类维护者提交资源时，系统不生成/不记录任何可关联到个人的标识符"
—— 匿名性不是"技术处理"，是架构哲学

【问题】
1. 这43种类型是否应该统一归类到8种标准类型？
2. 如果要归类，应该如何映射？
3. 还是说应该保留这些细分类型？

请基于网站精神和标准化原则给出建议。
"""
    
    try:
        send_to_doubao(question1)
        answer1 = wait_and_get_answer(45)
        
        with open("C:\\Users\\HYX\\Desktop\\doubao_audit_answer.txt", "w", encoding="utf-8") as f:
            f.write(f"【问题】\n{question1}\n\n{'='*60}\n\n【豆包回答】\n{answer1}")
        
        print("✅ 豆包回答已保存")
    except Exception as e:
        print(f"❌ 豆包提问失败: {e}")
        return
    
    time.sleep(5)
    
    # 向千问提问
    print("\n" + "=" * 80)
    print("向千问提问")
    print("=" * 80)
    
    question2 = f"""
我在审核一个AI资源分享网站，刚问了豆包一个问题。

【背景】
网站定义了8种标准类型，但实际数据库有43种类型，严重不符合标准化设计。

【豆包的建议】
{answer1[:500] if len(answer1) > 500 else answer1}

【我的疑问】
1. 是否应该强制统一到8种标准类型？
2. 还是应该扩展标准类型列表？
3. 如何平衡标准化和灵活性？

请从技术架构和用户体验角度给出建议。
"""
    
    try:
        send_to_qianwen(question2)
        answer2 = wait_and_get_answer(50)
        
        with open("C:\\Users\\HYX\\Desktop\\qianwen_audit_answer.txt", "w", encoding="utf-8") as f:
            f.write(f"【问题】\n{question2}\n\n{'='*60}\n\n【千问回答】\n{answer2}")
        
        print("✅ 千问回答已保存")
    except Exception as e:
        print(f"❌ 千问提问失败: {e}")
        return
    
    print("\n" + "=" * 80)
    print("✅ AI协作审核完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()
