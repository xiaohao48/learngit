import requests
import re

for page in range(1, 5):
    url = f'http://ppt.doczj.com/ppt/0b871761-{page}.html'
    result = requests.get(url)
    result.encoding = 'utf-8'
    html = result.text
    reg = '<p class="img"><img src="(.*?)" alt="《护理文书书写》PPT课件" /></p>'
    img_path = re.findall(reg, html)
    print(img_path[0])
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    response = requests.get(img_path[0], headers=head).content

    with open(f'img_ppt_{page}.jpg', 'wb') as f:
        f.write(response)
    f.close()

print('下载完成')
