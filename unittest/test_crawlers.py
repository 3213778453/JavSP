import os
import re
import sys
from glob import glob


file_dir = os.path.dirname(__file__)
data_dir = os.path.join(file_dir, 'data')
sys.path.insert(0, os.path.abspath(os.path.join(file_dir, '..')))

from core.datatype import MovieInfo


# 搜索抓取器并导入它们
all_crawler = []
exclude_files = ('base', 'proxyfree', 'fc2fan')
for file in os.listdir('web'):
    name, ext = os.path.splitext(file)
    if ext == '.py' and name not in exclude_files:
        all_crawler.append('web.' + name)
for i in all_crawler:
    __import__(i)


def compare(dvdid, scraper, file):
    """从本地的数据文件生成Movie实例，并与在线抓取到的数据进行比较"""
    local = MovieInfo(from_file=file)
    online = MovieInfo(dvdid)
    parse_data = getattr(sys.modules[f'web.{scraper}'], 'parse_data')
    parse_data(online)
    # 解包数据再进行比较，以便测试不通过时快速定位不相等的键值
    local_vars = vars(local)
    online_vars = vars(online)
    for k, v in online_vars.items():
        assert v == local_vars.get(k, None)


def test_auto_compare():
    """根据测试数据文件夹中的文件，爬取对应的在线数据进行比较"""
    data_files = glob(data_dir + os.sep + '*.json')
    print('')   # 打印空行，避免与pytest的输出同行显示
    for file in data_files:
        basename = os.path.basename(file)
        match = re.match(r"([-\w]+) \((\w+)\)", basename, re.I)
        if match:
            avid, scraper = match.groups()
            print(f'Comparing {avid} with {scraper} scraper...')
            compare(avid, scraper, file)
