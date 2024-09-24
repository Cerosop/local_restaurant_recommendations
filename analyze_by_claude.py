import anthropic
from pyhocon import ConfigFactory

conf = open('key.conf').read()
api_key = ConfigFactory.parse_string(conf)['key']

client = anthropic.Anthropic(api_key = api_key)

def analyze_reviews(reviews_list, is_cheap = False, max_token = 500):
    # if 'f' in input("免費試用9/16到期，是否繼續使用(T/F)").lower():
    #     return ''
    
    if is_cheap:
        model = "claude-3-haiku-20240307"
    else:
        model = "claude-3-5-sonnet-20240620"
    
    prompt = """
    請根據以下評論分析餐廳資訊：
    1. 推薦的食物
    2. 不推薦的食物
    3. 有提到的注意事項
    4. 整體風評

    評論：
    {}
    """.format("\n".join(reviews_list))
    
    message = client.messages.create(
        model=model, 
        max_tokens=max_token, 
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reviews_result = message.content[0].text
    print("success to analyze reviews")
    return reviews_result


def analyze_web(web_text_list, is_cheap = False, max_token = 1000):
    # if 'f' in input("免費試用9/16到期，是否繼續使用(T/F)").lower():
    #     return ''
    
    if is_cheap:
        model = "claude-3-haiku-20240307"
    else:
        model = "claude-3-5-sonnet-20240620"
        
    
    prompt = """
    請根據下方附上的當地推薦餐廳的網頁的內容文字統整提到的餐廳資訊：
    1. 全部有被推薦的餐廳名稱
    2. 此餐廳的地址
    並輸出成以下格式
    
    1. 店名: 甲店
    地址: 甲店地址
    2. 店名: 乙店
    地址: 未知
    
    提醒: 通常title會寫到此網站有幾家推薦餐廳，請盡量全部找到並列出全部店家，不要省略任何一個，就算店家數量很多也是請全部輸出

    網頁內容文字：
    {}
    """.format("\n".join(web_text_list))
    
    message = client.messages.create(
        model=model, 
        max_tokens=max_token, 
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    web_analyze_result = message.content[0].text.split("\n")
    
    web_analyze_result = [i.split(": ")[1].replace(" ", "") for i in web_analyze_result[1:] if len(i.split(": ")) == 2]

    web_analyze_result = [[web_analyze_result[i * 2], web_analyze_result[i * 2 + 1]] for i in range(int(len(web_analyze_result) / 2))]

    print("success to analyze web")
    return web_analyze_result


if __name__ == '__main__':
    # 示例评论列表
    reviews_list = [
        '這家餐廳的意大利麵真的很棒！不過沙拉有點鹹。',
        "服務很好，但湯有點溫度不夠。",
        '非常喜歡這裡的烤雞肉，甜點也很不錯。',
        "環境很好，但價格有點貴。",
    ]

    reviews_result = analyze_reviews(reviews_list)
    print(reviews_result)