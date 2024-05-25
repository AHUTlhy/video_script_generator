# streamlit组件
# 运行方式：streamlit run main.py

import streamlit as st
from utils import generate_script

st.title("视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

subject = st.text_input("请输入视频的主题")
video_length = st.number_input("请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
creativity = st.slider("请输入视频脚本的创造力（数字越小说明更严谨，数字大说明更多样)", min_value=0.0, max_value=1.0, value=0.2, step=0.1) # value表示默认值

submit = st.button("生成脚本")  # 返回的结果是True或者False

if submit and not openai_api_key:
    st.info("请输入您的OpenAI API密钥！") # 显示提示信息
    st.stop()   # 代码执行到此时候，停止执行

if submit and not subject:
    st.info("请输入视频的主题！")
    st.stop()

if submit:
    with st.spinner(("AI正在思考中，请稍等...")):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("视频脚本已生成！")
    st.subheader("标题：")
    st.write(title)
    st.subheader("视频脚本：")
    st.write(script)
    # 对于维基百科搜索的内容，用户可看可不看
    with st.expander("维基百科搜索结果"):
        st.info(search_result)
