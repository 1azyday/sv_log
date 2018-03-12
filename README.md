# Svlog— 爬取某游戏对战数据进行职业强弱分析
## 网页分析：
* 原始数据网站（日本）：https://shadowlog.com/trend/
* 网站无robot.txt，也无相应限制措施，无需反爬虫手段。
* 为提高数据准确性，目标为水平较高的Master段数据。
* 经抓包测试，页面数据为后端渲染，未发现数据api接口，需要网页爬取。
* 数据公布方式为周报形式，目标区间为2016——2017，按周遍历。
* 网页内数据并不整齐，如同同职业内战数据有留空，不利于后续数据存储和分析，需要处理。
* 涉及到的页面较多，采取等待时间和页面缓存减轻对方服务器负担。

### 网页情况

![image](https://github.com/1azyday/sv_log/blob/master/README/%E7%BD%91%E9%A1%B5%E5%88%86%E6%9E%90/%E7%BD%91%E9%A1%B5%E6%95%B0%E6%8D%AE.PNG)

## 爬取实现：
* Requests负责构造访问请求，Pyquery通过css选择器解提取数据。
* 页面缓存，建立本地爬取缓存，解析页面优先使用缓存数据，减少网站访问次数，提高效率。
* 爬取等待，如连续连续访问网站时，自动休息。
* 数据清理，提取网页数据，统一为list，对不齐数据进行补正。
* 数据存储，将清洗后的数据用python自带的sqlite3存储。

### 页面缓存
![image](https://github.com/1azyday/sv_log/blob/master/README/%E7%88%AC%E5%8F%96%E5%AE%9E%E7%8E%B0/%E9%A1%B5%E9%9D%A2%E7%BC%93%E5%AD%98.PNG)
### 数据存储
![image](https://github.com/1azyday/sv_log/blob/master/README/%E7%88%AC%E5%8F%96%E5%AE%9E%E7%8E%B0/%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE.PNG)

## 数据分析：
* 采用Elo算法（常用于天梯积分系统），根据一周对战胜率对各职业进行迭代分析。当周表现高于Elo算法预期，增加Elo分；低于Elo算法预期，调低Elo分。
* Elo分变动为零和关系，可以直观看出各职业的变化趋向。各职业初始Elo分100，趋向稳定后即为该职业实际强度数值。
* 使用Pandas加载数据，存储数据，方便后续使用。
* 代码实现Elo类，作为当次数据的计算容器。储存当前迭代情况及历次迭代情况。
* Elo类中抽象解耦Elo算法迭代过程，将其转换为各个功能函数进行实现。
* Elo类的三步使用逻辑——Pandas加载爬取的对战数据；初始化Elo类设置；Elo类加载各种对战数据迭代分析，生成csv格式的各职业Elo分统计表。
* 将Elo分数据直观化，以游戏版本更新为时间点，制作更为直观的折线图。

###  Elo迭代记录
![image](https://github.com/1azyday/sv_log/blob/master/README/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/%E8%BF%AD%E4%BB%A3%E5%90%8EElo%E5%88%86%E5%80%BC%E6%83%85%E5%86%B5.PNG)
### WLD版本走势
![image](https://github.com/1azyday/sv_log/blob/master/README/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/WLD%E7%89%88%E6%9C%AC%E8%B5%B0%E5%8A%BF.png)
### SFL版本走势
![image](https://github.com/1azyday/sv_log/blob/master/README/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/SFL%E7%89%88%E6%9C%AC%E8%B5%B0%E5%8A%BF.png)
