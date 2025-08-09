import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

# 配置参数
INPUT_FILE = "1970s_billboard_hot100_links.csv"
OUTPUT_FILE = "1970s_song_metadata.csv"
DELAY = 1.5  # 请求延迟(秒)
USER_AGENT = "BillboardScraper/1.0 (https://example.com)"

# 要提取的信息字段映射
FIELDS_OF_INTEREST = {
    "genre": "genre",
    "length": "length",
    "language": "language",
    "label": "label"
}

def clean_song_title(title):
    """清理歌曲标题，只保留主歌名"""
    # 移除日期部分（如 "January 3,"）
    if "," in title:
        title = title.split(",", 1)[1].strip()
    
    # 移除引号
    title = title.replace('"', '').replace("'", "").strip()
    
    # 处理斜杠分隔的多首歌曲（取第一首）
    if "/" in title:
        title = title.split("/")[0].strip()
    
    # 处理括号内容（如 "(They Long to Be) Close to You"）
    if "(" in title:
        # 保留括号内内容
        title = title.split("(")[0].strip() + title[title.find("("):]
    
    return title

def construct_wikipedia_url(song):
    """构建Wikipedia URL（仅基于歌曲名）"""
    clean_song = clean_song_title(song)
    encoded_query = quote(clean_song.replace(" ", "_"))
    return f"https://en.wikipedia.org/wiki/{encoded_query}"

def get_redirect_url(soup):
    """处理重定向页面"""
    redirect = soup.find("ul", class_="redirectText")
    if redirect and redirect.find("a"):
        return "https://en.wikipedia.org" + redirect.find("a")["href"]
    return None

def extract_infobox_data(soup):
    """从Infobox提取数据"""
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return {}
    
    data = {}
    rows = infobox.find_all("tr")
    
    for row in rows:
        th = row.find("th")
        td = row.find("td")
        
        if th and td:
            field = th.text.strip().lower()
            value = td.get_text(" ", strip=True)
            value = " ".join(value.split())  # 清理多余空格
            
            # 检查是否是我们感兴趣的字段
            for key in FIELDS_OF_INTEREST:
                if key in field:
                    data[FIELDS_OF_INTEREST[key]] = value
    
    return data

def scrape_song_data(df):
    """主爬虫函数"""
    results = []
    
    for index, row in df.iterrows():
        song = row["song"]
        artist = row["artist"]
        
        if pd.isna(song):
            print(f"[!] 跳过第 {index+1} 行: 缺少歌曲信息")
            continue
            
        data = {
            "year": row["year"],
            "original_song_title": song,
            "clean_song_title": clean_song_title(song),
            "artist": artist,
            "genre": "",
            "length": "",
            "language": "",
            "label": "",
            "wikipedia_url": "",
            "page_exists": False,
            "is_redirect": False
        }
        
        try:
            # 构建Wikipedia URL（仅基于歌曲名）
            url = construct_wikipedia_url(song)
            data["wikipedia_url"] = url
            
            print(f"[{index+1}/{len(df)}] 处理: {data['clean_song_title']}")
            
            # 发送请求
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # 检查是否是消歧义页面
            if soup.find("table", id="disambigbox"):
                print("   → 消歧义页面，跳过")
                results.append(data)
                time.sleep(DELAY)
                continue
                
            # 检查重定向
            redirect_url = get_redirect_url(soup)
            if redirect_url:
                print(f"   → 重定向到: {redirect_url}")
                response = requests.get(redirect_url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                data["is_redirect"] = True
                data["wikipedia_url"] = redirect_url
            
            # 提取Infobox数据
            infobox_data = extract_infobox_data(soup)
            for key, value in infobox_data.items():
                data[key] = value
            
            data["page_exists"] = True
            print(f"   ✓ 找到数据: {infobox_data}")
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                print("   ✗ 页面不存在")
            else:
                print(f"   ✗ HTTP错误: {e}")
        except Exception as e:
            print(f"   ✗ 错误: {e}")
        finally:
            results.append(data)
            time.sleep(DELAY)
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    # 读取输入文件
    print(f"读取输入文件: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # 运行爬虫
    print("开始爬取数据...")
    result_df = scrape_song_data(df)
    
    # 保存结果
    print(f"保存结果到: {OUTPUT_FILE}")
    result_df.to_csv(OUTPUT_FILE, index=False)
    
    print("完成! 共处理 {} 首歌曲".format(len(result_df)))
    print("成功找到信息的歌曲: {}".format(len(result_df[result_df["page_exists"] == True])))