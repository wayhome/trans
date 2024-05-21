import os
import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 OpenAI API 密钥
client = OpenAI(api_key=os.getenv('OPEN_API_KEY'), base_url=os.getenv('OPENAI_API_BASE'))

tab1, tab2 = st.tabs(["文本转换", "关于"])
with tab1:
    st.title('文本转换器')
    st.write('将您的想法转换为不同的语气和风格')

    # 输入文本
    input_text = st.text_area('请输入您的文本...')

    # 选择转换类型
    transformation = st.selectbox(
        '选择转换类型:',
        [
            '更专业', '更礼貌', '更少讽刺', '更易读', 
            '更正式', '更随意', '更健谈（废话连篇）', 
            '更简洁（废话少说）', '更冷静', '更有激情', 
            '更讽刺', '语法正确', '要点列出', 
            '单词同义词（词库模式）'
        ]
    )

    # 提示语映射
    prompts = {
        '更专业': "将以下文本改写得更专业:\n\n",
        '更礼貌': "将以下文本改写得更礼貌:\n\n",
        '更少讽刺': "将以下文本改写得更少讽刺:\n\n",
        '更易读': "将以下文本改写得更易读:\n\n",
        '更正式': "将以下文本改写得更正式:\n\n",
        '更随意': "将以下文本改写得更随意:\n\n",
        '更健谈（废话连篇）': "将以下文本改写得更健谈（废话连篇）:\n\n",
        '更简洁（废话少说）': "将以下文本改写得更简洁（废话少说）:\n\n",
        '更冷静': "将以下文本改写得更冷静:\n\n",
        '更有激情': "将以下文本改写得更有激情:\n\n",
        '更讽刺': "将以下文本改写得更讽刺:\n\n",
        '语法正确': "将以下文本改写得语法正确:\n\n",
        '要点列出': "将以下文本转换为要点:\n\n",
        '单词同义词（词库模式）': "提供以下文本的单词同义词:\n\n"
    }

    # 按钮点击事件
    if st.button('转换'):
        with st.spinner('转换中...'):
            # 根据选择的转换类型获取对应的 prompt
            prompt = prompts[transformation] + input_text
            
            try:
                response = client.chat.completions.create(
                    model=os.getenv('OPEN_API_MODEL'),
                    messages=[
                        {"role": "system", "content": "你是一个语气转化修饰器，可以将用户的想法转换为不同的语气和风格"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    temperature=0.7,
                    stream=False
                )
                converted_text = response.choices[0].message.content.strip()
                st.text_area('转换后的文本将出现在这里...', value=converted_text, height=200)
            except Exception as e:
                st.error(f"错误: {e}")

with tab2:
    st.header("关于")
    st.markdown("""
    **文本转换器** 使用 LLM 模型来将您的文本转换为不同的语气和风格。
    
    ### 功能
    - 将文本转换为更专业、更礼貌或更讽刺的风格。
    - 提供更易读或更简洁的文本版本。
    - 提供语法正确的文本。
    - 生成要点或单词同义词。

    ### 使用方法
    1. 在 "文本转换" 标签页中输入您要转换的文本。
    2. 选择所需的转换类型。
    3. 点击 "转换" 按钮查看转换后的文本。

    ### 关于开发者
    这是一个使用 Streamlit 和 OpenAI API 构建的示例应用程序。
    """)
