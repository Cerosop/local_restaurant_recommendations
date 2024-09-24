import jellyfish
import pandas as pd
from web_scrapper import get_recommend_web_url, get_web_text
from map_scraper import get_review_page_url, get_reviews
from analyze_by_claude import analyze_reviews, analyze_web


# TODO: 測試各地點、模型
max_web_num = 5
max_restaurant_num = 1e9
max_review_num = 40
debug = False
model_web_is_cheap = False
model_review_is_cheap = True
# 5個網站全部推薦兩次以上店家各40個評論用貴的模型要6-12塊，(便宜的/10)


if '1' in input('搜尋特定地點按1，搜尋特定店家按2\n'):
    place = input('輸入想查詢的地點\n')

    web_urls = get_recommend_web_url(place, debug=debug)
    web_analyze_result_list = []

    for l in web_urls[:min(max_web_num, len(web_urls))]:
        web_text_list = get_web_text(web_url=l, debug=debug)
        # for i, x in enumerate(web_text_list):
        #     print(i + 1)
        #     print(x)
                
        web_analyze_result = analyze_web(web_text_list, is_cheap=model_web_is_cheap, max_token=1000)
        web_analyze_result_list.append(web_analyze_result)
        print(f"此網站找到{len(web_analyze_result)}個推薦")
        # print(web_analyze_result)

    # result1 = [['一燔歐姆蛋咖哩', '基隆市仁愛區仁五路59號'], ['九如營養三明治', '未知'], ['全家福元宵', '未知'], ['橋頭臭豆腐基隆店', '基隆市仁愛區孝三路60號'], ['魚丸伯仔', '基隆市仁愛區愛二路56號'], ['金龍肉羹', '基隆市中正區中船路94號'], ['阿美麵店', '基隆市中正區和一路99號'], ['遠東煎包', '基隆市仁愛區忠三路91號'], ['魯都香', '基隆市中山區復興路183號'], ['手工碳烤吉古拉', '基隆市中正區正濱路27號'], ['小林烤鴨車', '未知'], ['安樂市場菜頭滷', '基隆市安樂區樂一路22號'], ['七堵酸菜白肉鍋宣騰莊', '基隆市七堵區開元路96號'], ['連珍糕餅店', '基隆市仁愛區愛二路42號'], ['十二堂雞絲飯', '基隆市中正區正豐街93號1樓'], ['廣東汕頭牛肉店 ', '基隆市中山區復旦路17之6號'], ['古月香熬粹牛肉麵', '基隆市安樂區麥金路421巷6號'], ['吳姳麵館', '基隆市仁愛區愛三路21號2樓'], ['西 定路麵館東家館', '基隆市中山區西定路76號'], ['天下滷肉飯', '基隆市安樂區樂利三街251號'], ['加分火鍋', '基隆市 仁愛區愛四路41號2、3樓'], ['春興水餃店', '基隆市中正區環港街68號'], ['榮生魚片', '基隆市仁愛區成功一路118巷3弄2號'], ['上海美味鮮湯包', '基隆市中正區北寧路317-6號'], ['七元生魚片海產店', '基隆市安樂區基金三路71號'], ['發哥臭豆腐', '基隆市仁愛區龍安街205號之1'], ['藏魚殿', '基隆市中正區義二路35號'], ['壽司郎基隆站前店', '基隆市仁愛區港西街5號3樓'], ['藏壽司基隆中正信三店', '未知'], ['逸番亭', '基隆市安樂區基金一路108之19號1樓'], ['峰壽司', '基隆市仁愛區愛三路21號攤位B42'], ['義美石頭火鍋', '基隆市中正區信二路303號'], ['望海巷石頭火鍋', '基隆市中正區北寧路369巷50-1號'], ['三奇千層蛋糕', '基隆市仁愛區愛二路54巷2號'], ['洪佳豆花仁愛店', '基隆市仁愛區愛三路21號2樓'], ['啾啾咖啡', '未知'], ['涮樂和牛鍋物', '基隆市仁愛區仁二路236號4樓'], ['燒鶴一番町', '基隆市仁愛區 愛五路4之1號1'], ['基隆樂天燒肉', '基隆市中正區信三路7號'], ['滿滿燒肉', '基隆市仁愛區愛二路23號'], ['燒肉smile基隆潮境公園店', '基隆市中正區北寧路369巷61號2樓'], ['築間基隆潮境公園店', '基隆市中正區北寧路369巷61號3樓'], ['八斗子夜市', '基隆市中正區北寧路262號'], ['基隆廟口美食', '未知'], ['仁愛市場', '未知']]
    # result2 = [['一燔歐姆蛋咖哩', '未知'], ['九如營養三明治', '基隆市安樂區基金一路133-2號'], ['全家福元宵', '未知'], ['橋頭臭豆腐基隆店', '基隆市仁愛區孝三路60號'], ['魚丸伯', '基隆市仁愛區愛二路56號'], ['金龍肉羹', '基隆市中正區中船路94號'], ['阿美麵店', '基隆市中正區和一路99號'], ['遠東煎包', '基隆市仁愛區忠三路91號'], ['魯都香滷味', '基隆市中山區復興路183號'], ['碳烤吉古拉', '基隆市中正區正濱路27號'], ['小林烤鴨車', '未知'], ['安樂菜頭滷', '基隆市安樂區樂一路22號'], ['宣騰莊', '基隆市七堵區開元路96號'], ['連珍糕餅店', '基隆市仁愛區愛二路42號'], ['十二堂', '基隆市中正區正豐街93號1樓'], ['廣東汕頭牛肉店 ', '基隆市中山區復旦路17之6號'], ['古月香', '基隆市安樂區麥金路421巷6號'], ['吳姳麵館', '基隆市仁愛區愛三路21號2樓'], ['西 定路麵館東家館', '基隆市中山區西定路76號'], ['天下滷肉飯', '基隆市安樂區樂利三街251號'], ['加分火鍋', '基隆市 仁愛區愛四路41號2、3樓'], ['春興水餃店', '基隆市中正區環港街68號'], ['榮生魚片', '基隆市仁愛區成功一路118巷3弄2號'], ['上海美味鮮湯包', '基隆市中正區北寧路317-6號'], ['七元生魚片', '基隆市安樂區基金三路71號'], ['發哥臭豆腐', '基隆市仁愛區龍安街205號之1'], ['藏魚殿', '基隆市中正區義二路35號'], ['壽司郎基隆站前店', '基隆市仁愛區港西街5號3樓'], ['藏壽司基隆中正信三店', '未知'], ['逸番亭', '基隆市安樂區基金一路108之19號1樓'], ['峰壽司', '基隆市仁愛區愛三路21號攤位B42'], ['義美', '基隆市中正區信二路303號'], ['望海巷', '基隆市中正區北寧路369巷50-1號'], ['三奇千層蛋糕', '基隆市仁愛區愛二路54巷2號'], ['洪佳豆花仁愛店', '基隆市仁愛區愛三路21號2樓'], ['啾啾咖啡', '未知'], ['涮樂和牛鍋物', '基隆市仁愛區仁二路236號4樓'], ['燒鶴一番町', '基隆市仁愛區 愛五路4之1號1'], ['基隆樂天燒肉', '基隆市中正區信三路7號'], ['滿滿燒肉', '基隆市仁愛區愛二路23號'], ['燒肉smile基隆潮境公園店', '基隆市中正區北寧路369巷61號2樓'], ['築間基隆潮境公園店', '基隆市中正區北寧路369巷61號3樓'], ['八斗子夜市', '基隆市中正區北寧路262號'], ['基隆廟口', '未知'], ['仁愛市場', '未知']]
    # print(jellyfish.jaro_winkler_similarity('酸菜白肉鍋宣騰莊', '七堵酸菜白肉鍋宣騰莊'))
    # result  = [result1, result2]

    restaurant_list = []
    for r in web_analyze_result_list:
        for i in r:
            x = True
            for j in restaurant_list:
                for k in j[0]:
                    if i[0] == k:
                        if j[1] == '未知':
                            j[1] = i[1]
                        j[2] += 1
                        x = False
                        break
                    elif i[1] == j[1] and jellyfish.jaro_winkler_similarity(i[0], k) > 0.7:
                        j[0].append(i[0])
                        j[2] += 1
                        x = False
                        break
                if not x:
                    break
            if x:
                restaurant_list.append([[i[0]], i[1], 1])

    restaurant_list = sorted(restaurant_list, key=lambda x: x[2], reverse=True)
    print('獲取到的店家資訊: \n' + str(restaurant_list))
    restaurant_list = [i for i in restaurant_list if i[2] > 1]
    
    restaurant_result_list = []
    for i in restaurant_list[:min(max_restaurant_num, len(restaurant_list))]:
        search_name = i[0][0]
        if i[1] != '未知':
            search_name += " " + i[1]
        
        review_url = get_review_page_url(search_name, debug=debug)
        
        if not review_url:
            restaurant_result_list.append([i[0][0], i[2], "在google map找不到此店家"])
            continue
        
        # 差不多一則評論100 token input  每40則評論便宜的0.05 詳細的0.5元台幣
        reviews_list = get_reviews(review_url, max_review_num, debug=debug)
                
        # for i, r in enumerate(reviews_list):
        #     print(i + 1, r)
            
        reviews_result = analyze_reviews(reviews_list, is_cheap=model_review_is_cheap, max_token=500)
        
        restaurant_result_list.append([i[0][0], i[2], reviews_result])
        
        # print(i[0][0])
        # print(result)
        
    for i in restaurant_result_list:
        print('--------------------')
        print(f"{i[0]}總共被推薦{i[1]}次，下方是這家店的map評論總結")
        print(i[2])
        print()

    df = pd.DataFrame(restaurant_result_list)

    df.to_excel(f"output/{place}推薦店家.xlsx", index=False, header=['店家', '被推薦次數', 'map評論總結'])

else:
    restaurant_name = input('輸入想查詢的店家名稱(存檔用)\n')
    restaurant_url = input('輸入想查詢的店家 google map url(請按到review那)\n')
    
    reviews_list = get_reviews(restaurant_url, max_review_num, debug=debug)
        
    # for i, r in enumerate(reviews_list):
    #     print(i + 1, r)
        
    reviews_result = analyze_reviews(reviews_list, is_cheap=model_review_is_cheap, max_token=500)
    print('--------------------')
    print("下方是這家店的map評論總結")
    print(reviews_result)
    print()

    df = pd.DataFrame([[restaurant_url, reviews_result]])

    df.to_excel(f"output/{restaurant_name}評價.xlsx", index=False, header=['url', 'map評論總結'])
