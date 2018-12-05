# 新聞Source列表

## 网易(非自家媒體) http://www.163.com/rss
- Crawler source: 
```sh
http://news.163.com/special/0001220O/news_json.js?
```
- 一天新聞量：150-200則
### 優點:
- 資料容易爬
- 格式固定
- 資訊整齊
### 缺點:
- 新聞量少

## 中國新聞網(非自家媒體) http://www.chinanews.com/
- Crawler source: 
```sh
http://www.chinanews.com/scroll-news/2018/1205/news.shtml
```
- 一天新聞量: 650-750

### 優點:
- 新聞類別多
- 有滾動列表，易取得新聞的url
- 透過調整url時間，可以取得相對時間的新聞

### 缺點:
- 需parse出網址

## 封面(非自家媒體) http://www.thecover.cn/

- 一天新聞量: 450-550

### 優點:
- 新聞類別多
- 格式統一

### 缺點:
- 文章沒有tag
- 需找出url生成的規律，才能找出所有文章

## 人民網(非自家媒體) http://news.people.com.cn/
- Crawler source:
```sh
http://news.people.com.cn/210801/211150/index.js? + (time)
```
- 一天新聞量: 900-1000則

### 優點:
- 新聞量大
- 格式統一

### 缺點:
- 需找出source call出以前文章的方法
