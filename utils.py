from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, creativity, api_key):
    """
    生成指定主题视频的脚本。

    参数:
    - subject: 电影主题，字符串类型。
    - video_length: 视频时长，以分钟为单位的整数。
    - creativity: 生成脚本的创意程度，浮点数，控制OpenAI模型的输出温度。
    - api_key: OpenAI的API密钥，字符串类型。

    返回值:
    - search_result: 维基百科搜索结果的相关信息。
    - title: 生成的视频标题，字符串类型。
    - script: 生成的视频脚本，字符串类型。
    """
    # 使用ChatPromptTemplate创建标题和脚本模板
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间、结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合一下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             '''{wikipedia_search}'''"""
             )
        ]
    )

    # 初始化OpenAI模型
    model = OpenAI(openai_api_key=api_key, temperature=creativity, max_tokens=2000)

    # 使用模板和模型生成标题
    # title_template | model表示只创建了操作的链接，没有执行，需要调用invoke方法执行
    title_chain = title_template | model  # 把title_template的结果作为model的输入，然后返回model的输出
    title = title_chain.invoke({"subject": subject})

    # 使用维基百科API搜索主题信息
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    # 使用模板和模型生成脚本
    script_chain = script_template | model
    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result})

    return search_result, title, script



