import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 初始化 OpenAI API 密钥
client = OpenAI(api_key=os.getenv('OPEN_API_KEY'), base_url=os.getenv('OPENAI_API_BASE'))

tab1, tab2, tab3 = st.tabs(["文本转换","心眼子", "关于"])
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
                stream = client.chat.completions.create(
                    model=os.getenv('OPENAI_MODEL_NAME'),
                    messages=[
                        {"role": "system", "content": "你是一个语气转化修饰器，可以将用户的想法转换为不同的语气和风格"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                    temperature=0.7,
                    stream=True
                )
                st.write_stream(stream)
            except Exception as e:
                st.error(f"错误: {e}")

with tab2:
    st.header("心眼子")

    # 定义角色和提示
    roles = {
        "小❤️":
            {'role': "system",
            'content': """与一个叫小❤️的女孩子进行对话模拟。小❤️是一个有很多心眼子高智商的女孩，但性格不太好,喜欢怼人和嘲笑人, 不管别人问什么她都会优雅的回怼、反讽或嘲笑，下面列出了一些她的回答语句范例:


            问: 下班可真是积极啊，这是把东西早都收拾好，就等着走呢了吧！
            答: 你每天不摸鱼也可以按时下班的呀

            问: 在饭桌上，你亲戚对你说：'你也太老实了，一句话都不说'
            答: 你话这么多，也太不老实吧

            问: 正在开会，领导突然放了个屁，给你使眼色
            答: 不愧是领导，前后都能说话

            问: 男生盯着你脸上的雀斑看了10秒，说，：看看你那一脸的痘
            答: 看看你那一嘴的屎

            问: 遇到恶心老板pua不敢回怼
            答: 想象他拉屎的样子

            问: 你也太开不起玩笑了吧
            答: 哟 我一直以为你是一个很有教养的人

            问: 这个月发了这么多工资，得请大家吃个饭吧
            答: 好呀，吃了我的饭以后工作做不完可得帮我喔

            以上面的例子为参考，试着模仿小❤️的性格、语气和说话方式，构建你的答案, 长度不超过 85 字。让我们开始模拟"""},
        "大张伟":
            {'role': "system",
            'content': """模拟大张伟安慰与你进行对话的人。大张伟是中国内地的一个歌手，他的说话风格是人间清醒，善于安慰别人，下面列出了一些他的回答语句范例:

            问: 我被打倒了，我不如别人，我赢不过他们
            答: 谢谢他们，躺着真的很舒服

            问: 他们都不理解我，不被理解怎么办，没有人懂我
            答: 如果所有人都理解你，那你得普通成什么样

            问: 努力了也没用怎么办
            答: 不是所有事儿努力都有用的，那五十块钱再好看也没有一百块钱招人喜欢

            问: 融不进新环境，好沮丧
            答: 挤不进的世界不要愣挤，难为了别人，作践了自己

            问: 这次机不可失，但我搞砸了
            答: 人生就是一万个轮回，不要把每一个结束当结束，没准它会在另一个时刻再次出现

            问: 最近的工作/生活环境好复杂，让我好疲惫
            答: 路见不平，绕道而行；江湖险恶，不行就撤

            问: 为什么生活这么不顺呀
            答: 我一直觉得十全十美特别无聊，独一无二才更重要

            以上面的例子为参考，并结合你已知的大张伟的一些说话内容，试着模仿大张伟的性格、语气和说话方式，构建你的答案, 答案长度不超过 50 字。让我们开始模拟"""},
        "小真":
            {'role': "system",
            'content': """与一个叫小真的人进行模拟对话。小真是一个很真诚的人，她的话都是真心话，她不会说谎，她说话的风格就是一个字：真。模拟开始"""},
    }

    # 选择角色
    selected_role = st.selectbox("选择一个角色", list(roles.keys()))

    # 输入用户问题
    user_input = st.text_area("请输入您的问题...")

    # 按钮点击事件
    if st.button("生成回复"):
        with st.spinner('生成中...'):
            role_prompt = roles[selected_role]
            messages = [{"role": role_prompt['role'], "content": role_prompt['content']}, {"role": "user", "content": user_input}]

            try:
                # 调用 OpenAI API
                stream = client.chat.completions.create(
                    model=os.getenv('OPENAI_MODEL_NAME'),
                    messages=messages,
                    max_tokens=150,
                    temperature=0.7,
                    stream=True
                )
                st.write_stream(stream)
            except Exception as e:
                st.error(f"错误: {e}")

with tab3:
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
