from config import DOUBAN_BASE_URL

def get_nexturl(CURRENT_PAGE):
    '''根据当前url参数，得出下一页的url'''
    url = DOUBAN_BASE_URL + f'start={CURRENT_PAGE}&filter='
    return url  
    
def has_nexturl(html):
    '''判断是否还有下一页(根据页面是否有下一页按钮)'''
    if not html:
        return False
    from lxml import etree
    tree = etree.HTML(html)
    next_btn = tree.xpath('//span[@class="next"]/link/@href')
    return len(next_btn) > 0
 